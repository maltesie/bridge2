# -*- coding: utf-8 -*-

import matplotlib as mpl
mpl.rcParams['path.simplify'] = True
mpl.rcParams['path.simplify_threshold'] = 1.0

import networkx as nx
import numpy as np
from collections import defaultdict
from matplotlib.colors import is_color_like
import matplotlib.pyplot as plt
from core.helpfunctions import rgb_to_string, trans_angle

from matplotlib.backends.qt_compat import QtCore
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT)
else:
    from matplotlib.backends.backend_qt4agg import (FigureCanvas, NavigationToolbar2QT)
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from core.helpfunctions import Error

default_colors = ['seagreen', 'red', 'blue', 'yellow', 'grey', 'lightblue', 'orange', 'maroon', 'olive', 'skyblue', 'pink', 'silver', 'peru', 'fuchsia', 'lavender']

class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2QT.toolitems if t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

class InteractiveMPLGraph:
    
    def __init__(self, parent):
        
        self.fig = Figure(dpi=170)
        self.canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.cax = None
        self.selected_nodes = []
        self._node = {}
        self._adj = {}
        self._current_node = None
        self._current_node_handle = None
        self._parent = parent
        self._analysis = parent.analysis
        self._canvas_toolbar = None
        self._default_size = {}
        
        node_positions = self._analysis.get_current_node_positions()
        if node_positions is None: node_positions = self._analysis.get_node_positions_2d()
        node_labels = self._analysis.get_short_node_labels()
        edge_labels_occupancy = {(key.split(':')[0], key.split(':')[1]):value for key, value in self._analysis.get_occupancies(as_labels=True).items()}
        frame_time, frame_unit = self._parent._search_parameter['frame_time']
        edge_labels_endurance = {(key.split(':')[0], key.split(':')[1]):value for key, value in self._analysis.get_endurance_times(as_labels=True, frame_time=frame_time, frame_unit=frame_unit).items()}
        if self._parent._analysis_type == 'ww': edge_labels_nb_water = {(key.split(':')[0], key.split(':')[1]):value for key, value in self._analysis.get_nb_waters(as_labels=True).items()}
        graph = self._analysis.initial_graph
        f = 0.55
        len2fontsize = defaultdict(lambda: 6*f, {2:11*f, 3:11*f, 4:11*f, 5:11*f, 6:10*f, 7:9*f, 8:8*f, 9:7*f, 10:7*f})
        
        for node in graph.nodes:
            label_length = len(node_labels[node])
            if not self._analysis.residuewise: label_length -= 1
            subgraph = graph.subgraph([node])
            label = nx.draw_networkx_labels(subgraph, node_positions, labels={node:node_labels[node]}, 
                                    font_weight='bold', font_size=len2fontsize[label_length], ax=self.ax)[node]
            handle = nx.draw_networkx_nodes(subgraph, node_positions, node_color=default_colors[0], alpha=0.5, ax=self.ax)

            self._node[node] = {'handle':handle, 'label':label, 'active':True, 'color':default_colors[0]}
            self._default_size['node'] = (handle.get_sizes()[0], len2fontsize[label_length])
            self._adj[node] = {}
            
        
        for u, v in graph.edges:
            subgraph = graph.subgraph([u, v])
            direction = list(subgraph.edges)[0]
            handle = nx.draw_networkx_edges(subgraph, node_positions, width=1.0, alpha=0.5, ax=self.ax)
            self._default_size['edge'] = handle.get_linewidth()
            segments = handle.get_segments()
            ta = trans_angle(segments[0][0], segments[0][1], self.ax)
            try: edge_label = {direction:edge_labels_occupancy[(u,v)]}
            except KeyError: edge_label = {direction:edge_labels_occupancy[(v,u)]}
            edge_label_occupancy = nx.draw_networkx_edge_labels(subgraph, node_positions, edge_labels=edge_label,
                                                 font_weight='bold', font_size=len2fontsize[6],
                                                 ax=self.ax)[direction]
            edge_label_occupancy.set_visible(False)
            edge_label_occupancy.set_rotation(ta)
            self._default_size['label'] = edge_label_occupancy.get_fontsize()
            
            try: edge_label = {direction:edge_labels_endurance[(u,v)]}
            except KeyError: edge_label = {direction:edge_labels_endurance[(v,u)]}
            edge_label_endurance = nx.draw_networkx_edge_labels(subgraph, node_positions, edge_labels=edge_label,
                                                 font_weight='bold', font_size=len2fontsize[6],
                                                 ax=self.ax)[direction]
            edge_label_endurance.set_visible(False)
            edge_label_endurance.set_rotation(ta)
            
            if self._parent._analysis_type == 'ww': 
                try: edge_label = {direction:edge_labels_nb_water[(u,v)]}
                except KeyError: edge_label = {direction:edge_labels_nb_water[(v,u)]}
                edge_label_water = nx.draw_networkx_edge_labels(subgraph, node_positions, edge_labels=edge_label,
                                                     font_weight='bold', font_size=len2fontsize[6],
                                                     ax=self.ax)[direction]
                edge_label_water.set_visible(False)
                edge_label_water.set_rotation(ta)
            
                edge_data = {'handle':handle, 'direction':direction, 'active':True, 'color':'black', 'all_labels':{'occupancy':edge_label_occupancy, 
                                                                                                                 'endurance':edge_label_endurance, 
                                                                                                                 'nb_water':edge_label_water}}
            else:
                edge_data = {'handle':handle, 'direction':direction, 'active':True, 'color':'black', 'all_labels':{'occupancy':edge_label_occupancy, 
                                                                                                                 'endurance':edge_label_endurance}}
            
            self._adj[u][v] = edge_data
            self._adj[v][u] = edge_data
            
        
        self.fig.tight_layout()
        self.cax = self.fig.add_axes([0.73, 0.1, 0.2, 0.01])
        self.cax.axis('off')
        
        self._cidpress = self.fig.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self._cidrelease = self.fig.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self._cidmotion = self.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
        
    def on_press(self, event):
        if event.inaxes != self.ax: return
        if (self._canvas_toolbar is None) or (self._canvas_toolbar.mode != ""): return
        if self._current_node is not None: return

        clicked_on_node = False
        for node in self._node:
            if not self._node[node]['active']: continue
            node_handle = self._node[node]['handle']
            contains, attrd = node_handle.contains(event)
            if contains: 
                clicked_on_node = True
                break
        if not clicked_on_node: return

        self.moved = False
        x0, y0 = node_handle.get_offsets()[0]
        self.press = x0, y0, event.xdata, event.ydata
        self._current_node_handle = node_handle
        self._current_node = node

        node_handle.set_animated(True)
        label = self._node[node]['label']
        label.set_animated(True)
        for other_node in self._adj[node]: 
            other_node_handle = self._node[other_node]['handle']
            edge = self._adj[node][other_node]['handle']
            edge.set_animated(True)
            for label_type in self._adj[node][other_node]['all_labels']:
                label = self._adj[node][other_node]['all_labels'][label_type]
                label.set_animated(True)
            other_node_handle.set_animated(True)
        
        self.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)

        for other_node in self._adj[node]: 
            other_node_handle = self._node[other_node]['handle']
            edge = self._adj[node][other_node]['handle']
            self.ax.draw_artist(edge)
            self.ax.draw_artist(other_node_handle)
        self.ax.draw_artist(node_handle)
        self.ax.draw_artist(label)

        self.canvas.blit(self.ax.bbox)
    
    def on_motion(self, event):
        if self._current_node is None: return
        if event.inaxes != self.ax: return
        node = self._current_node
        node_handle = self._current_node_handle
        self.moved = True
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        
        node_handle.set_offsets([x0+dx, y0+dy])
        
        for other_node in self._adj[node]: 
            edge = self._adj[node][other_node]['handle']
            direction = self._adj[node][other_node]['direction']
            segments = edge.get_segments()
            index = direction.index(node)
            segments[0][index] = [x0+dx, y0+dy]
            edge.set_segments(segments)
            label_pos = np.array(segments[0]).sum(axis=0)/2
            ta = trans_angle(segments[0][0], segments[0][1], self.ax)
            for label_type in self._adj[node][other_node]['all_labels']:
                edge_label = self._adj[node][other_node]['all_labels'][label_type]
                edge_label.set_position(label_pos)
                edge_label.set_rotation(ta)
        
        label = self._node[node]['label']
        label.set_position([x0+dx, y0+dy])
        
        self.canvas.restore_region(self.background)
        
        for other_node in self._adj[node]: 
            other_node_handle = self._node[other_node]['handle']
            edge = self._adj[node][other_node]['handle']
            for label_type in self._adj[node][other_node]['all_labels']:
                edge_label = self._adj[node][other_node]['all_labels'][label_type]
                self.ax.draw_artist(edge_label)
            self.ax.draw_artist(edge)
            self.ax.draw_artist(other_node_handle)
        self.ax.draw_artist(node_handle)
        self.ax.draw_artist(label)
        
        self.canvas.blit(self.ax.bbox)
    
    def on_release(self, event):
        if self._current_node is None: return
        node_handle = self._current_node_handle
        node = self._current_node
        label = self._node[node]['label']
        
        if not self.moved:
            if node in self.selected_nodes:
                self.selected_nodes.remove(node)
                node_handle.set_linewidth(1.0)
                node_handle.set_edgecolor(self._node[node]['color'])
            else:
                self.selected_nodes.append(node)
                self._parent.statusbar.showMessage(self.get_current_node_info())
            self.process_selected_nodes()
            self.ax.draw_artist(node_handle)
            self.canvas.blit(self.ax.bbox)
        
        node_handle.set_animated(False)
        label.set_animated(False)
        for other_node in self._adj[node]: 
            other_node_handle = self._node[other_node]['handle']
            edge = self._adj[node][other_node]['handle']
            for label_type in self._adj[node][other_node]['all_labels']:
                edge_label = self._adj[node][other_node]['all_labels'][label_type]
                edge_label.set_animated(False)
            edge.set_animated(False)
            other_node_handle.set_animated(False)
        
        self.background = None
        self.canvas.draw_idle()
        self.press = None
        self._current_node = None
    
    def edges(self):
        seen = {}
        for node, neighbours in self._adj.items():
            for neighbor, data in neighbours.items():
                if neighbor not in seen:
                    yield (node, neighbor, data)
            seen[node] = True
        del seen
        
    def nodes(self):
        for node in self._node:
            yield node
    
    def get_current_node_info(self):
        return self._current_node
    
    def reset_selected_nodes(self):
        self.selected_nodes = []
        for node in self._node:
            node_handle = self._node[node]['handle']
            node_handle.set_linewidth(1.0)
            node_handle.set_edgecolor(self._node[node]['color'])
        self.canvas.draw_idle()
    
    def process_selected_nodes(self):
        focus_widget = self._parent.focusWidget()
        
        if focus_widget is self._parent.line_bonds_connected_root:
            self._parent.line_bonds_connected_root.setText(self._current_node)
        elif focus_widget is self._parent.line_bonds_path_root:
            self._parent.line_bonds_path_root.setText(self._current_node)
        elif focus_widget is self._parent.line_bonds_path_goal:
            self._parent.line_bonds_path_goal.setText(self._current_node)
        elif focus_widget is self._parent.lineEdit_specific_path:
            self._parent.lineEdit_specific_path.setText(', '.join(self.selected_nodes))
          
        current_plugin = self._parent.comboBox_plugins.currentText()    
        plugin_ui = self._parent._plugins[current_plugin].ui
        plugin_lineEdits = [getattr(plugin_ui, lineEdit) for lineEdit in ['lineEdit_node_picker'+str(i) for i in range(1,4)] if hasattr(plugin_ui, lineEdit)]
        for lineEdit in plugin_lineEdits:
            if focus_widget is lineEdit:
                lineEdit.setText(self._current_node)
            
        rem_nodes = []
        for node in self.selected_nodes:
            node_handle = self._node[node]['handle']
            if node not in self._analysis.filtered_graph.nodes:
                rem_nodes.append(node)
                node_handle.set_linewidth(1.0)
                node_handle.set_edgecolor(self._node[node]['color'])
            node_handle.set_linewidth(2.0)
            node_handle.set_edgecolor('black')
        for node in rem_nodes: self.selected_nodes.remove(node)
    
    def set_edge_color(self):
        for node, other_node, edge_data in self.edges():
            edge_handle = edge_data['handle']
            edge_handle.set_facecolor(edge_data['color'])
            edge_handle.set_edgecolor(edge_data['color'])
        self.canvas.draw_idle()

    def set_subgraph(self, **kwargs):
        subgraph = self._analysis.filtered_graph
        node_labels_active = self._parent.checkBox_bonds_graph_labels.isChecked()
        for node in self._node:
            if node in subgraph.nodes:
                self._node[node]['active'] = True
                node_handle = self._node[node]['handle']
                node_handle.set_visible(True)
                label = self._node[node]['label']
                if node_labels_active: label.set_visible(True)
                else: label.set_visible(False)
            else:
                self._node[node]['active'] = False
                node_handle = self._node[node]['handle']
                node_handle.set_visible(False)
                label = self._node[node]['label']
                label.set_visible(False)
        for node, other_node, edge_data in self.edges():
            edge_handle = edge_data['handle']
            for edge_label_type, edge_label in edge_data['all_labels'].items():
                if (node, other_node) in subgraph.edges:
                    edge_handle.set_visible(True)
                    edge_data['active'] = True
                else:
                    edge_handle.set_visible(False)
                    edge_label.set_visible(False)
                    edge_data['active'] = False
        self.set_edge_labels(draw=False)
        if ('draw' not in kwargs) or kwargs['draw']: self.canvas.draw_idle()
            
    def set_colors(self, **kwargs):
        if self.ax.get_legend() is not None: 
            self.ax.get_legend().remove()
        if self.cax is not None:
            self.cax.clear()
            self.cax.axis('off')
        
        if self._parent.radioButton_color.isChecked():
            color = self._parent.comboBox_single_color.currentText()
            if color == '': color = default_colors[0]
            if not is_color_like(color): 
                Error('Color Error'+' '*30, "Did not understand color definition '{}'. You can use strings like green or shorthands like g or RGB codes like #15b01a.".format(color))
                return
            for node in self._node: self._node[node]['color'] = color
        
        elif self._parent.radioButton_colors.isChecked():
            for node in self._node: 
                segname = node.split('-')[0]
                color = self._parent._segname_colors[segname]
                if not is_color_like(color): 
                    Error('Color Error'+' '*30, "Did not understand color definition '{}'. You can use strings like green or shorthands like g or RGB codes like #15b01a.".format(color))
                    return
                self._node[node]['color'] = color
            if self._parent.checkBox_segnames_legend.isChecked():
                custom_lines = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, alpha=0.6, markersize=12, lw=4) for color in self._parent._segname_colors.values()]
                segnames = [segname for segname in self._parent._segname_colors.keys()]
                self.ax.legend(custom_lines, segnames)
        
        elif self._parent.radioButton_degree.isChecked() or self._parent.radioButton_betweenness.isChecked():
            avg_type = True
            norm_type =  self._parent.checkBox_centralities_norm.isChecked()
            if self._parent.radioButton_degree.isChecked(): centralities = self._analysis.centralities['degree'][avg_type][norm_type]
            elif self._parent.radioButton_betweenness.isChecked(): centralities = self._analysis.centralities['betweenness'][avg_type][norm_type]
            
            max_centrality = sorted(centralities.values())[-1]
            if self._parent.radioButton_degree.isChecked() and (not (avg_type or norm_type)): max_centrality = round(max_centrality)
            cmap = plt.get_cmap('jet')
            for node in centralities:
                centrality_value = centralities[node]
                self._node[node]['color'] = rgb_to_string(cmap(centrality_value/max_centrality))
            if self._parent.checkBox_color_legend.isChecked():
                sm = plt.cm.ScalarMappable(cmap=cmap)
                sm.set_array([0.0, max_centrality])
                plt.colorbar(sm, cax=self.cax, ticks=[0, max_centrality], orientation='horizontal')
                self.cax.set_xticklabels([str(0), str(max_centrality)])
                self.cax.axis('on')
        
        for node in self._node:
            node_handle = self._node[node]['handle']
            color = self._node[node]['color']
            if not self._parent.checkBox_white.isChecked(): node_handle.set_facecolor(color)
            else: node_handle.set_facecolor('white')
            node_handle.set_edgecolor(color)
        if ('draw' not in kwargs) or kwargs['draw']: self.canvas.draw_idle()
    
    def set_node_positions(self, **kwargs):
        projection = 'PCA'
        if self._parent.radioButton_rotation_xy.isChecked(): projection = 'XY'
        elif self._parent.radioButton_rotation_zy.isChecked(): projection = 'ZY'
        adjust_water = False
        frame = self._parent.horizontalSlider_frame.value()
        positions = self._parent.analysis.get_node_positions_2d(projection=projection, in_frame=frame, adjust_water_positions=adjust_water)
        
        all_pos = np.array([positions[key] for key in positions])
        minx, maxx, miny, maxy = np.min(all_pos[:,0]), np.max(all_pos[:,0]), np.min(all_pos[:,1]), np.max(all_pos[:,1])
        xmargin = (maxx-minx)/20
        ymargin = (maxy-miny)/20
        for node in self._node:
            node_handle = self._node[node]['handle']
            node_handle.set_offsets(positions[node])
            node_label = self._node[node]['label']
            node_label.set_position(positions[node])
            
        for node, other_node, edge_data in self.edges():
            edge = edge_data['handle']
            direction = edge_data['direction']
            index = direction.index(node)
            other_index = direction.index(other_node)
            edge_positions = np.array([positions[node], positions[other_node]])[[index,other_index]]
            edge.set_segments([edge_positions])
            label_pos = np.array(edge_positions).sum(axis=0)/2
            ta = trans_angle(edge_positions[0], edge_positions[1], self.ax)
            for label_type in edge_data['all_labels']:
                edge_label = edge_data['all_labels'][label_type]
                edge_label.set_position(label_pos)
                edge_label.set_rotation(ta)
            
        self.ax.set_xlim(minx-xmargin, maxx+xmargin)
        self.ax.set_ylim(miny-ymargin, maxy+ymargin)
        if ('draw' not in kwargs): self.canvas.draw_idle()
    
    def set_nodesize(self, **kwargs):
        for node in self._node:
            offset = self._default_size['node'][0]/2
            size = offset + 2/(self._default_size['node'][0]) * (self._parent.horizontalSlider_nodes.value()/100*self._default_size['node'][0])**2
            node_handle = self._node[node]['handle']
            node_handle.set_sizes([size])
            offset = self._default_size['node'][1]/2
            size = offset + self._parent.horizontalSlider_nodes.value()/100*self._default_size['node'][1]
            label_handle = self._node[node]['label']
            label_handle.set_size(size)
        if ('draw' not in kwargs) or kwargs['draw']: self.canvas.draw_idle()
        
    def set_edgesize(self, **kwargs):
        for node, other_node, edge_data in self.edges():
            offset = self._default_size['edge'] / 2
            size = offset + self._default_size['edge'] * (self._parent.horizontalSlider_edges.value()/100)
            edge_data['handle'].set_linewidth(size)
        if ('draw' not in kwargs) or kwargs['draw']: self.canvas.draw_idle()
        
    def set_labelsize(self, **kwargs):
        for node, other_node, edge_data in self.edges():
            offset = self._default_size['label'] / 2
            size = offset + self._default_size['label'] * (self._parent.horizontalSlider_labels.value()/100)
            for typ, label_handle in edge_data['all_labels'].items():
                label_handle.set_fontsize(size)
        if ('draw' not in kwargs) or kwargs['draw']: self.canvas.draw_idle()
    
    def set_node_labels(self, **kwargs):
        labels_active = self._parent.checkBox_bonds_graph_labels.isChecked()
        for node in self._node:
            show_label = self._node[node]['active']
            label = self._node[node]['label']
            if labels_active and show_label: label.set_visible(True)
            else: label.set_visible(False)
        if ('draw' not in kwargs) or kwargs['draw']: self.canvas.draw_idle()
        
    def set_edge_labels(self, **kwargs):
        if self._parent.checkBox_bonds_occupancy.isChecked(): active_label_type = 'occupancy'
        elif self._parent.checkBox_bonds_endurance.isChecked(): active_label_type = 'endurance'
        elif self._parent.checkBox_nb_water.isChecked(): active_label_type = 'nb_water'
        else: active_label_type = None
        for node, other_node, edge_data in self.edges():
            show_label = edge_data['active']
            labels = edge_data['all_labels']
            for label_type in labels:
                label = labels[label_type]
                if (label_type == active_label_type) and show_label: 
                    label.set_visible(True)
                else: 
                    label.set_visible(False)
        if ('draw' not in kwargs) or kwargs['draw']: self.canvas.draw_idle()
    
    def get_active_nodes(self):
        return [node for node in self._node if self._node[node]['active']]
            
    def set_current_pos(self):
        node_pos = {}
        for node in self._node:
            node_handle = self._node[node]['handle']
            x, y = node_handle.get_offsets()[0]
            node_pos[node] = (x,y)
        self._analysis._current_node_positions = node_pos
    
    def add_toolbar(self):
        self._canvas_toolbar = NavigationToolbar(self.canvas, self._parent)
        self._canvas_toolbar.home = self.set_node_positions
        self._parent.addToolBar(self._canvas_toolbar)
        
    def remove_toolbar(self):
        self._parent.removeToolBar(self._canvas_toolbar)
        
    def _disconnect(self):
        'disconnect all the stored connection ids'
        self.canvas.mpl_disconnect(self.cidpress)
        self.canvas.mpl_disconnect(self.cidrelease)
        self.canvas.mpl_disconnect(self.cidmotion)
        
