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

import numpy as np
import copy
import MDAnalysis
from collections import defaultdict
import networkx as nx
import itertools
from PySide2.QtWidgets import QMessageBox

r_covalent = defaultdict(lambda: 1.5, N=1.31, O=1.31, P=1.58, S=1.55)
donor_names_global = {'OH2', 'OW', 'NE', 'NH1', 'NH2', 'ND2', 'SG', 'NE2', 'ND1', 'NZ', 'OG', 'OG1', 'NE1', 'OH', 'OE1', 'OE2', 'N16', 'OD1', 'OD2'}
acceptor_names_global = {'OH2', 'OW', 'OD1', 'OD2', 'SG', 'OE1', 'OE2', 'ND1', 'NE2', 'SD', 'OG', 'OG1', 'OH'}
aa_three2one = {'CYS': 'C', 'ASP': 'D', 'SER': 'S', 'GLN': 'Q', 'LYS': 'K', 'ILE': 'I', 'PRO': 'P', 'THR': 'T', 'PHE': 'F', 'ASN': 'N', 'GLY': 'G', 'HIS': 'H', 'LEU': 'L', 'ARG': 'R', 'TRP': 'W', 'ALA': 'A', 'VAL':'V', 'GLU': 'E', 'TYR': 'Y', 'MET': 'M', 'TIP3': 'O', 'HOH':'O', 'LYR':'RET', 'HSE':'H', 'HSD':'H', 'HSP':'H'}
water_definition = '(resname TIP3 and name OH2) or (resname HOH and name O)'

class Error(QMessageBox):
    
    def __init__(self, message='Undefined error!', informative=''):
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
        self.setInformativeText(informative)
        self.setWindowTitle("Error")
        self.exec_()
        
class Info(QMessageBox):
    
    def __init__(self, message='Empty Information!', informative='', title='Information'):
        super().__init__()
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setInformativeText(informative)
        self.setWindowTitle(title)
        self.exec_()

class EmptyGroup:
    def __init__(self):
        self.positions = np.array([])
        
    def __len__(self):
        return 0

class Cluster:
    def __init__(self, size=None, centers=None, leafs=None, max_bc=None, width=None):
        self.size = size
        self.leafs = leafs
        if (self.size is not None) and (self.leafs is not None): self.density = np.round(len(leafs)/size, 2)
        else: self.density = None
        self.centers = centers
        self.max_bc = max_bc
        self.width = width

class Selection:
    def __init__(self, mda_residue, donor_names, acceptor_names, add_donors_without_hydrogen, add_all_donor_acceptor=[]):

        self.donors = []
        self.donor_info = []
        self.acceptors = []
        self.acceptor_info = []
        self.hydrogens = []
        self.hydrogen_info = []
        self.donor2hydrogens = []
        if mda_residue:
            for atom in mda_residue.atoms:
                if (atom.name in donor_names) or (len(atom.name) > 1 and atom.name[0] in add_all_donor_acceptor):
                    if add_donors_without_hydrogen:
                        self.donors.append(atom)
                        self.donor_info.append(
                            str(atom.segid) + '-' + atom.resname + '-' + str(atom.resid) + '-' + atom.name)
                    else:
                        c = 0
                        for otheratom in atom.residue.atoms:
                            if (otheratom.name[0] == 'H' or otheratom.name[:2] in ['1H', '2H', '3H'] or otheratom.type == 'H') and np.sqrt(((atom.position - otheratom.position) ** 2).sum()) < r_covalent[atom.name[0]]:
                                self.hydrogens.append(otheratom)
                                self.hydrogen_info.append(str(otheratom.index))
                                c += 1
                        if c>0:    
                            self.donor2hydrogens.append(range(len(self.hydrogens) - c, len(self.hydrogens)))
                            self.donors.append(atom)
                            self.donor_info.append(
                                str(atom.segid) + '-' + atom.resname + '-' + str(atom.resid) + '-' + atom.name)
                if (atom.name in acceptor_names) or (len(atom.name) > 1 and atom.name[0] in add_all_donor_acceptor):
                    self.acceptors.append(atom)
                    self.acceptor_info.append(
                        str(atom.segid) + '-' + atom.resname + '-' + str(atom.resid) + '-' + atom.name)
            
            if self.donors: self.donors = MDAnalysis.core.groups.AtomGroup(self.donors)
            if self.acceptors: self.acceptors = MDAnalysis.core.groups.AtomGroup(self.acceptors)
            if self.hydrogens: self.hydrogens = MDAnalysis.core.groups.AtomGroup(self.hydrogens)
            self.count = len(self.donors) + len(self.acceptors)
            if not self.count>0: raise AssertionError('neither donors nor acceptors in the selection')

