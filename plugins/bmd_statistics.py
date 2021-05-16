# -*- coding: utf-8 -*-

from PySide2.QtCore import (QCoreApplication, QMetaObject, Qt, QSize)
from PySide2.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QFileDialog,
     QCheckBox, QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, QRadioButton)

from core.helpfunctions import (Error, get_segnames, get_resids, rgb_to_string, 
     histogram_to_string, string_in_columns)
from core.drawing import (histogram, multi_histogram, boolean_scatter, timeseries,
                          multi_timeseries, heatmap)
from itertools import combinations
import numpy as np
import matplotlib as mpl

#Necessary attributes:
main_window = None #stores the pointer to the main window passed to the load routine
plugin_widget = None #stores the QtWidget that will be displayed in the Computations tab
title = 'MD Statistics' #Title of the plugin that will be displayed in the combobox

ui = None
segname_colors = None

#necessary function to initialize the QtWidget
def load(parent):
    global plugin_widget, main_window, ui
    main_window = parent
    plugin_widget = QGroupBox()
    plugin_widget.setTitle('')
    ui = Ui_GroupBox()
    ui.setupUi(plugin_widget)
    ui.pushButton_plot_occupancy.clicked.connect(plot_occupancy)
    ui.pushButton_save_occupancy.clicked.connect(save_occupancy)
    ui.pushButton_plot_jo.clicked.connect(plot_jo)
    ui.pushButton_save_jo.clicked.connect(save_jo)
    ui.pushButton_plot_timeseries.clicked.connect(plot_timeseries)
    ui.pushButton_save_timeseries.clicked.connect(save_timeseries)
    ui.checkBox_color_segments_occupancy.clicked.connect(toggle_stacked)

#Necessary function that is called when the plugin is selected in the combobox.
def update(parent):
    global main_window, segname_colors
    main_window = parent
    if main_window.analysis is not None: segname_colors = main_window._segname_colors
    if main_window._analysis_type == 'ww': 
        ui.groupBox_joint_occupancy.setTitle('Joint Occupancy of Water Wires')
        ui.groupBox_nb_connections.setTitle('Time series of Sum of Water Wires')
    elif main_window._analysis_type == 'hb': 
        ui.groupBox_joint_occupancy.setTitle('Joint Occupancy of H Bonds')
        ui.groupBox_nb_connections.setTitle('Time series of Sum of H Bonds')

def toggle_stacked():
    ui.checkBox_stacked_histogram.setEnabled(ui.checkBox_color_segments_occupancy.isChecked())

def compute_occupancy():
    if segname_colors is None: return None, None, None, None

    try:
        nb_bins = int(ui.lineEdit_bins.text()) + 1
    except:
        Error('Format Error', 'Please enter an integer as number of bins.')
        return
    try:
        mi, ma = float(ui.lineEdit_minimum.text()), float(ui.lineEdit_maximum.text())
        if not (0<=mi<1.0 and 0<ma<=1.0): raise AssertionError('min/max')
    except:
        Error('Format Error', 'Minimum and maximum occupancy have to be floats between 0 and 1.')
        return
    
    count = {(segname,segname):[] for segname in segname_colors}
    count.update({tuple(sorted(combination)):[] for combination in combinations(segname_colors.keys(), 2)})
    graph = main_window.analysis.filtered_graph
    for edge in graph.edges():
        segn_a, segn_b = get_segnames(edge)
        d = graph.get_edge_data(*edge)
        count[tuple(sorted((segn_a, segn_b)))].append(d['occupancy'])
    return nb_bins, mi, ma, count
    
