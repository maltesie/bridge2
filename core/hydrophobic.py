from . import helpfunctions as _hf
from .network import NetworkAnalysis
import numpy as _np
import MDAnalysis as _MDAnalysis
from scipy import spatial as _sp

class HydrophobicAnalysis(NetworkAnalysis):
    
    def __init__(self, selection=None, structure=None, trajectories=None, distance=5., 
                 partially_hydrophobic_residues=True, start=None, stop=None, step=1, 
                 residuewise=False, progress_callback=None, restore_filename=None):
        
        if restore_filename != None: 
            self.load_from_file(restore_filename)
            return
        
        self.progress_callback = progress_callback
        if selection==None: raise AssertionError('No selection string.')
        if structure==None: raise AssertionError('No structure file path.')
        self._selection = selection
        self._structure = structure
        self._trajectories = trajectories
        if trajectories != None: self._universe = _MDAnalysis.Universe(structure, trajectories)
        else: self._universe = _MDAnalysis.Universe(structure)
        self._trajectory_slice = slice(start if isinstance(start, int) else None, stop if isinstance(stop, int) else None, step)
        
        self._mda_selection = self._universe.select_atoms(selection)
        if not self._mda_selection:  raise AssertionError('No atoms match the selection')
        self._water = _hf.EmptyGroup()
        self._ions = _hf.EmptyGroup()
        self._ions_ids = []
        self._ions_ids_atomwise = []
        self.add_missing_residues = 0
        self._partially_hydrophobic_residues = partially_hydrophobic_residues
        
        if partially_hydrophobic_residues:
            self._da_selection = self._mda_selection.select_atoms('not (backbone or name H*) and \
                                                                       ((resname ALA) or \
                                                                        (resname VAL) or \
                                                                        (resname ILE) or \
                                                                        (resname LEU) or \
                                                                        (resname MET) or \
                                                                        (resname TRP) or \
                                                                        (resname PHE) or \
                                                                        (resname PRO) or \
                                                                        (resname ASP and name CB) or \
                                                                        (resname GLU and (name CB or name CG)) or \
                                                                        (resname THR and name CG2) or \
                                                                        (resname TYR and not name OH) or \
                                                                        (resname ASN and not (name OD1 or name ND2)) or \
                                                                        (resname GLN and not (name OE1 or name NE2)) or \
                                                                        (resname CYS and not name SH) or \
                                                                        (resname SER and not name OG))')
        else:
            self._da_selection = self._mda_selection.select_atoms('not (backbone or name H*) and \
                                                                       ((resname ALA) or \
                                                                        (resname VAL) or \
                                                                        (resname ILE) or \
                                                                        (resname LEU) or \
                                                                        (resname MET) or \
                                                                        (resname TRP) or \
                                                                        (resname PHE) or \
                                                                        (resname PRO))')
        
        self._first_water_id = len(self._da_selection)
        self.distance = distance
        self.residuewise = residuewise
        self._all_ids = _hf.MDA_info_list(self._da_selection, detailed_info=False)
        self._all_ids_atomwise = _hf.MDA_info_list(self._da_selection, detailed_info=True)
        self.nb_frames = sum([1 for ts in self._universe.trajectory[self._trajectory_slice]])
        self.initial_results = {}
        self.filtered_results = {}
        self.applied_filters = {'resnames':None, 
                                'segnames':None, 
                                'resids':None, 
                                'shortest_paths':None, 
                                'single_path':None, 
                                'occupancy':None, 
                                'connected_component':None, 
                                'shells':None, 
                                'avg_least_bonds':None, 
                                'backbone':None}
        self.add_missing_residues = 0
        self._connection_position = None
        self._node_positions_3d = {}
        self.centralities = None
        self._current_node_positions = None
        
    def set_hydrophobic_contacts_in_selection(self):
        frame_count = 0
        frames = self.nb_frames
        result = {}
        for ts in self._universe.trajectory[self._trajectory_slice]:
            
            hydrophobic_coordinates = self._da_selection.positions
            hydrophobic_tree = _sp.cKDTree(hydrophobic_coordinates)
            pairs = [pair for pair in hydrophobic_tree.query_pairs(self.distance)]
            
            sorted_bonds = _np.sort(pairs, axis=1)
            if self.residuewise: frame_res = [self._all_ids[i] + ':' + self._all_ids[j] for (i, j) in sorted_bonds]
            else: frame_res = [self._all_ids_atomwise[i] + ':' + self._all_ids_atomwise[j] for (i, j) in sorted_bonds]
            
            for contact in frame_res:
                a, b = contact.split(':')
                if a.split('-')[:3] == b.split('-')[:3]: continue
                try:
                    result[contact][frame_count] = True
                except:
                    result[contact] = _np.zeros(frames, dtype=bool)
                    result[contact][frame_count] = True
                    
            frame_count += 1
        
        self._set_results(result)
        
    def _set_results(self, result):
        self.initial_results = result
        self.filtered_results = result
        self._generate_graph_from_current_results()
        self._generate_filtered_graph_from_filtered_results()
    
    def get_endurance_times(self, as_labels=False, frame_time=None, frame_unit=None):
        results = self.initial_results
        endurance_times = {}
        for bond in results:
            ts = results[bond]
            endurance_time = _np.diff(list(_hf.pairwise(_np.hstack(([0], _np.nonzero(_np.diff(ts))[0] + 1, [self.nb_frames])))), axis=1)
            if ts[0]: endurance_time = endurance_time[::2] 
            else: endurance_time = endurance_time[1::2]
            endurance_times[bond] = endurance_time.max()
        if as_labels: 
            if frame_time is not None:
                endurance_times = {key:_hf.unit_to_string(value*frame_time, frame_unit) for key, value in endurance_times.items()}
            else:
                endurance_times = {key:str(value) for key, value in endurance_times.items()}
        return endurance_times