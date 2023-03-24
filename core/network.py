from . import helpfunctions as _hf
import numpy as _np
import networkx as _nx
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    import MDAnalysis as _MDAnalysis

from copy import deepcopy
import concurrent.futures
import time

class NetworkAnalysis:
    
    def __init__(self, selection=None, structure=None, trajectories=None, distance=3.5, cut_angle=60., 
                 start=None, stop=None, step=1, residuewise=False, additional_donors=[], 
                 additional_acceptors=[], exclude_donors=[], exclude_acceptors=[], 
                 ions=[], check_angle=True, add_donors_without_hydrogen=False, 
                 add_all_donor_acceptor=False, progress_callback=None, threads=2,
                 water_definition=None, restore_filename=None):
        
        
        if restore_filename != None: return
        
        if selection==None: raise AssertionError('No selection string.')
        if structure==None: raise AssertionError('No structure file path.')
        self._threads = threads
        self._selection = selection
        self._structure = structure
        self._trajectories = trajectories
        #t0 = time.time()
        if trajectories != None: self._universe = _MDAnalysis.Universe(structure, trajectories)
        else: self._universe = _MDAnalysis.Universe(structure)
        self._trajectory_slice = slice(start if isinstance(start, int) else None, stop if isinstance(stop, int) else None, step)
        #t1 = time.time()
        self._mda_selection = self._universe.select_atoms(selection)
        if not self._mda_selection:  raise AssertionError('No atoms match the selection')
        #t2 = time.time()
        if water_definition is not None: self.water_definition = water_definition
        else: self.water_definition = _hf.water_definition
        self._water = self._universe.select_atoms(self.water_definition)
        #t7 = time.time()
        self._water_ids = _hf.MDA_info_list(self._water, detailed_info=False)
        self._water_ids_atomwise = _hf.MDA_info_list(self._water, detailed_info=True)
        #t3 = time.time()
        self.initial_results = {}
        self.filtered_results = {}
        self.nb_frames = len([0 for i in self._universe.trajectory[self._trajectory_slice]])
        
        self.progress_callback = progress_callback
        self.donor_names = additional_donors
        self.acceptor_names = additional_acceptors
        self.check_angle = check_angle
        self.distance = distance
        self.cut_angle = cut_angle
        self._add_donors_without_hydrogen = add_donors_without_hydrogen
        self._add_all_donor_acceptor = add_all_donor_acceptor
        #t4 = time.time()
        sorted_selection = _hf.Selection(self._mda_selection, self.donor_names, self.acceptor_names, add_donors_without_hydrogen, add_all_donor_acceptor)
        if not sorted_selection.donors: da_selection = sorted_selection.acceptors
        elif not sorted_selection.acceptors: da_selection = sorted_selection.donors
        else: da_selection = _MDAnalysis.core.groups.AtomGroup(sorted_selection.donors + sorted_selection.acceptors)
        self._da_selection = da_selection
        #t5 = time.time()
        if sorted_selection.donors: self._donors = _MDAnalysis.core.groups.AtomGroup(sorted_selection.donors)
        else: self._donors = _hf.EmptyGroup()
        self._nb_donors = len(self._donors)
        if sorted_selection.acceptors: self._acceptors = _MDAnalysis.core.groups.AtomGroup(sorted_selection.acceptors)
        else: self._acceptors = _hf.EmptyGroup()
        self._nb_acceptors = len(self._acceptors)
        da_ids = _hf.MDA_info_list(da_selection, detailed_info=False)
        da_ids_atomwise = _hf.MDA_info_list(da_selection, detailed_info=True)
        self._first_water_id = len(da_selection)
        self._first_water_hydrogen_id = len(sorted_selection.hydrogens)
        if not add_donors_without_hydrogen:
            try:
                water_hydrogen = _MDAnalysis.core.groups.AtomGroup(self._water[0].residue.atoms[1:])
                for l in self._water[1:]:
                    water_hydrogen += l.residue.atoms[1:]
            except:
                water_hydrogen = []
        else:
            water_hydrogen = []
        #water_hydrogen = [h for l in self._water for h in l.residue.atoms[1:]]
        if self._nb_acceptors == 0: raise AssertionError('No Acceptors! Could not detect any acceptors in the selection with the current settings.')
        if self._nb_donors == 0: raise AssertionError('No Donors! Could not detect any donors in the selection with the current settings.')
        if not sorted_selection.hydrogens and not water_hydrogen: 
            if check_angle: raise AssertionError('There are no possible hbond donors in the selection and no water. Since check_angle is True, hydrogen is needed for the calculations!')
            else: hydrogen = _hf.EmptyGroup()
        elif not sorted_selection.hydrogens: hydrogen = _MDAnalysis.core.groups.AtomGroup(water_hydrogen)
        elif not water_hydrogen: hydrogen = sorted_selection.hydrogens
        else: hydrogen = sorted_selection.hydrogens + _MDAnalysis.core.groups.AtomGroup(water_hydrogen)
        self._hydrogen = hydrogen
        self.heavy2hydrogen = sorted_selection.donor2hydrogens + [[] for i in sorted_selection.acceptors] + [[self._first_water_hydrogen_id+i, self._first_water_hydrogen_id+i+1] for i in range(0, len(water_hydrogen), 2)]
        self._all_ids = da_ids+self._water_ids
        self._all_ids_atomwise = da_ids_atomwise + self._water_ids_atomwise
        self._resids = _np.array([int(ids.split('-')[2]) for ids in self._all_ids])
        self.initial_graph = _nx.Graph()
        self.filtered_graph = self.initial_graph
        self.joint_occupancy_series = None
        self.joint_occupancy_frames = None
        self.residuewise = residuewise
        self._exclude_backbone_backbone = True
        self.add_missing_residues = 0
        self._connection_position = None
        self._node_positions_3d = {}
        self.centralities = None
        self._current_node_positions = None
        #t6 = time.time()
        #print(t1-t0, t2-t1, t7-t2, t3-t7, t4-t3, t5-t4, t6-t5)
        
    def filter_occupancy(self, min_occupancy, use_filtered=True):
        if use_filtered: results = self.filtered_results
        else: results = self.initial_results
        if len(results) == 0: raise AssertionError('nothing to filter!')
        filtered_result = {key:results[key] for key in results if _np.mean(results[key])>(min_occupancy/100)}
        self.filtered_results = filtered_result
        self._generate_filtered_graph_from_filtered_results()
    
    def filter_connected_component(self, root, use_filtered=True):
        if use_filtered: graph = self.filtered_graph
        else: graph = self.initial_graph
        if len(graph.nodes()) == 0: raise AssertionError('nothing to filter!')
        if root not in graph.nodes(): raise AssertionError('The root node is not in the current graph')
        for component in _nx.connected_components(graph):
            if root in component: break
        self.filtered_graph = graph.subgraph(component)
        self._generate_filtered_results_from_filtered_graph()
    
    def filter_all_paths(self, start, goal, max_len=_np.inf, only_shortest=True, use_filtered=True):
        if use_filtered: graph = self.filtered_graph
        else: graph = self.initial_graph 
        if len(graph.nodes()) == 0: raise AssertionError('nothing to filter!')
        if start not in graph.nodes(): raise AssertionError('The start node is not in the graph')
        if goal not in graph.nodes(): raise AssertionError('The goal node is not in the graph')
        try: 
            if only_shortest: paths = list(_nx.all_shortest_paths(graph, start, goal))
            else: paths = list(_nx.all_simple_paths(graph, start, goal, cutoff=max_len))
        except: 
            raise AssertionError('Root and target are not connected!')
        edges = []
        for path in paths:
            edges += _hf.pairwise(path)
        self.filtered_graph = graph.edge_subgraph(edges)
        self._generate_filtered_results_from_filtered_graph()

    def filter_single_path(self, path_nodes, use_filtered=True):
        if use_filtered: graph = self.filtered_graph
        else: graph = self.initial_graph 
        if len(graph.nodes()) == 0: raise AssertionError('nothing to filter!')
        keep_edges = []
        for resa, resb in _hf.pairwise(path_nodes):
            edge = (resa, resb)
            if edge in graph.edges():
                keep_edges.append(edge)
            else:
                raise AssertionError('There is no connection between {} and {}'.format(resa, resb))
        self.filtered_graph = graph.edge_subgraph(keep_edges)
        self._generate_filtered_results_from_filtered_graph()
    
    def filter_between_segnames(self, msegna, msegnb=None, use_filtered=True):
        segna, segnb = deepcopy(msegna), deepcopy(msegnb)
        if use_filtered: results = self.filtered_results
        else: results = self.initial_results
        if len(results) == 0: raise AssertionError('nothing to filter!')
        if (segna is None) and (segnb is not None): segna, segnb = segnb, segna
        segnames = [segna, segnb]
        keep_bonds = []
        for key in results:
            sa,_,_, sb,_,_ = _hf.deconst_key(key, self.residuewise)
            if ((sa in segnames) and (sb in segnames) and (sa!=sb) and (segnb!=None)) or (_np.logical_or((sa in segnames),(sb in segnames)) and (segnb==None)) or ((sa in segnames) and (sb in segnames) and (sa==sb) and (segnb==segna)):
                keep_bonds.append(key)
        self.filtered_results = {key:results[key] for key in keep_bonds}
        self._generate_filtered_graph_from_filtered_results()
        
    def filter_between_resnames(self, mresna, mresnb=None, use_filtered=True):
        resna, resnb = deepcopy(mresna), deepcopy(mresnb)
        if use_filtered: results = self.filtered_results
        else: results = self.initial_results
        if len(results) == 0: raise AssertionError('nothing to filter!')
        if (resna is None) and (resnb is not None): resna, resnb = resnb, resna
        resnames = [resna, resnb]
        keep_bonds = []
        for key in results:
            _,ra,_, _,rb,_ = _hf.deconst_key(key, self.residuewise)
            if ((ra in resnames) and (rb in resnames) and (ra!=rb) and (resnb!=None)) or (_np.logical_or((ra in resnames),(rb in resnames)) and (resnb==None)) or ((ra in resnames) and (rb in resnames) and (ra==rb) and (resnb==resnb)):
                keep_bonds.append(key)
        self.filtered_results = {key:results[key] for key in keep_bonds}
        self._generate_filtered_graph_from_filtered_results()
        
    def filter_between_resids(self, mresida, mresidb=None, use_filtered=True):
        resida, residb = deepcopy(mresida), deepcopy(mresidb)
        if use_filtered: results = self.filtered_results
        else: results = self.initial_results
        if len(results) == 0: raise AssertionError('nothing to filter!')
        if (resida is None) and (residb is not None): resida, residb = residb, resida
        keep_bonds = []
        for key in results:
            _,_,rida, _,_,ridb = _hf.deconst_key(key, self.residuewise)
            if residb is not None:
                if not (((rida in resida) and (ridb in residb)) or ((rida in residb) and (ridb in resida))): continue
            else:
                if not _np.logical_or((rida in resida),(ridb in resida)): continue
            keep_bonds.append(key)
        self.filtered_results = {key:results[key] for key in keep_bonds}
        self._generate_filtered_graph_from_filtered_results()
    
    def filter_set_nodes(self, nodes, use_filtered=True):
        if use_filtered: graph = self.filtered_graph
        else: graph = self.initial_graph 
        present_nodes = [node for node in nodes if node in graph.nodes]
        self.filtered_graph = graph.subgraph(present_nodes)
        self._generate_filtered_results_from_filtered_graph()
    
    def filter_to_frame(self, frame, use_filtered=True):
        _ = self._compute_graph_in_frame(frame, True, use_filtered)
    
    def _centrality_per_frame_range(self, r, centrality_type, use_filtered):
        centralities = []
        for i in r:
            g_i = self._compute_graph_in_frame(i, use_filtered=use_filtered)
            if centrality_type == 'betweenness': 
                centrality_normalized_i = _nx.betweenness_centrality(g_i, normalized=True)
                nb_nodes = len(centrality_normalized_i)
                normalization_factor = (nb_nodes - 1)*(nb_nodes - 2)/2
                centrality_i = {key:value*normalization_factor for key, value in centrality_normalized_i.items()}
            elif centrality_type == 'degree': 
                centrality_normalized_i = _nx.degree_centrality(g_i)
                normalization_factor = len(centrality_normalized_i)-1
                centrality_i = {key:value*normalization_factor for key, value in centrality_normalized_i.items()}
            else: 
                raise AssertionError("centrality_type has to be 'betweenness' or 'degree' or 'biological'")
            centralities.append((i,centrality_i,centrality_normalized_i))
            if self.progress_callback is not None: self.progress_callback.emit('Computing {} centrality in frame {}/{}'.format(centrality_type, i, self.nb_frames))

        return centralities
    
    def compute_centrality(self, centrality_type='betweenness', use_filtered=True):
        if use_filtered: graph = self.filtered_graph
        else: graph = self.initial_graph 
        frames = self.nb_frames

        if self.progress_callback is not None: self.progress_callback.emit('Computing {} centrality'.format(centrality_type))
        centralities = {node:_np.zeros(frames) for node in graph.nodes()}
        centralities_normalized = {node:_np.zeros(frames) for node in graph.nodes()}

        for r in _hf.partition(range(frames), max(10, int(frames/(self._threads-1)))):
            for i, centrality_i, centrality_normalized_i in self._centrality_per_frame_range(r, centrality_type, use_filtered): 
                for node in centrality_i: 
                    centralities[node][i] = centrality_i[node]
                    centralities_normalized[node][i] = centrality_normalized_i[node]   

        for node in centralities: 
            centralities[node] = _hf.round_to_1(centralities[node].mean())
            centralities_normalized[node] = _hf.round_to_1(centralities_normalized[node].mean())
        

        return centralities, centralities_normalized
    
    def _reload_universe(self):
        super(NetworkAnalysis, self)._reload_universe()
        sorted_selection = _hf.Selection(self._mda_selection, self.donor_names, self.acceptor_names, self._add_donors_without_hydrogen, self._add_all_donor_acceptor)
        if not sorted_selection.donors: da_selection = sorted_selection.acceptors
        elif not sorted_selection.acceptors: da_selection = sorted_selection.donors
        else: da_selection = _MDAnalysis.core.groups.AtomGroup(sorted_selection.donors + sorted_selection.acceptors)
        self._da_selection = da_selection
        if sorted_selection.donors: self._donors = _MDAnalysis.core.groups.AtomGroup(sorted_selection.donors)
        else: self._donors = _hf.EmptyGroup()
        self._nb_donors = len(self._donors)
        if sorted_selection.acceptors: self._acceptors = _MDAnalysis.core.groups.AtomGroup(sorted_selection.acceptors)
        else: self._acceptors = _hf.EmptyGroup()
        self._nb_acceptors = len(self._acceptors)
        self._first_water_id = len(da_selection)
        self._first_water_hydrogen_id = len(sorted_selection.hydrogens)
        if not self._add_donors_without_hydrogen:
            try:
                water_hydrogen = _MDAnalysis.core.groups.AtomGroup(self._water[0].residue.atoms[1:])
                for l in self._water[1:]:
                    water_hydrogen += l.residue.atoms[1:]
            except:
                water_hydrogen = []
        else:
            water_hydrogen = []

        if not sorted_selection.hydrogens and not water_hydrogen: 
            if self._check_angle: raise AssertionError('There are no possible hbond donors in the selection and no water. Since check_angle is True, hydrogen is needed for the calculations!')
            else: hydrogen = _hf.EmptyGroup()
        elif not sorted_selection.hydrogens: hydrogen = _MDAnalysis.core.groups.AtomGroup(water_hydrogen)
        elif not water_hydrogen: hydrogen = sorted_selection.hydrogens
        else: hydrogen = sorted_selection.hydrogens + _MDAnalysis.core.groups.AtomGroup(water_hydrogen)
        self._hydrogen = hydrogen
    
    def get_segnames_and_resnames(self):
        segnames = {node.split('-')[0] for node in self.initial_graph.nodes}
        resnames = {node.split('-')[1] for node in self.initial_graph.nodes}
        return segnames, resnames

    def get_occupancies(self, as_labels=False):
        occupancies = {key:_np.mean(self.initial_results[key]) for key in self.initial_results}
        if as_labels: occupancies = {key:str(round(value*100)) for key, value in occupancies.items()}
        return occupancies

    def set_centralities(self):
        betweenness, betweenness_norm = self.compute_centrality(centrality_type='betweenness', use_filtered=False)
        degree, degree_norm = self.compute_centrality(centrality_type='degree', use_filtered=False)
        self.centralities = {'betweenness':{True:betweenness_norm, False:betweenness},
                             'degree':{True:degree_norm, False:degree}}

    def get_centralities(self):
        return self.centralities

    def set_node_positions_3d(self, include_water=False):
        graph = self.initial_graph
        nodes = _np.array(graph.nodes())
        if self.residuewise: all_id = _np.array(self._all_ids)
        else: all_id = _np.array(self._all_ids_atomwise)
        if not include_water: all_id = all_id[:self._first_water_id]
        nb_samples = min(100, self.nb_frames)
        #t = time.time()
        for i, in_frame in enumerate(_np.linspace(0, self.nb_frames-1, nb_samples, dtype=int)):  
            if self.progress_callback is not None: self.progress_callback.emit('Extracting positional information from frame {}'.format(in_frame))
            self._universe.trajectory[in_frame]
            if include_water: all_coordinates = _np.vstack((self._da_selection.positions, self._water.positions.reshape((-1,3))))
            else: all_coordinates = self._da_selection.positions.copy()
            for node in nodes:
                try:
                    self._node_positions_3d[node][i] = all_coordinates[all_id == node].mean(0)
                except KeyError:
                    self._node_positions_3d[node] = _np.empty((nb_samples, 3))
                    self._node_positions_3d[node][i] = all_coordinates[all_id == node].mean(0)
        #print(time.time()-t)
        if self.progress_callback is not None: self.progress_callback.emit('Done!')
        
    def get_node_positions_3d(self, in_frame=0):
        return {key:value[in_frame] for key, value in self._node_positions_3d.items()}
    
    def get_node_positions_2d(self, projection='PCA', in_frame=0, adjust_water_positions=False):
        if adjust_water_positions: 
            graph = self._compute_graph_in_frame(in_frame, use_filtered=True)
            pos = _np.array([value for value in _hf.adjust_water_positions(graph, self.get_node_positions_3d(in_frame)).values()])
        else:
            pos = _np.array([value for value in self.get_node_positions_3d(in_frame).values()])
        if projection == 'PCA':
            pos2d, _ = _hf.pca_2d_projection(pos)
        elif projection == 'XY':
            pos2d = pos[:,0:2]
        elif projection == 'ZY':
            pos2d = pos[:,1:3]
        else:
            raise AssertionError("invalid projection type. projection has to be 'PCA', 'XY', or 'ZY'")
        nodes = list(self._node_positions_3d.keys())
        pos={node:p for p, node in zip(pos2d, nodes)}
        return pos
    
    def get_current_node_positions(self):
        return self._current_node_positions

    def get_short_node_labels(self):
        graph = self.initial_graph
        labels={}
        for j, node in enumerate(graph.nodes()):
            if self.residuewise: segname, resname, resid = node.split('-')
            else: segname, resname, resid, atomname = node.split('-')
            try:
                if self.residuewise:
                    if resname in ['TIP3', 'HOH']: labels[node] = 'O\n' + str(int(resid))
                    else: labels[node] = _hf.aa_three2one[resname]+str(int(resid)+self.add_missing_residues)
                else:
                    if resname in ['TIP3', 'HOH']: labels[node] = 'O\n' + str(int(resid))
                    else: labels[node] = _hf.aa_three2one[resname]+str(int(resid)+self.add_missing_residues)+'\n'+atomname
            except KeyError:
                labels[node] = resname+resid
        return labels
    
    def _compute_graph_in_frame(self, frame, set_as_filtered_results=False, use_filtered=True):
        if use_filtered: results = self.filtered_results
        else: results = self.initial_results
        keep_edges=[]
        for key in results:
            if results[key][frame]:
                keep_edges.append((key.split(':')[0], key.split(':')[1]))
        graph = _nx.Graph()
        graph.add_edges_from(keep_edges)
        if set_as_filtered_results: 
            self.filtered_graph = graph
            self._generate_filtered_results_from_filtered_graph()
        return graph
    
    def _all_frame_graphs(self):
        for i in range(self.nb_frames):
            yield self._compute_graph_in_frame(i)
    
    def _generate_filtered_results_from_filtered_graph(self):
        temp_res = {}
        for resa, resb in self.filtered_graph.edges():
            key, key_check = ':'.join((resa, resb)), ':'.join((resb, resa))
            try: temp_res[key] = self.initial_results[key]
            except KeyError:  temp_res[key_check] = self.initial_results[key_check]
        self.filtered_results = temp_res 
    
    def _generate_graph_from_current_results(self):
        self.initial_graph = _hf.dict2graph(self.initial_results)
        
    def _generate_filtered_graph_from_filtered_results(self):
        self.filtered_graph = self.initial_graph.edge_subgraph([tuple(connection.split(':')) for connection in self.filtered_results])
        
    def _set_results(self, result):
        self.initial_results = result
        self.filtered_results = result
        self._generate_graph_from_current_results()
        self._generate_filtered_graph_from_filtered_results()
        
    def prepare_for_pickling(self):
        self._universe=None
        self._water=None
        self._hydrogen=None
        self._mda_selection=None
        self._da_selection=None
        self._donors=None
        self._acceptors=None   
        self.progress_callback = None
        self.initial_graph = None
        self.filtered_graph = None

    def restore_after_pickle(self):
        self._generate_graph_from_current_results()
        self._generate_filtered_graph_from_filtered_results()
        