def plot_occupancy():
    nb_bins, mi, ma, count = compute_occupancy()
    if nb_bins is None: return
    color_by_segment = ui.checkBox_color_segments_occupancy.isChecked()
    cumulative = ui.checkBox_cumulative_histogram.isChecked()
    if cumulative: cumulative = -1
    if not color_by_segment: 
        one_count = []
        for key, value in count.items():
            one_count += value
        histogram(one_count, mi=mi, ma=ma, nb_bins=nb_bins, xlabel='Occupancy', cumulative=cumulative)
    else:
        stacked = ui.checkBox_stacked_histogram.isChecked()
        cmap = mpl.cm.get_cmap('Spectral')
        colors = {}
        labels = []
        i = 0
        for segname_combination in count:
            segn_a, segn_b = segname_combination
            if segn_a == segn_b: 
                labels.append(segn_a)
                colors[segname_combination] = segname_colors[segn_a]
            else:
                labels.append('{}-{}'.format(segn_a, segn_b))
                colors[segname_combination] = rgb_to_string(cmap(np.linspace(0,1,len(count)-len(segname_colors))[i]))
                i += 1
        multi_histogram(count.values(), colors=colors.values(), legend_labels=labels, mi=mi, ma=ma, nb_bins=nb_bins, xlabel='Occupancy', cumulative=cumulative, stacked=stacked)
    
def save_occupancy():
    nb_bins, mi, ma, count = compute_occupancy()
    if nb_bins is None: return
    labels = []
    for segname_combination in count:
        segn_a, segn_b = segname_combination
        if segn_a == segn_b: labels.append(segn_a)
        else: labels.append('{}-{}'.format(segn_a,segn_b))
    #filename = QFileDialog.getSaveFileName(main_window, 'Save Data', filter='ASCII File (*.txt);;All Files (*.*)')[0]
    #if not filename: return
    #with open(filename, 'w') as f:
    #    f.write(histogram_to_string(count.values(), mi=mi, ma=ma, nb_bins=nb_bins, labels=labels))
    main_window.results_dialog.show_results(histogram_to_string(count.values(), mi=mi, ma=ma, nb_bins=nb_bins, labels=labels))

def compute_jo():
    if segname_colors is None: return None, None, None
    frame_time, frame_unit = main_window._search_parameter['frame_time']
    results = main_window.analysis.filtered_results
    ts = np.ones(main_window.analysis.nb_frames, dtype=bool)
    for key in results: ts &= results[key]
    return ts, frame_time, frame_unit

def plot_jo():
    ts, frame_time, frame_unit = compute_jo()
    if ts is None: return
    
    if ui.radioButton_scatter.isChecked(): 
        try:
            scatter_size = float(ui.lineEdit_scatter_size.text())
        except:
            Error('Format Error!', 'Please specify the dot size as a floating point number.')
            return
        boolean_scatter(ts, scatter_size=scatter_size, frame_time=frame_time, frame_unit=frame_unit)
    else: 
        nodes = [node for node in main_window.analysis.filtered_graph.nodes()]
        occupancies = {node:{othernode:0.0 for othernode in nodes} for node in nodes}
        for key, result in main_window.analysis.filtered_results.items():
            a, b = key.split(':')
            occ = result.mean()
            occupancies[a][b] = occupancies[b][a] = occ
        resids = get_resids(nodes)
        ind = np.argsort(resids)
        nodes = [nodes[i] for i in ind]
        data = np.array([[occupancies[node][othernode] for node in nodes] for othernode in nodes[::-1]])
        heatmap(data, nodes, nodes[::-1], 'Joint Occupancy: '+str(np.round(ts.mean()*100,1)))
        

def save_jo():
    ts, frame_time, frame_unit = compute_jo()
    if ts is None: return
    if frame_time is not None:
        save_string = 'time_[{}] '.format(frame_unit) + ' '.join((np.arange(len(ts)) * frame_time).astype(np.str)) + '\n'
    else:
        save_string = 'frame ' + ' '.join(np.arange(len(ts)).astype(np.str)) + '\n'
    save_string += 'jo ' + ' '.join(ts.astype(np.str))
    #filename = QFileDialog.getSaveFileName(main_window, 'Save Data', filter='ASCII File (*.txt);;All Files (*.*)')[0]
    #if not filename: return
    #with open(filename, 'w') as f:
    #    f.write(string_in_columns(save_string))
    main_window.results_dialog.show_results(string_in_columns(save_string))

