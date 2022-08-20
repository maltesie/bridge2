from . import helpfunctions as _hf
from .network import NetworkAnalysis
import numpy as _np
from scipy import spatial as _sp
import concurrent.futures
import time

class HbondAnalysis(NetworkAnalysis):
    
    def __init__(self, selection=None, structure=None, trajectories=None, distance=3.5, cut_angle=60., 
                 start=None, stop=None, step=1, additional_donors=[], residuewise=False,
                 additional_acceptors=[], exclude_donors=[], exclude_acceptors=[], 
                 ions=[], check_angle=True, add_donors_without_hydrogen=False, 
                 add_all_donor_acceptor=False, progress_callback=None, threads=2,
                 water_definition=None, restore_filename=None):
        
        super(HbondAnalysis, self).__init__(selection=selection, structure=structure, trajectories=trajectories, 
             distance=distance, cut_angle=cut_angle, start=start, stop=stop, step=step, 
             additional_donors=additional_donors, additional_acceptors=additional_acceptors,
             exclude_donors=exclude_donors, exclude_acceptors=exclude_acceptors,
             ions=ions, check_angle=check_angle, add_donors_without_hydrogen=add_donors_without_hydrogen, 
             add_all_donor_acceptor=add_all_donor_acceptor, progress_callback=progress_callback, threads=threads,
             restore_filename=restore_filename, residuewise=residuewise, water_definition=water_definition)
        
        if restore_filename is not None: return
        self._sfilter = _np.array([(ids.split('-')[3].startswith('S')) for ids in self._all_ids_atomwise])  
        self._i4_distribution = None
        self._i4_res3 = None

    def _set_thread_results(self, threads_results):
        result = {}
        for frame_count, local_hbonds in threads_results:
            sorted_bonds = _np.sort(local_hbonds)
            check = self._resids[sorted_bonds]
            check = check[:,0] < check[:,1]
            
            if self.residuewise: frame_res = [self._all_ids[i] + ':' + self._all_ids[j] if check[ii] else self._all_ids[j] + ':' + self._all_ids[i] for ii, (i, j) in enumerate(sorted_bonds)]
            else: frame_res = [self._all_ids_atomwise[i] + ':' + self._all_ids_atomwise[j] if check[ii] else self._all_ids_atomwise[j] + ':' + self._all_ids_atomwise[i] for ii, (i, j) in enumerate(sorted_bonds)]
            
            for bond in frame_res:
                a, b = bond.split(':')
                if self.residuewise and (a.split('-')[:3] == b.split('-')[:3]): continue
                try:
                    result[bond][frame_count] = True
                except:
                    result[bond] = _np.zeros(self.nb_frames, dtype=bool)
                    result[bond][frame_count] = True

        self._set_results(result)

    def _hbonds_in_selection_range(self, r):
        range_results = []
        for ts in r:
            self._universe.trajectory[ts]
            selection_coordinates = self._da_selection.positions
            d_tree = _sp.cKDTree(self._donors.positions)
            a_tree = _sp.cKDTree(self._acceptors.positions)
            hydrogen_coordinates = self._hydrogen.positions
    
            da_pairs = _np.array([[i, j] for i,donors in enumerate(a_tree.query_ball_tree(d_tree, self.distance)) for j in donors])
            da_pairs[:,0] += self._nb_donors
            da_pairs = da_pairs[_np.logical_not(_np.all(self._sfilter[da_pairs], axis=1))]

            if self.check_angle:
                all_coordinates = selection_coordinates
                local_hbonds = _hf.check_angle(da_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                local_hbonds = da_pairs
            
            range_results.append((ts, local_hbonds))
        return range_results
    
    def set_hbonds_in_selection(self):
        if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds...')
        #t0 = time.time()
        threads_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._threads) as executor:
            for r in _hf.partition(range(self.nb_frames), max(10, int(self.nb_frames/(self._threads-1)))):
                threads_results += executor.submit(self._hbonds_in_selection_range, r).result()
        
        #print('Time to compute kdtrees: {}s'.format(_np.round(time.time()-t0,5)))
        self._set_thread_results(threads_results)
        
    def _hbonds_only_water_in_convex_hull(self, r):
        range_results = []
        for ts in r:
            self._universe.trajectory[ts]
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
            range_results.append((ts, local_hbonds))
        return range_results

    def set_hbonds_only_water_in_convex_hull(self):
        if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds...')
    
        threads_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._threads) as executor:
            for r in _hf.partition(range(self.nb_frames), max(10, int(self.nb_frames/(self._threads-1)))):
                threads_results += executor.submit(self._hbonds_only_water_in_convex_hull, r).result()

        self._set_thread_results(threads_results)
    
    def _hbonds_in_selection_and_water_in_convex_hull_range(self, r):
        range_results = []
        for ts in r:
            self._universe.trajectory[ts]
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
                da_pairs = da_pairs[_np.logical_not(_np.all(self._sfilter[da_pairs], axis=1))]
            else: da_pairs = []
            
            if self.check_angle:
                all_coordinates = _np.vstack((select_coordinates, water_coordinates))
                hbonds = _hf.check_angle(list(da_pairs)+water_pairs+local_pairs, self.heavy2hydrogen, all_coordinates, hydrogen_coordinates, self.cut_angle)
            else:
                hbonds = list(da_pairs) + water_pairs + local_pairs
            range_results.append((ts, hbonds))
        return range_results

    def set_hbonds_in_selection_and_water_in_convex_hull(self):
        if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds...')
        
        threads_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._threads) as executor:
            for r in _hf.partition(range(self.nb_frames), max(10, int(self.nb_frames/(self._threads-1)))):
                threads_results += executor.submit(self._hbonds_in_selection_and_water_in_convex_hull_range, r).result()
                
        self._set_thread_results(threads_results)
    
    def _hbonds_in_selection_and_water_around_range(self, r, around_radius, not_water_water):
        range_results = []
        for ts in r:
            self._universe.trajectory[ts]
            
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
            if da_pairs != []: da_pairs = da_pairs[_np.logical_not(_np.all(self._sfilter[da_pairs], axis=1))]
            
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
            range_results.append((ts, hbonds))
        return range_results

    def set_hbonds_in_selection_and_water_around(self, around_radius, not_water_water=False):
        if self.progress_callback is not None: self.progress_callback.emit('Computing H bonds...')
        
        threads_results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self._threads) as executor:
            for r in _hf.partition(range(self.nb_frames), max(10, int(self.nb_frames/(self._threads-1)))):
                threads_results += executor.submit(self._hbonds_in_selection_and_water_around_range, r, around_radius, not_water_water).result()
                
        self._set_thread_results(threads_results)
        
    
    def add_disulphide_bridges_in_selection(self):
        frame_count = 0
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
                a, b = bond.split(':')
                if a == b: continue
                try:
                    result[bond][frame_count] = True
                except:
                    result[bond] = _np.zeros(self.nb_frames, dtype=bool)
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