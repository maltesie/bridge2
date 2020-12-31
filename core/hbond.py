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
from scipy import spatial as _sp

class HbondAnalysis(NetworkAnalysis):
    
    def __init__(self, selection=None, structure=None, trajectories=None, distance=3.5, cut_angle=60., 
                 start=None, stop=None, step=1, additional_donors=[], residuewise=False,
                 additional_acceptors=[], exclude_donors=[], exclude_acceptors=[], 
                 ions=[], check_angle=True, add_donors_without_hydrogen=False, 
                 add_all_donor_acceptor=False, progress_callback=None, 
                 water_definition=None, restore_filename=None):
        
        super(HbondAnalysis, self).__init__(selection=selection, structure=structure, trajectories=trajectories, 
             distance=distance, cut_angle=cut_angle, start=start, stop=stop, step=step, 
             additional_donors=additional_donors, additional_acceptors=additional_acceptors,
             exclude_donors=exclude_donors, exclude_acceptors=exclude_acceptors,
             ions=ions, check_angle=check_angle, add_donors_without_hydrogen=add_donors_without_hydrogen, 
             add_all_donor_acceptor=add_all_donor_acceptor, progress_callback=progress_callback,
             restore_filename=restore_filename, residuewise=residuewise, water_definition=water_definition)
        
        if restore_filename is not None: return
        self._i4_distribution = None
        self._i4_res3 = None
    
    def set_hbonds_in_selection(self):
        sfilter = _np.array([(ids.split('-')[3].startswith('S')) for ids in self._all_ids_atomwise])
        frame_count = 0
        frames = self.nb_frames
        result = {}
        for ts in self._universe.trajectory[self._trajectory_slice]:
            selection_coordinates = self._da_selection.positions
            d_tree = _sp.cKDTree(self._donors.positions)
            a_tree = _sp.cKDTree(self._acceptors.positions)
            hydrogen_coordinates = self._hydrogen.positions
    
            da_pairs = _np.array([[i, j] for i,donors in enumerate(a_tree.query_ball_tree(d_tree, self.distance)) for j in donors])
            da_pairs[:,0] += self._nb_donors
            da_pairs = da_pairs[_np.logical_not(_np.all(sfilter[da_pairs], axis=1))]

            if self.check_angle:
                all_coordinates = selection_coordinates
                local_hbonds = _hf.check_angle(da_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                local_hbonds = da_pairs
            
            sorted_bonds = _np.sort(local_hbonds)
            check = self._resids[sorted_bonds]
            check = check[:,0] < check[:,1]
            if self.residuewise: frame_res = [self._all_ids[i] + ':' + self._all_ids[j] if check[ii] else self._all_ids[j] + ':' + self._all_ids[i] for ii, (i, j) in enumerate(sorted_bonds)]
            else: frame_res = [self._all_ids_atomwise[i] + ':' + self._all_ids_atomwise[j] if check[ii] else self._all_ids_atomwise[j] + ':' + self._all_ids_atomwise[i] for ii, (i, j) in enumerate(sorted_bonds)]
            
            for bond in frame_res:
                if not self.check_angle:
                    a, b = bond.split(':')
                    if a.split('-')[:3] == b.split('-')[:3]: continue
                try:
                    result[bond][frame_count] = True
                except:
                    result[bond] = _np.zeros(frames, dtype=bool)
                    result[bond][frame_count] = True
            frame_count+=1
            if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds in frame {}/{}'.format(frame_count, self.nb_frames))
        self._set_results(result)

    def set_hbonds_only_water_in_convex_hull(self):
        result = {}
        frame_count = 0
        frames = self.nb_frames
        
        for ts in self._universe.trajectory[self._trajectory_slice]:
            water_coordinates = self._water.positions
            select_coordinates = self._da_selection.positions
            hydrogen_coordinates = self._hydrogen.positions[self._first_water_hydrogen_id:]
            
            hull = _sp.Delaunay(select_coordinates)
            local_index = (hull.find_simplex(water_coordinates) != -1).nonzero()[0]
    
            local_water_coordinates = water_coordinates[local_index]
            local_water_tree = _sp.cKDTree(local_water_coordinates)
            water_pairs = local_index[_np.array([pair for pair in local_water_tree.query_pairs(self.distance)])]
            
            if self.check_angle:
                local_hbonds = _hf.check_angle_water(water_pairs, water_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                local_hbonds = water_pairs
            
            sorted_bonds = _np.sort(local_hbonds)
            check = self._resids[sorted_bonds]
            check = check[:,0] < check[:,1]
            if self.residuewise: frame_res = [self._all_ids[i] + ':' + self._all_ids[j] if check[ii] else self._all_ids[j] + ':' + self._all_ids[i] for ii, (i, j) in enumerate(sorted_bonds)]
            else: frame_res = [self._all_ids_atomwise[i] + ':' + self._all_ids_atomwise[j] if check[ii] else self._all_ids_atomwise[j] + ':' + self._all_ids_atomwise[i] for ii, (i, j) in enumerate(sorted_bonds)]
            
            for bond in frame_res:
                if not self.check_angle:
                    a, b = bond.split(':')
                    if a.split('-')[:3] == b.split('-')[:3]: continue
                try:
                    result[bond][frame_count] = True
                except:
                    result[bond] = _np.zeros(frames, dtype=bool)
                    result[bond][frame_count] = True
            frame_count+=1
            if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds in frame {}/{}'.format(frame_count, self.nb_frames))
        self._set_results(result)  
    
    def set_hbonds_in_selection_and_water_in_convex_hull(self):
        sfilter = _np.array([(ids.split('-')[3].startswith('S')) for ids in self._all_ids_atomwise])        
        result = {}
        frame_count = 0
        frames = self.nb_frames
        for ts in self._universe.trajectory[self._trajectory_slice]:
            water_coordinates = self._water.positions
            select_coordinates = self._da_selection.positions
            hydrogen_coordinates = self._hydrogen.positions
            
            selection_tree = _sp.cKDTree(select_coordinates)
            if self._nb_acceptors > 0 and self._nb_donors > 0: 
                d_tree = _sp.cKDTree(self._donors.positions)
                a_tree = _sp.cKDTree(self._acceptors.positions)
                
            hull = _sp.Delaunay(select_coordinates)
            local_water_index = (hull.find_simplex(water_coordinates) != -1).nonzero()[0]
    
            local_water_coordinates = water_coordinates[local_water_index]
            local_water_tree = _sp.cKDTree(local_water_coordinates)
            
            local_pairs = [(i, local_water_index[j]+self._first_water_id) for i, bla in enumerate(selection_tree.query_ball_tree(local_water_tree, self.distance)) for j in bla]
            water_pairs = [(local_water_index[p[0]]+self._first_water_id, local_water_index[p[1]]+self._first_water_id) for p in local_water_tree.query_pairs(self.distance)]
            if self._nb_acceptors > 0 and self._nb_donors > 0: 
                da_pairs = _np.array([[i, j] for i,donors in enumerate(a_tree.query_ball_tree(d_tree, self.distance)) for j in donors])
                da_pairs[:,0] += self._nb_donors
                da_pairs = da_pairs[_np.logical_not(_np.all(sfilter[da_pairs], axis=1))]
            else: da_pairs = []
            
            if self.check_angle:
                all_coordinates = _np.vstack((select_coordinates, water_coordinates))
                hbonds = _hf.check_angle(list(da_pairs)+water_pairs+local_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                hbonds = list(da_pairs) + water_pairs + local_pairs
                
            sorted_bonds = _np.sort(hbonds)
            check = self._resids[sorted_bonds]
            check = check[:,0] < check[:,1]
            if self.residuewise: frame_res = [self._all_ids[i] + ':' + self._all_ids[j] if check[ii] else self._all_ids[j] + ':' + self._all_ids[i] for ii, (i, j) in enumerate(sorted_bonds)]
            else: frame_res = [self._all_ids_atomwise[i] + ':' + self._all_ids_atomwise[j] if check[ii] else self._all_ids_atomwise[j] + ':' + self._all_ids_atomwise[i] for ii, (i, j) in enumerate(sorted_bonds)]
            
            for bond in frame_res:
                if not self.check_angle:
                    a, b = bond.split(':')
                    if a.split('-')[:3] == b.split('-')[:3]: continue
                try:
                    result[bond][frame_count] = True
                except:
                    result[bond] = _np.zeros(frames, dtype=bool)
                    result[bond][frame_count] = True
            frame_count+=1
            if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds in frame {}/{}'.format(frame_count, self.nb_frames))
        self._set_results(result)
    
    def set_hbonds_in_selection_and_water_around(self, around_radius, not_water_water=False):
        sfilter = _np.array([(ids.split('-')[3].startswith('S')) for ids in self._all_ids_atomwise])
        result = {}
        frame_count = 0
        frames = self.nb_frames
        
        for ts in self._universe.trajectory[self._trajectory_slice]:
            
            water_coordinates = self._water.positions
            selection_coordinates = self._da_selection.positions
            
            selection_tree = _sp.cKDTree(selection_coordinates)
            if self._nb_acceptors > 0 and self._nb_donors > 0:
                d_tree = _sp.cKDTree(self._donors.positions)
                a_tree = _sp.cKDTree(self._acceptors.positions)
            hydrogen_coordinates = self._hydrogen.positions
    
            water_tree = _sp.cKDTree(water_coordinates, leafsize=32)
            local_water_index = []
            [local_water_index.extend(l) for l in water_tree.query_ball_point(selection_coordinates, float(around_radius))]
            local_water_index = _np.unique(local_water_index)
    
            local_water_coordinates = water_coordinates[local_water_index]
            local_water_tree = _sp.cKDTree(local_water_coordinates)
            
            local_pairs = [(i, local_water_index[j]+self._first_water_id) for i, bla in enumerate(selection_tree.query_ball_tree(local_water_tree, self.distance)) for j in bla]
            water_pairs = [(local_water_index[p[0]]+self._first_water_id, local_water_index[p[1]]+self._first_water_id) for p in local_water_tree.query_pairs(self.distance)]
            if self._nb_acceptors > 0 and self._nb_donors > 0: 
                da_pairs = _np.array([[i, j] for i,donors in enumerate(a_tree.query_ball_tree(d_tree, self.distance)) for j in donors])
                da_pairs[:,0] += self._nb_donors
            else: da_pairs = []
            if da_pairs != []: da_pairs = da_pairs[_np.logical_not(_np.all(sfilter[da_pairs], axis=1))]
            
            if self.check_angle:
                all_coordinates = _np.vstack((selection_coordinates, water_coordinates))
                if not_water_water: 
                    hbonds = _hf.check_angle(list(da_pairs)+local_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
                else:
                    hbonds = _hf.check_angle(list(da_pairs)+water_pairs+local_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                if not_water_water:
                    hbonds = list(da_pairs) + local_pairs
                else:
                    hbonds = list(da_pairs) + water_pairs + local_pairs
    
            hbonds = _np.array(hbonds)
            
            sorted_bonds = _np.sort(hbonds)
            check = self._resids[sorted_bonds]
            check = check[:,0] < check[:,1]
            if self.residuewise: frame_res = [self._all_ids[i] + ':' + self._all_ids[j] if check[ii] else self._all_ids[j] + ':' + self._all_ids[i] for ii, (i, j) in enumerate(sorted_bonds)]
            else: frame_res = [self._all_ids_atomwise[i] + ':' + self._all_ids_atomwise[j] if check[ii] else self._all_ids_atomwise[j] + ':' + self._all_ids_atomwise[i] for ii, (i, j) in enumerate(sorted_bonds)]
            
            for bond in frame_res:
                if not self.check_angle:
                    a, b = bond.split(':')
                    if a.split('-')[:3] == b.split('-')[:3]: continue
                try:
                    result[bond][frame_count] = True
                except:
                    result[bond] = _np.zeros(frames, dtype=bool)
                    result[bond][frame_count] = True
            frame_count+=1
            if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds in frame {}/{}'.format(frame_count, self.nb_frames))
        self._set_results(result)
    
    def add_disulphide_bridges_in_selection(self):
        frame_count = 0
        frames = self.nb_frames
        result = {}
        for ts in self._universe.trajectory[self._trajectory_slice]:
            selection_coordinates = self._da_selection.positions
            d_tree = _sp.cKDTree(self._donors.positions)
            a_tree = _sp.cKDTree(self._acceptors.positions)
            hydrogen_coordinates = self._hydrogen.positions
    
            da_pairs = _np.array([[i, j] for i,donors in enumerate(a_tree.query_ball_tree(d_tree, self.distance)) for j in donors])
            da_pairs[:,0] += self._nb_donors

            if self.check_angle:
                all_coordinates = selection_coordinates
                local_hbonds = _hf.check_angle(da_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                local_hbonds = da_pairs
            
            sorted_bonds = _np.sort(local_hbonds)
            check = self._resids[sorted_bonds]
            check = check[:,0] < check[:,1]
            if self.residuewise: frame_res = [self._all_ids[i] + ':' + self._all_ids[j] if check[ii] else self._all_ids[j] + ':' + self._all_ids[i] for ii, (i, j) in enumerate(sorted_bonds)]
            
            for bond in frame_res:
                if not self.check_angle:
                    a, b = bond.split(':')
                    if a.split('-')[:3] == b.split('-')[:3]: continue
                try:
                    result[bond][frame_count] = True
                except:
                    result[bond] = _np.zeros(frames, dtype=bool)
                    result[bond][frame_count] = True
            frame_count+=1
            if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds in frame {}/{}'.format(frame_count, self.nb_frames))
        self._set_results(result)
    
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