def compute_timeseries():
    if segname_colors is None: return None, None, None
    frame_time, frame_unit = main_window._search_parameter['frame_time']
    su = {(segname,segname):np.zeros(main_window.analysis.nb_frames, dtype=np.int) for segname in segname_colors}
    su.update({tuple(sorted(combination)):np.zeros(main_window.analysis.nb_frames, dtype=np.int) for combination in combinations(segname_colors.keys(), 2)})
    connections = main_window.analysis.filtered_results
    for key, ts in connections.items():
        segn_a, segn_b = get_segnames(key.split(':'))
        su[tuple(sorted((segn_a, segn_b)))] += ts
    return su, frame_time, frame_unit

def plot_timeseries():
    su, frame_time, frame_unit = compute_timeseries()
    if su is None: return
    color_by_segment = ui.checkBox_color_segments_timeseries.isChecked()
    if not color_by_segment: 
        one_sum = np.zeros(main_window.analysis.nb_frames)
        for key, value in su.items():
            one_sum += value
        timeseries(one_sum, frame_time=frame_time, frame_unit=frame_unit, xlabel='Frames')
    else:
        cmap = mpl.cm.get_cmap('Spectral')
        colors = {}
        labels = []
        i = 0
        for segname_combination in su:
            segn_a, segn_b = segname_combination
            if segn_a == segn_b: 
                labels.append(segn_a)
                colors[segname_combination] = segname_colors[segn_a]
            else:
                labels.append('{}-{}'.format(segn_a, segn_b))
                colors[segname_combination] = rgb_to_string(cmap(np.linspace(0,1,len(su)-len(segname_colors))[i]))
                i += 1
        multi_timeseries(list(su.values()), colors=list(colors.values()), legend_labels=labels, frame_time=frame_time, frame_unit=frame_unit)