def angle(p1, p2, p3):
    """angle(p1,p2,p3) takes three numpy arrays of shape (N,3) as arguments.
    p1, p2 and p3 have to represent coordinates of the following form: 
        p1
       a  \
      -----p2---p3
    The returned array of shape (N,1) contains degree angles, representing 
    positive angles a between the lines p2--p3 and p1--p2 as indicated in the 
    above scheme.
    """
    v1s = p2 - p1
    v2s = p3 - p2
    
    dot_v1_v2 = np.einsum('ij,ij->i', v1s, v2s)
    dot_v1_v1 = np.einsum('ij,ij->i', v1s, v1s)
    dot_v2_v2 = np.einsum('ij,ij->i', v2s, v2s)
    cos_arg = dot_v1_v2/(np.sqrt(dot_v1_v1)*np.sqrt(dot_v2_v2))
    cos_arg[cos_arg<-1.0] = -1.0
    return np.rad2deg(np.arccos(cos_arg))


def MDA_info_list(group, detailed_info=False, special_naming=[]):
    result = []
    for atom in group:
        sid = str(atom.segid)
        rname = str(atom.resname)
        rid = str(atom.resid)
        if rname in special_naming:
            rname = str(atom.name)
        if detailed_info: result.append(sid + '-' + rname + '-' + rid + '-' + atom.name)
        else: result.append(sid + '-' + rname + '-' + rid)
    return result


def dict2graph(connections_dict, value_name='occupancy'):
    g = nx.Graph()
    edges = []
    for connection in connections_dict:
        node_a, node_b = connection.split(':')
        if value_name == 'wire_length':
            mean = connections_dict[connection][connections_dict[connection]!=np.inf].mean()
        elif value_name == 'occupancy':
            mean = connections_dict[connection].mean()
        else:
            raise AssertionError('Unknown edge attribute!')
        edges.append((node_a, node_b, {value_name:mean}))
    g.add_edges_from(edges)
    return g

    
def check_angle(atoms_in_distance, heavy2hydrogen, local_coordinates, hydrogen_coordinates, cut_angle):
    pairs = np.asarray(atoms_in_distance)
    angle_check_index = []
    a_index = []
    b_index = []
    hydrogen_index = []
    for i, (atom_a, atom_b) in enumerate(atoms_in_distance):
        temp_hydrogen = list(heavy2hydrogen[atom_a]) + list(heavy2hydrogen[atom_b])
        hydrogen_index += temp_hydrogen
        nb_hydrogen = len(temp_hydrogen)
        angle_check_index += [i]*nb_hydrogen
        a_index += [atom_a]*nb_hydrogen
        b_index += [atom_b]*nb_hydrogen
    temp_b = local_coordinates[b_index]
    temp_h = hydrogen_coordinates[hydrogen_index]
    temp_a = local_coordinates[a_index]
    
    angles = angle(temp_b, temp_h, temp_a)
    angle_check = angles <= cut_angle
    angle_check_index = np.array(angle_check_index)
    bond_index = np.asarray(angle_check_index[angle_check.flatten()], dtype=np.int)
    hbond_pairs = pairs[bond_index]
    return hbond_pairs  
    

