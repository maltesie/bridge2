#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    Author: Malte Siemers, Freie Universität Berlin 
#   
#    If you use this software or anything it produces for work to be published,
#    please cite:
#    
#    Malte Siemers, Michalis Lazaratos, Konstantina Karathanou,
#    Federico Guerra, Leonid Brown, and Ana-Nicoleta Bondar. 
#    Bridge: A graph-based algorithm to analyze dynamic H-bond networks in
#    membrane proteins, Journal of Chemical Theory and Computation 15 (12) 6781-6798
#
#    and
#
#    Federico Guerra, Malte Siemers, Christopher Mielack, and Ana-Nicoleta Bondar
#    Dynamics of Long-Distance Hydrogen-Bond Networks in Photosystem II
#    The Journal of Physical Chemistry B 2018 122 (17), 4625-4641

from . import helpfunctions as _hf
from .network import NetworkAnalysis
import numpy as _np
import networkx as _nx
import MDAnalysis as _MDAnalysis
from scipy import spatial as _sp
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

class WireAnalysis(NetworkAnalysis):
    
    def __init__(self, selection=None, structure=None, trajectories=None, distance=3.5, cut_angle=60., 
                 start=None, stop=None, step=1, residuewise=False, additional_donors=[], 
                 additional_acceptors=[], exclude_donors=[], exclude_acceptors=[], 
                 ions=[], check_angle=True, add_donors_without_hydrogen=False, 
                 add_all_donor_acceptor=False, progress_callback=None, 
                 water_definition=None, restore_filename=None):
        
        super(WireAnalysis, self).__init__(selection=selection, structure=structure, trajectories=trajectories, 
             distance=distance, cut_angle=cut_angle, start=start, stop=stop, step=step, 
             additional_donors=additional_donors, additional_acceptors=additional_acceptors,
             exclude_donors=exclude_donors, exclude_acceptors=exclude_acceptors,
             ions=ions, check_angle=check_angle, add_donors_without_hydrogen=add_donors_without_hydrogen, 
             add_all_donor_acceptor=add_all_donor_acceptor, progress_callback=progress_callback,
             restore_filename=restore_filename, residuewise=residuewise, water_definition=water_definition)
        
        if restore_filename != None: return
        if not self._mda_selection:  raise AssertionError('No atoms match the selection')
        sorted_selection = _hf.Selection(self._mda_selection, self.donor_names, self.acceptor_names, add_donors_without_hydrogen=add_donors_without_hydrogen)
        if not sorted_selection.donors: da_selection = sorted_selection.acceptors
        elif not sorted_selection.acceptors: da_selection = sorted_selection.donors
        else: da_selection = _MDAnalysis.core.groups.AtomGroup(sorted_selection.donors + sorted_selection.acceptors)
        da_ids = _hf.MDA_info_list(da_selection)
        self.hashs = {}
        self.hash_table = {}
        da_u, da_ind, da_inv = _np.unique(da_ids, return_index=True, return_inverse=True)
        self.da_trans = da_ind[da_inv]
        self.wire_lengths = {}
    
    def set_water_wires_csr(self, max_water=5, allow_direct_bonds = True, water_in_convex_hull=False):
        
        distances = {}
        path_hashs = {}
        frame_count = 0
        hash_table = {}
        no_direct_bonds = False
        self._allow_direct_bonds = allow_direct_bonds
        #t0 = time.time()
        for ts in self._universe.trajectory[self._trajectory_slice]:
        
            water_coordinates = self._water.positions
            selection_coordinates = self._da_selection.positions
            selection_tree = _sp.cKDTree(selection_coordinates)
            try:
                d_tree = _sp.cKDTree(self._donors.positions)
                a_tree = _sp.cKDTree(self._acceptors.positions)
            except:
                no_direct_bonds = True
            hydrogen_coordinates = self._hydrogen.positions
    
            water_tree = _sp.cKDTree(water_coordinates, leafsize=32)
            local_water_index = []
            [local_water_index.extend(l) for l in water_tree.query_ball_point(selection_coordinates, float(max_water+1)*self.distance/2.)]
            local_water_index = _np.unique(local_water_index)
            local_water_coordinates = water_coordinates[local_water_index]
            
            if water_in_convex_hull:
                hull = _sp.Delaunay(selection_coordinates)
                local_water_index_hull = (hull.find_simplex(local_water_coordinates) != -1).nonzero()[0]
                local_water_coordinates = water_coordinates[local_water_index[local_water_index_hull]]
            
            local_water_tree = _sp.cKDTree(local_water_coordinates)
            
            local_water_index += self._first_water_id
            local_pairs = [(i, local_water_index[j]) for i, bla in enumerate(selection_tree.query_ball_tree(local_water_tree, self.distance)) for j in bla]
            local_water_index -= self._first_water_id
            try:
                water_pairs = local_water_index[_np.array(list(local_water_tree.query_pairs(self.distance)))]
            except IndexError:
                water_pairs = da_pairs = _np.array([])
            
            if not no_direct_bonds: 
                da_pairs = _np.array([[i, j] for i,donors in enumerate(a_tree.query_ball_tree(d_tree, self.distance)) for j in donors])
                da_pairs[:,0] += self._nb_donors
            else:
                da_pairs = _np.array([])
            if self.check_angle:
                all_coordinates = _np.vstack((selection_coordinates, water_coordinates))
                da_hbonds = _hf.check_angle(da_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
                water_hbonds = _hf.check_angle_water(water_pairs, water_coordinates, hydrogen_coordinates[self._first_water_hydrogen_id:], self.cut_angle)
                local_hbonds = _hf.check_angle(local_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                da_hbonds = da_pairs
                water_hbonds = water_pairs
                local_hbonds = local_pairs
            da_hbonds = _np.sort(da_hbonds)
            water_hbonds = _np.sort(water_hbonds) + self._first_water_id
            local_hbonds = _np.sort(_np.array(local_hbonds))
            local_hbonds[:,0]=self.da_trans[local_hbonds[:,0]]
            if no_direct_bonds: hbonds = _np.vstack((local_hbonds, water_hbonds))
            else: hbonds = _np.vstack((_np.vstack((da_hbonds,local_hbonds)), water_hbonds))
            no_direct_bonds = False
            water_da = _np.zeros(len(hbonds), dtype=bool)
            water_da[len(da_hbonds):len(da_hbonds)+len(local_hbonds)]=True
            water_water = _np.zeros(len(hbonds), dtype=bool)
            water_water[len(da_hbonds)+len(local_hbonds):] = True
            uniques, rowsncols = _np.unique(hbonds, return_inverse=True)
            rows, cols = rowsncols.reshape(hbonds.shape).T
            nb_nodes = uniques.size
            residues = (uniques < self._first_water_id).nonzero()[0]
            data = _np.ones(len(hbonds), dtype=float)
            g = csr_matrix((data, (rows, cols)), shape=(nb_nodes, nb_nodes))
            local_rows, local_cols = rows[water_da], cols[water_da]
            g[local_rows, local_cols] = _np.inf
            already_checked = []
            for source in residues:
                source_index = local_rows == source
                if source_index.sum()==0: continue
                g[local_rows[source_index], local_cols[source_index]] = 1.0
                lengths, predecessors = dijkstra(g, directed=False, indices=source, unweighted=False, limit=max_water, return_predecessors=True)
                g[local_rows[source_index], local_cols[source_index]] = _np.inf
                in_range = _np.nonzero(lengths <= max_water)[0]
                target_index = _np.in1d(local_cols,in_range)
                targets = _np.unique(local_rows[target_index])
                for target in targets:
                    if target in already_checked or target==source: continue
                    target_water = local_cols[(local_rows==target) & target_index]
                    length_index = _np.argmin(lengths[target_water])
                    length = lengths[target_water][length_index]
                    wire = uniques[[_hf.predecessor_recursive_1d(ii, predecessors, target_water[length_index]) for ii in range(int(length))[::-1]]+[target]]
                    ai, bi = _np.sort(uniques[[source, target]])
                    if self.residuewise: aname, bname = self._all_ids[ai], self._all_ids[bi]
                    else: wire_info = aname, bname = self._all_ids_atomwise[ai], self._all_ids_atomwise[bi]
                    if aname == bname: continue
                    wire_hash = hash(wire.tobytes())
                    hash_table[wire_hash] = wire
                    wire_info = ':'.join(sorted([aname, bname]))
                    try:
                        distances[wire_info][frame_count] = length
                        path_hashs[wire_info][frame_count] = wire_hash
                    except KeyError:
                        distances[wire_info] = _np.ones(self.nb_frames, dtype=int) * _np.inf
                        path_hashs[wire_info] = _np.arange(self.nb_frames, dtype=int)
                        distances[wire_info][frame_count] = length
                        path_hashs[wire_info][frame_count] = wire_hash
                already_checked.append(source)
            
            if allow_direct_bonds:
                for ai, bi in da_hbonds:
                    if self.residuewise: aname, bname = self._all_ids[ai], self._all_ids[bi]
                    else: aname, bname = self._all_ids_atomwise[ai], self._all_ids_atomwise[bi]
                    if aname == bname: continue
                    wire_info = ':'.join(sorted([aname, bname]))
                    try:
                        path_hashs[wire_info][frame_count] = -1
                        distances[wire_info][frame_count] = 0
                    except:
                        distances[wire_info] = _np.ones(self.nb_frames, dtype=int)*_np.inf
                        distances[wire_info][frame_count] = 0
                        path_hashs[wire_info] = _np.arange(self.nb_frames, dtype=int)
                        path_hashs[wire_info][frame_count] = -1
            frame_count += 1
            
            if self.progress_callback is not None: self.progress_callback.emit('Computing water wires in frame {}/{}'.format(frame_count, self.nb_frames))
        #print('Time to compute {} water wires: {}s'.format(len(distances), _np.round(time.time()-t0,5)))
        self._set_results(distances)
        self.wire_lengths = distances
        self.hashs = path_hashs
        self.hash_table = hash_table


    def set_water_wires(self, max_water=5, allow_direct_bonds=True, water_in_convex_hull=False):
        
        intervals_results = {}
        results = {}
        frame_count = 0
        frames = self.nb_frames
        this_frame_table = {}
        no_direct_bonds = False
        self._allow_direct_bonds = allow_direct_bonds
        #t0 = time.time()
        for ts in self._universe.trajectory[self._trajectory_slice]:
    
            water_coordinates = self._water.positions
            selection_coordinates = self._da_selection.positions
            water_tree = _sp.cKDTree(water_coordinates, leafsize=32)
            selection_tree = _sp.cKDTree(selection_coordinates)
            try:
                d_tree = _sp.cKDTree(self._donors.positions)
                a_tree = _sp.cKDTree(self._acceptors.positions)
            except:
                no_direct_bonds = True
            hydrogen_coordinates = self._hydrogen.positions
    
            local_water_index = []
            [local_water_index.extend(l) for l in water_tree.query_ball_point(selection_coordinates, float(max_water+1)*self.distance/2.)]
            local_water_index = _np.unique(local_water_index)
            if local_water_index.size>0: 
                local_water_coordinates = water_coordinates[local_water_index]
                
                
                if water_in_convex_hull:
                    hull = _sp.Delaunay(selection_coordinates)
                    local_water_index_hull = (hull.find_simplex(local_water_coordinates) != -1).nonzero()[0]
                    local_water_coordinates = water_coordinates[local_water_index[local_water_index_hull]]
                    
                local_water_tree = _sp.cKDTree(local_water_coordinates)
                
                local_water_index += self._first_water_id
                local_pairs = _np.array([(i, local_water_index[j]) for i, bla in enumerate(selection_tree.query_ball_tree(local_water_tree, self.distance)) for j in bla])
                local_water_index -= self._first_water_id
                try:
                    water_pairs = local_water_index[_np.array(list(local_water_tree.query_pairs(self.distance)))]
                except IndexError:
                    water_pairs = da_pairs = _np.array([])
            else:
                water_pairs = local_pairs = _np.array([])
            
            if not no_direct_bonds: 
                da_pairs = _np.array([[i, j] for i,donors in enumerate(a_tree.query_ball_tree(d_tree, self.distance)) for j in donors])
                da_pairs[:,0] += self._nb_donors
            else:
                da_pairs = _np.array([])
                no_direct_bonds = False
            
            if self.check_angle:
                all_coordinates = _np.vstack((selection_coordinates, water_coordinates))
                da_hbonds = _hf.check_angle(da_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
                if water_pairs.size > 0: water_hbonds = _hf.check_angle_water(water_pairs, water_coordinates, hydrogen_coordinates[self._first_water_hydrogen_id:], self.cut_angle)
                else: water_hbonds = _np.array([])
                if local_pairs.size > 0: local_hbonds = _hf.check_angle(local_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
                else: local_hbonds = _np.array([])
            else:
                da_hbonds = da_pairs
                water_hbonds = water_pairs
                local_hbonds = local_pairs
            
            da_hbonds = _np.sort(da_hbonds)
            water_hbonds = _np.sort(water_hbonds) + self._first_water_id
            
            if local_hbonds.size > 0:
                local_hbonds = _np.sort(_np.array(local_hbonds))
                local_hbonds[:,0]=self.da_trans[local_hbonds[:,0]]
    
                g = _nx.Graph()
                g.add_edges_from(water_hbonds)
                
                residues = _np.unique(local_hbonds[:,0])
                already_checked=[]
                for source in residues:
                    already_checked_targets = []
                    source_water_index = local_hbonds[:,0]==source
        
                    if not source_water_index.any(): continue
        
                    g.add_edges_from(local_hbonds[source_water_index])
                    paths = _nx.single_source_shortest_path(g,source,max_water)
                    g.remove_node(source)
                    
                    idx = _np.array([self._all_ids[bl]!=self._all_ids[source] for bl in local_hbonds[:,0]])
                    target_water_set = set(paths) & set(local_hbonds[:,1][idx])
                    twlist = list(target_water_set)
                    
                    all_targets_index = _np.in1d(local_hbonds[:,1], _np.array(twlist))
                    
                    for target, last_water in local_hbonds[all_targets_index]:
        
                        if target in already_checked or target in already_checked_targets: continue
                        if self.residuewise: sourcename, targetname = self._all_ids[source], self._all_ids[target]
                        else: sourcename, targetname = self._all_ids_atomwise[source], self._all_ids_atomwise[target]
                        if sourcename == targetname: continue
                        wire = paths[last_water] + [target]
                        wire_hash = hash(str(wire))
                        this_frame_table[wire_hash] = wire
                        wire_info = ':'.join(sorted([sourcename, targetname]))
                        water_in_wire = len(wire)-2
                        
                        if self.residuewise:
                            try: water_already_found = results[wire_info][frame_count]
                            except: water_already_found = _np.inf
                            if (water_in_wire >= water_already_found): continue    
                            
                        try:
                            results[wire_info][frame_count] = water_in_wire
                            intervals_results[wire_info][frame_count] = wire_hash
                        except:
                            results[wire_info] = _np.ones(frames)*_np.inf
                            results[wire_info][frame_count] = water_in_wire
                            intervals_results[wire_info] = _np.arange(frames, dtype=int)
                            intervals_results[wire_info][frame_count] = wire_hash
                    
                    already_checked.append(source)  
            
            if allow_direct_bonds:
                for source, target in da_hbonds:
                    if self.residuewise: sourcename, targetname = self._all_ids[source], self._all_ids[target]
                    else: sourcename, targetname = self._all_ids_atomwise[source], self._all_ids_atomwise[target]
                    if sourcename == targetname: continue
                    wire_info = ':'.join(sorted([sourcename, targetname]))
                    try:
                        intervals_results[wire_info][frame_count] = -1
                        results[wire_info][frame_count] = 0
                    except:
                        results[wire_info] = _np.ones(frames, dtype=int)*_np.inf
                        results[wire_info][frame_count] = 0
                        intervals_results[wire_info] = _np.arange(frames, dtype=int)
                        intervals_results[wire_info][frame_count] = -1
            
            frame_count += 1
            if self.progress_callback is not None: self.progress_callback.emit('Computing water wires in frame {}/{}'.format(frame_count, self.nb_frames))
        #print('Time to compute {} water wires with {} max waters and convex hull {}: {}s'.format(len(results), max_water, water_in_convex_hull, _np.round(time.time()-t0,5)))
        self._set_results(results)
        self.wire_lengths = results
        self.hashs = intervals_results
        self.hash_table = this_frame_table
    
    def get_endurance_times(self, as_labels=False, frame_time=None, frame_unit=None):
        results = self.initial_results
        endurance_times = {}
        for bond in results:
            hashs = self.hashs[bond]
            endurance_time = _np.diff(_np.hstack(([0], _np.nonzero(_np.diff(hashs))[0] + 1, [self.nb_frames])))
            endurance_times[bond] = endurance_time.max()
        if as_labels: 
            if frame_time is not None:
                endurance_times = {key:_hf.unit_to_string(value*frame_time, frame_unit) for key, value in endurance_times.items()}
            else:
                endurance_times = {key:str(value) for key, value in endurance_times.items()}
        return endurance_times 
    
    def get_nb_waters(self, as_labels=False):
        nb_waters = {key:value[value!=_np.inf].mean() for key,value in self.wire_lengths.items()}
        if as_labels:
            nb_waters = {key:str(round(value,1)) for key,value in nb_waters.items()}
        return nb_waters
    
    def _set_results(self, wire_lengths):
        occupancy = {connection:wire_lengths[connection]!=_np.inf for connection in wire_lengths}
        self.initial_results = occupancy
        self.filtered_results = occupancy
        self._generate_graph_from_current_results()
        g = _hf.dict2graph(wire_lengths, value_name='wire_length')
        self.initial_graph.update(g)
        self._generate_filtered_graph_from_filtered_results()
        
    def restore_after_pickle(self):
        self._set_results(self.wire_lengths)