def save_timeseries():
    su, frame_time, frame_unit = compute_timeseries()
    if su is None: return
    
    if frame_time is not None:
        save_string = 'time_[{}] '.format(frame_unit) + ' '.join((np.arange(main_window.analysis.nb_frames) * frame_time).astype(np.str)) + '\n'
    else:
        save_string = 'frame ' + ' '.join(np.arange(main_window.analysis.nb_frames).astype(np.str)) + '\n'
    for segname_combination, ts in su.items():
        segn_a, segn_b = segname_combination
        if segn_a == segn_b: save_string += segn_a 
        else: save_string += '{}-{}'.format(segn_a,segn_b)
        save_string += ' ' + ' '.join(ts.astype(np.str)) +'\n'
    #filename = QFileDialog.getSaveFileName(main_window, 'Save Data', filter='ASCII File (*.txt);;All Files (*.*)')[0]
    #if not filename: return
    #with open(filename, 'w') as f:
    #    f.write(string_in_columns(save_string))
    main_window.results_dialog.show_results(string_in_columns(save_string))

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        if not GroupBox.objectName():
            GroupBox.setObjectName(u"GroupBox")
        GroupBox.resize(535, 520)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GroupBox.sizePolicy().hasHeightForWidth())
        GroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(GroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_occupancy_histogram = QGroupBox(GroupBox)
        self.groupBox_occupancy_histogram.setObjectName(u"groupBox_occupancy_histogram")
        self.verticalLayout = QVBoxLayout(self.groupBox_occupancy_histogram)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_56 = QLabel(self.groupBox_occupancy_histogram)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setMaximumSize(QSize(16777215, 16777215))
        self.label_56.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_56)

        self.lineEdit_bins = QLineEdit(self.groupBox_occupancy_histogram)
        self.lineEdit_bins.setObjectName(u"lineEdit_bins")
        self.lineEdit_bins.setMinimumSize(QSize(50, 0))
        self.lineEdit_bins.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.lineEdit_bins)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_55 = QLabel(self.groupBox_occupancy_histogram)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setMaximumSize(QSize(16777215, 16777215))
        self.label_55.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_55)

        self.lineEdit_minimum = QLineEdit(self.groupBox_occupancy_histogram)
        self.lineEdit_minimum.setObjectName(u"lineEdit_minimum")
        self.lineEdit_minimum.setMinimumSize(QSize(50, 0))
        self.lineEdit_minimum.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.lineEdit_minimum)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.label_17 = QLabel(self.groupBox_occupancy_histogram)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_17)

        self.lineEdit_maximum = QLineEdit(self.groupBox_occupancy_histogram)
        self.lineEdit_maximum.setObjectName(u"lineEdit_maximum")
        self.lineEdit_maximum.setMinimumSize(QSize(50, 0))
        self.lineEdit_maximum.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout.addWidget(self.lineEdit_maximum)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.checkBox_cumulative_histogram = QCheckBox(self.groupBox_occupancy_histogram)
        self.checkBox_cumulative_histogram.setObjectName(u"checkBox_cumulative_histogram")

        self.horizontalLayout_7.addWidget(self.checkBox_cumulative_histogram)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_12)

        self.checkBox_stacked_histogram = QCheckBox(self.groupBox_occupancy_histogram)
        self.checkBox_stacked_histogram.setObjectName(u"checkBox_stacked_histogram")

        self.horizontalLayout_7.addWidget(self.checkBox_stacked_histogram)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.checkBox_color_segments_occupancy = QCheckBox(self.groupBox_occupancy_histogram)
        self.checkBox_color_segments_occupancy.setObjectName(u"checkBox_color_segments_occupancy")
        self.checkBox_color_segments_occupancy.setChecked(True)

        self.horizontalLayout_6.addWidget(self.checkBox_color_segments_occupancy)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_save_occupancy = QPushButton(self.groupBox_occupancy_histogram)
        self.pushButton_save_occupancy.setObjectName(u"pushButton_save_occupancy")

        self.horizontalLayout_2.addWidget(self.pushButton_save_occupancy)

        self.pushButton_plot_occupancy = QPushButton(self.groupBox_occupancy_histogram)
        self.pushButton_plot_occupancy.setObjectName(u"pushButton_plot_occupancy")
        self.pushButton_plot_occupancy.setAutoDefault(False)

        self.horizontalLayout_2.addWidget(self.pushButton_plot_occupancy)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.groupBox_occupancy_histogram)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.groupBox_nb_connections = QGroupBox(GroupBox)
        self.groupBox_nb_connections.setObjectName(u"groupBox_nb_connections")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_nb_connections)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.checkBox_color_segments_timeseries = QCheckBox(self.groupBox_nb_connections)
        self.checkBox_color_segments_timeseries.setObjectName(u"checkBox_color_segments_timeseries")
        self.checkBox_color_segments_timeseries.setChecked(True)

        self.horizontalLayout_5.addWidget(self.checkBox_color_segments_timeseries)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.pushButton_save_timeseries = QPushButton(self.groupBox_nb_connections)
        self.pushButton_save_timeseries.setObjectName(u"pushButton_save_timeseries")

        self.horizontalLayout_4.addWidget(self.pushButton_save_timeseries)

        self.pushButton_plot_timeseries = QPushButton(self.groupBox_nb_connections)
        self.pushButton_plot_timeseries.setObjectName(u"pushButton_plot_timeseries")
        self.pushButton_plot_timeseries.setAutoDefault(False)

        self.horizontalLayout_4.addWidget(self.pushButton_plot_timeseries)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.groupBox_nb_connections)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.groupBox_joint_occupancy = QGroupBox(GroupBox)
        self.groupBox_joint_occupancy.setObjectName(u"groupBox_joint_occupancy")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_joint_occupancy)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.radioButton_scatter = QRadioButton(self.groupBox_joint_occupancy)
        self.radioButton_scatter.setObjectName(u"radioButton_scatter")
        self.radioButton_scatter.setChecked(True)

        self.horizontalLayout_10.addWidget(self.radioButton_scatter)

        self.label_3 = QLabel(self.groupBox_joint_occupancy)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_10.addWidget(self.label_3)

        self.lineEdit_scatter_size = QLineEdit(self.groupBox_joint_occupancy)
        self.lineEdit_scatter_size.setObjectName(u"lineEdit_scatter_size")
        self.lineEdit_scatter_size.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_10.addWidget(self.lineEdit_scatter_size)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_10)


        self.verticalLayout_4.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_heatmap = QRadioButton(self.groupBox_joint_occupancy)
        self.radioButton_heatmap.setObjectName(u"radioButton_heatmap")

        self.horizontalLayout_3.addWidget(self.radioButton_heatmap)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.pushButton_save_jo = QPushButton(self.groupBox_joint_occupancy)
        self.pushButton_save_jo.setObjectName(u"pushButton_save_jo")

        self.horizontalLayout_3.addWidget(self.pushButton_save_jo)

        self.pushButton_plot_jo = QPushButton(self.groupBox_joint_occupancy)
        self.pushButton_plot_jo.setObjectName(u"pushButton_plot_jo")
        self.pushButton_plot_jo.setAutoDefault(False)

        self.horizontalLayout_3.addWidget(self.pushButton_plot_jo)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox_joint_occupancy)


        self.retranslateUi(GroupBox)

        QMetaObject.connectSlotsByName(GroupBox)
    # setupUi

    def retranslateUi(self, GroupBox):
        GroupBox.setWindowTitle(QCoreApplication.translate("GroupBox", u"GroupBox", None))
        self.groupBox_occupancy_histogram.setTitle(QCoreApplication.translate("GroupBox", u"Occupancy histogram", None))
        self.label_56.setText(QCoreApplication.translate("GroupBox", u"# of bins", None))
        self.lineEdit_bins.setText(QCoreApplication.translate("GroupBox", u"10", None))
        self.label_55.setText(QCoreApplication.translate("GroupBox", u"min. occupancy", None))
        self.lineEdit_minimum.setText(QCoreApplication.translate("GroupBox", u"0.0", None))
        self.label_17.setText(QCoreApplication.translate("GroupBox", u"max. occupancy", None))
        self.lineEdit_maximum.setText(QCoreApplication.translate("GroupBox", u"1.0", None))
        self.checkBox_cumulative_histogram.setText(QCoreApplication.translate("GroupBox", u"cumulative", None))
        self.checkBox_stacked_histogram.setText(QCoreApplication.translate("GroupBox", u"stacked", None))