def check_angle_water(atoms_in_distance, oxygen_coordinates, hydrogen_coordinates, cut_angle):
    pairs = np.asarray(atoms_in_distance)
    a_index = np.repeat(pairs[:,0], 4)
    b_index = np.repeat(pairs[:,1], 4)
    hydrogen_index = np.zeros(a_index.size, dtype=np.int)
    hydrogen_index[::4] = pairs[:,0] * 2
    hydrogen_index[1::4] = pairs[:,0] * 2 + 1
    hydrogen_index[2::4] = pairs[:,1] * 2
    hydrogen_index[3::4] = pairs[:,1] * 2 + 1    
    temp_b = oxygen_coordinates[b_index]
    temp_h = hydrogen_coordinates[hydrogen_index]
    temp_a = oxygen_coordinates[a_index]
    angles = angle(temp_b, temp_h, temp_a)
    angle_check = angles <= cut_angle
    bond_index = angle_check.reshape(-1,4).any(axis=1)
    hbond_pairs = pairs[bond_index]
    return hbond_pairs 

    
def intervals(timeseries):
    ts = np.array(timeseries)
    changes = np.nonzero(np.diff(ts))[0]+1
    changes = np.concatenate(([0],changes,[len(ts)]))
    intervals = [(changes[i],changes[i+1]-1) for i in range(len(changes)-1) if changes[i+1]-changes[i]>1]
    return intervals
    
def intervals_binary(timeseries):
    ts = np.array(timeseries, dtype=bool)
    if ts[0]:
        if ts[-1]: changes = np.concatenate(([0],np.nonzero(np.diff(ts))[0]+1,[ts.size]))
        else: changes = np.concatenate(([0],np.nonzero(np.diff(ts))[0]+1))
    else:
        if ts[-1]: changes = np.concatenate((np.nonzero(np.diff(ts))[0]+1,[ts.size]))
        else: changes = np.nonzero(np.diff(ts))[0]+1
    return changes.reshape((-1,2))

def block_analysis(dictionary, step_size, block_size, conv_cut):
    min_interval = range(0,int((len(dictionary[dictionary.keys()[0]])-block_size)/step_size), step_size)
    values = np.array(list(dictionary.values()), dtype=np.float)
    blockupancies = np.empty((values.shape[0],len(min_interval)))
    for ii,i in enumerate(min_interval):
        blockupancies[:,ii] = np.mean(values[:,i:i+block_size], axis=1)
    stds = np.std(blockupancies, axis=1)
    conv_index = stds < conv_cut
    result = dict(zip(np.array(dictionary.keys())[conv_index],np.array(dictionary.values())[conv_index]))
    return result


def filter_occupancy(dictionary, min_occupancy):
    for key in dictionary: 
        dtype = dictionary[key].dtype
        break
    if dtype == np.int: values = np.array(np.array(list(dictionary.values())) < np.inf, dtype=np.float)
    else: values = np.array(list(dictionary.values()), dtype=np.float)
    filter_index = values.mean(axis=1) > min_occupancy
    keys = [key for key in dictionary]
    values = [dictionary[key] for key in dictionary]
    result = dict(zip(np.array(keys)[filter_index],np.array(values)[filter_index]))
    return result
    

def pca_2d_projection(pos3d):
    m = pos3d.mean(axis=0)
    pos3dm = pos3d - m
    S = pos3dm.T.dot(pos3dm)
    try:
        eig_val, eig_vec = np.linalg.eigh(S)
        eig_val, eig_vec = eig_val[::-1][:2], eig_vec.T[::-1][:2]
        return eig_vec.dot(pos3dm.T).T, eig_vec
    except:
        return np.array([1.0,1.0]), np.array([[1.0,0,0],[0,1.0,0]])


def predecessor_recursive(d,pred,start,stop):
    if d==0: return pred[start,stop]
    else: return pred[start,predecessor_recursive(d-1,pred,start,stop)]
 
    
def predecessor_recursive_1d(d,pred,start):
    if d==0: return pred[start]
    else: return pred[predecessor_recursive_1d(d-1,pred,start)]
    

def complete_subgraphs(edges_matrix):
    edges_matrix = edges_matrix | np.eye(edges_matrix.shape[0], dtype=bool)
    subgraphs = np.zeros(edges_matrix.shape, dtype=bool)
    for i in range(edges_matrix.shape[0]):
        indices = edges_matrix[i].nonzero()[0]
        if indices.size < 2: continue
        check_matrix = edges_matrix[indices][:, indices]
        subgraphs[i][indices[check_matrix.all(axis=0)]] = True
    subgraphs = np.unique(subgraphs, axis=0)
    subgraphs = subgraphs[np.logical_not([((subgraphs * p) == p).all(axis=1).sum() > 1 for p in subgraphs])] 
    return subgraphs


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b) 


def connected_component_subgraph(graph, node):
    for component in nx.connected_component_subgraphs(graph):
        if node in component.nodes(): return component
    return None


def deconst_key(key, residuewise):
    a, b = key.split(':')
    if residuewise:
        segna, resna, resia = a.split('-')
        segnb, resnb, resib = b.split('-')
        
    else:
        segna, resna, resia, atomna = a.split('-')
        segnb, resnb, resib, atomnb = b.split('-')
    return segna, resna, int(resia), segnb, resnb, int(resib)


def remove_by_index(l, indices):
    for i,index in enumerate(indices):
        l.pop(index-i)
        
        
def points_in_slice(pt1, pt2, q):
    vec = pt2 - pt1
    return (np.dot(q - pt1, vec) >= 0) & (np.dot(q - pt2, vec) <= 0)
       
 
def points_in_cylinder(pt1, pt2, r, q):
    vec = pt2 - pt1
    const = r * np.linalg.norm(vec)
    return (np.dot(q - pt1, vec) >= 0) & (np.dot(q - pt2, vec) <= 0) & (np.linalg.norm(np.cross(q - pt1, vec), axis=1) <= const)  

def msd_fft_broadcast(r):
  N=len(r)
  F = np.fft.fft(r, n=2*N, axis=0)
  PSD = F * F.conjugate()
  res = np.fft.ifft(PSD, axis=0)
  res= (res[:N]).real
  n=np.arange(0,N)[::-1]+1
  S2 = (res/n.reshape(-1,1,1)).sum(-1)
  D=np.square(r).sum(-1) 
  D=np.vstack((D,np.zeros(D.shape[1])))
  Q=2*D.sum(0)
  S1=np.zeros((N,Q.size))
  for m in range(N):
      Q=Q-D[m-1]-D[N-m]
      S1[m]=Q/(N-m)
  return (S1-2*S2).mean(-1)

def msd_fft(r):
  N=len(r)
  F = np.fft.fft(r, n=2*N, axis=0)
  PSD = F * F.conjugate()
  res = np.fft.ifft(PSD, axis=0)
  res= (res[:N]).real
  n=np.arange(0,N)[::-1]+1
  S2 = (res/n.reshape(-1,1)).sum(-1)
  D=np.square(r).sum(-1) 
  D=np.append(D,0) 
  Q=2*D.sum(0)
  S1=np.zeros(N)
  for m in range(N):
      Q=Q-D[m-1]-D[N-m]
      S1[m]=Q/(N-m)
  return S1-2*S2

def invperm(p):
    q = np.empty_like(p)
    q[p] = np.arange(len(p))
    return q

def find_map(arr1, arr2):
    o1 = np.argsort(arr1)
    o2 = np.argsort(arr2)
    return o2[invperm(o1)]

def string_in_columns(s):
    lines = s.strip('\n').split('\n')
    elements = [line.split(' ') for line in lines]
    rotated_elements = np.array(elements, dtype=np.str).T
    return_string = '\n'.join(['\t'.join(rot_element) for rot_element in rotated_elements])
    return return_string

def histogram_to_string(data, mi=None, ma=None, nb_bins=10, labels=None):
    bins = np.linspace(mi, ma, nb_bins)
    save_string = 'occupancy ' + ' '.join(['{}-{}'.format(np.round(b1,2), np.round(b2,2)) for b1, b2 in pairwise(bins)]) + '\n'
    for i, values in enumerate(data):
        hist_data = np.histogram(values, bins=bins)[0]
        save_string += labels[i] + ' ' + ' '.join(['{}'.format(c) for c in hist_data]) + '\n'
    return string_in_columns(save_string)

def rgb_to_string(rgb):
    r,g,b,a = (np.array(rgb) * 255).astype(np.int)
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