#if QT_CONFIG(tooltip)
        self.checkBox_color_segments_occupancy.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p align=\"justify\">Toggle if histogram bars are colored by segment or molecule. With colors turned on, comparing to other analyses is not possible.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_color_segments_occupancy.setText(QCoreApplication.translate("GroupBox", u"color by segment", None))
        self.pushButton_save_occupancy.setText(QCoreApplication.translate("GroupBox", u"Data", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_occupancy.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p>Compute histogram of H bond occupancies. Counts the number of H bonds with an occupancy equal or greater than the respective value.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_occupancy.setText(QCoreApplication.translate("GroupBox", u"Plot", None))
        self.groupBox_nb_connections.setTitle(QCoreApplication.translate("GroupBox", u"Number of connections time series", None))
#if QT_CONFIG(tooltip)
        self.checkBox_color_segments_timeseries.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p align=\"justify\">Toggle if histogram bars are colored by segment or molecule. With colors turned on, comparing to other analyses is not possible.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_color_segments_timeseries.setText(QCoreApplication.translate("GroupBox", u"color by segment", None))
        self.pushButton_save_timeseries.setText(QCoreApplication.translate("GroupBox", u"Data", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_timeseries.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p align=\"justify\">Compute the number of H bonds per frame.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_timeseries.setText(QCoreApplication.translate("GroupBox", u"Plot", None))
        self.groupBox_joint_occupancy.setTitle(QCoreApplication.translate("GroupBox", u"Joint Occupancy", None))
        self.radioButton_scatter.setText(QCoreApplication.translate("GroupBox", u"scatter plot", None))
        self.label_3.setText(QCoreApplication.translate("GroupBox", u"with dot size", None))
        self.lineEdit_scatter_size.setText(QCoreApplication.translate("GroupBox", u"1", None))
        self.lineEdit_scatter_size.setPlaceholderText(QCoreApplication.translate("GroupBox", u"0 - 100", None))
        self.radioButton_heatmap.setText(QCoreApplication.translate("GroupBox", u"heatmap", None))
        self.pushButton_save_jo.setText(QCoreApplication.translate("GroupBox", u"Data", None))
#if QT_CONFIG(tooltip)
        self.pushButton_plot_jo.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p align=\"justify\">Compute the joint occupancy of the H bond network. The joint occupancy is true, if all H bonds of the network are present in a frame and false otherwise.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_plot_jo.setText(QCoreApplication.translate("GroupBox", u"Plot", None))
    # retranslateUi