def trans_angle(p1, p2, ax):
    label_pos = np.array((p1,p2)).sum(axis=0)/2
    x1, y1 = p1
    x2, y2 = p2
    angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
    if angle > 90:
        angle -= 180
    if angle < - 90:
        angle += 180
    trans_angle = ax.transData.transform_angles(np.array((angle,)), label_pos.reshape((1, 2)))[0]
    return trans_angle

def ranges_to_numbers(range_string):
    items_a = range_string.replace(' ','').split(',')
    numbers_a = []
    for item in items_a:
        item_split = item.split('-')
        if len(item_split)==2:
            numbers_a += list(range(int(item_split[0]), int(item_split[1])+1))
        elif len(item_split)==1:
            numbers_a += [int(item_split[0])]
    return numbers_a

def unit_to_seconds(value, unit):
    units = {'ms':1e-3,
             'mus':1e-6,
             'ns':1e-9,
             'ps':1e-12,
             'fs':1e-15,
             'as':1e-18}
    return value * units[unit]
    
def seconds_to_unit_string(seconds, only_unit=False):
    units = {'ms':1e-3,
             'mus':1e-6,
             'ns':1e-9,
             'ps':1e-12,
             'fs':1e-15,
             'as':1e-18}
    for name, unit in units.items():
        value = np.round(seconds/unit, 1)
        if float(value) == int(value): value = int(value)
        if 1000 > value >= 1:
            if only_unit: return name
            else: return '{}{}'.format(value, name)
            
def unit_to_string(value, unit, only_unit=False):
    return seconds_to_unit_string(unit_to_seconds(value, unit), only_unit=only_unit)

def get_segname(node):
    return node.split('-')[0]

def get_segnames(nodes):
    return [get_segname(node) for node in nodes]

def get_resname(node):
    return node.split('-')[1]

def get_resnames(nodes):
    return [get_resname(node) for node in nodes]

def get_resid(node):
    return int(node.split('-')[2])

def get_resids(nodes):
    return [get_resid(node) for node in nodes]

def sort_nodes(nodes):
    segnames = np.sort(np.unique(get_segnames(nodes)))
    nodes_per_segname = {segname:[] for segname in segnames}
    for node in nodes:
        for segname in segnames:
            if node.startswith(segname): 
                nodes_per_segname[segname].append(node)
                continue
    sor = []
    for segname in segnames:
        resids = get_resids(nodes_per_segname[segname])
        ind = np.argsort(resids)
        sor += [nodes_per_segname[segname][i] for i in ind]
    return sor

def biological_centrality_2(graph, normalize=False):
    centrality = {node:0.01 for node in graph}
    """
    trans_nodes = {node:i for i,node in enumerate(graph.nodes)}
    back_nodes = {i:node for i,node in enumerate(graph.nodes)}
    trans_graph = nx.Graph([(trans_nodes[n1], trans_nodes[n2]) for n1, n2 in graph.edges])
    
    all_paths = []
    longest = 0
    for source in trans_graph:
        seen, predecessors, sigma = single_source_shortest_paths(trans_graph, source)
        already_found = []
        all_current_paths = []
        while seen:
            target = seen.pop()
            if target in already_found: continue
            current_paths = predecessor_recursive_all_paths(predecessors, target)
            all_current_paths += current_paths
            already_found += deep_flatten_recursive(current_paths)
            if len(current_paths[0])>longest: longest = len(current_paths[0])
        all_paths += all_current_paths
    check_paths = np.ones((len(all_paths), longest), dtype=np.int)*-1
    for i, path in enumerate(all_paths): check_paths[i][:len(path)]=path
    for path in all_paths:
        if (np.in1d(path, check_paths).sum(axis=1) == len(path)).sum() > 1:
            try: 
                for node in path[1:-1]: 
                    centrality[back_nodes[node]] += 1
            except:
                pass
    if normalize: 
        ma = len(all_paths)
        for key in centrality:
            centrality[key] /= ma
    """
    return centrality

def biological_centrality(graph):
    centrality = {node:0 for node in graph}
    all_paths = []
    for source in graph:
        seen, predecessors, sigma = single_source_shortest_paths(graph, source)
        already_found = []
        all_current_paths = []
        while seen:
            target = seen.pop()
            if target in already_found: continue
            if any([((source in path) and (target in path)) for path in all_paths]): continue
            current_paths = predecessor_recursive_all_paths(predecessors, target)
            all_current_paths += current_paths
            already_found += deep_flatten_recursive(current_paths)
        #print(len(all_paths))
        all_paths = [path for path in all_paths if not is_sub_path(path, all_current_paths)]
        all_paths += all_current_paths
    for path in all_paths:
        for node in path[1:-1]: centrality[node] += 1
    ma = len(all_paths)
    return centrality, ma

def biological_centrality_3(graph, normalize=False):
    centrality = {node:0 for node in graph}
    all_paths = []
    for source in graph:
        seen, predecessors, sigma = single_source_shortest_paths(graph, source)
        already_found = []
        all_current_paths = []
        while seen:
            target = seen.pop()
            if target in already_found: continue
            if any([((source in path) and (target in path)) for path in all_paths]): continue
            current_paths = predecessor_recursive_all_paths(predecessors, target)
            all_current_paths += current_paths
            already_found += deep_flatten_recursive(current_paths)
        all_paths = [path for path in all_paths if not is_sub_path(path, all_current_paths)]
        all_paths += all_current_paths
    for path in all_paths:
        for node in path[1:-1]: centrality[node] += 1
    if normalize: 
        ma = len(all_paths)
        for key in centrality:
            centrality[key] /= ma
    return centrality


def single_source_shortest_paths(graph, source):
    sigma = {node:0.0 for node in graph}
    sigma[source] = 1.0
    predecessors = {node:[] for node in graph}
    distances = {source:0}
    seen = []
    Q = [source]
    while Q:
        v = Q.pop(0)
        seen.append(v)
        distance_v = distances[v]
        sigma_v = sigma[v]
        for w in graph[v]:
            if w not in distances:
                Q.append(w)
                distances[w] = distance_v + 1
            if distances[w] == distance_v + 1:
                sigma[w] += sigma_v
                predecessors[w].append(v) 
    return seen, predecessors, sigma

def flatten_recursive(S):
    if S == []:
        return S
    if isinstance(S[0][0], list):
        return flatten_recursive(S[0]) + flatten_recursive(S[1:])
    return S[:1] + flatten_recursive(S[1:])

def deep_flatten_recursive(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return deep_flatten_recursive(S[0]) + deep_flatten_recursive(S[1:])
    return S[:1] + deep_flatten_recursive(S[1:])

def predecessor_recursive_all_paths(predecessors, current):
    def rec(predecessors, current, paths=[]):
        preds = predecessors[current]
        if len(preds) == 0: 
            return paths + [current]
        elif len(preds) == 1:
            pred = preds[0]
            return rec(predecessors, pred, paths + [current])
        else:
            return [rec(predecessors, pred, paths + [current]) for pred in preds]
    paths = rec(predecessors, current)
    if not isinstance(paths[0], list): return [paths]
    elif not isinstance(paths[0][0], list): return paths
    else: return flatten_recursive(paths)
        
def is_sub_path(path, test_paths):
    return any([((path[0] in test_path) and (path[-1] in test_path)) for test_path in test_paths])

def adjust_water_positions(graph, pos):
    new_pos = copy.deepcopy(pos)
    for node in graph.nodes():
        resname = node.split('-')[1]
        if resname not in ['TIP3', 'HOH']: continue
        temp_pos = []
        for other_node in graph[node]:
            other_resname = other_node.split('-')[1]
            if other_resname in ['TIP3', 'HOH']: continue
            temp_pos.append(pos[other_node])
        if len(temp_pos) > 1:
            new_pos[node] = np.array(temp_pos).mean(axis=0)
        elif len(temp_pos) == 1:
            new_pos[node] = temp_pos[0] + 3.5 * (new_pos[node] - temp_pos[0]) / np.linalg.norm(new_pos[node] - temp_pos[0]) 
    return new_pos
                
def round_to_1(x):
    if x == 0.:
        return 0.
    elif x<1:
        return round(x, -int(np.floor(np.log10(abs(x)))))
    else:
        return np.round(x, 1)
    
def partition(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i : i+size]