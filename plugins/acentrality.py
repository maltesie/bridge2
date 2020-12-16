# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'centrality.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, Qt, QSize)
from PySide2.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, 
     QCheckBox, QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, 
     QComboBox, QRadioButton, QFileDialog)
from core.helpfunctions import (Error, get_segname, get_resids, get_resid,
                                ranges_to_numbers, aa_three2one, get_resname)
from core.drawing import bar, multi_bar, histogram, multi_histogram
import numpy as np
import csv

main_window = None
plugin_widget = None
title = 'Centrality Measures'

ui = None
segname_colors = None
centralities = None


def load(parent):
    global plugin_widget, main_window, ui
    main_window = parent
    plugin_widget = QGroupBox()
    plugin_widget.setTitle('')
    ui = Ui_GroupBox()
    ui.setupUi(plugin_widget)
    ui.pushButton_degree_plot.clicked.connect(plot_centrality)
    ui.pushButton_degree_save.clicked.connect(save_centrality)
    ui.groupBox_per_residue.toggled.connect(toggle_histogram)
    ui.groupBox_histogram.toggled.connect(toggle_per_residue)
    ui.checkBox_normalized.toggled.connect(update_min_max)
    ui.checkBox_averaged_frames.toggled.connect(update_min_max)
    ui.radioButton_degree.toggled.connect(update_min_max)
    ui.radioButton_betweenness.toggled.connect(update_min_max)

def update(parent):
    global main_window, segname_colors, centralities
    main_window = parent
    if main_window.analysis is not None: 
        segname_colors = main_window._segname_colors
    else: return
    if main_window.analysis.centralities is not None: 
        centralities = main_window.analysis.centralities
        ui.comboBox.clear()
        ui.comboBox.addItems(['all']+list(segname_colors.keys()))
        
def update_min_max():
    if centralities is None: return
    if ui.radioButton_betweenness.isChecked():
        centrality_type = 'betweenness'
    else:
        centrality_type = 'degree'
    average_across_frames = ui.checkBox_averaged_frames.isChecked()
    normalized = ui.checkBox_normalized.isChecked()
    centrality = centralities[centrality_type][average_across_frames][normalized]
    mi, ma = min(centrality.values()), max(centrality.values())
    try: significant = int(np.log10(ma-mi))
    except: significant = 1
    if significant < 0: r = np.abs(significant)+1
    else: r = 1
    mi, ma = np.round([mi, ma], r)
    ui.lineEdit_minimum.setText(str(mi))
    ui.lineEdit_maximum.setText(str(ma))

def toggle_histogram():
    per_residue_state = ui.groupBox_per_residue.isChecked()
    ui.groupBox_histogram.setChecked(not per_residue_state)
    
def toggle_per_residue():
    histogram_state = ui.groupBox_histogram.isChecked()
    ui.groupBox_per_residue.setChecked(not histogram_state)

def compute_centrality_bar():
    if centralities is None: return None, None
    ranges_string = ui.lineEdit_degree_residue_ids.text()
    if ranges_string != '' and ui.groupBox_per_residue.isChecked():
        numbers = ranges_to_numbers(ranges_string)
        if numbers == []:
            Error('Could not interpret input!', 'Please specify the residue ids as ranges [start-end] and integers devided by comma.')
            return None
        else:
            numbers = np.unique(numbers)
    else:
        mi = min(get_resids(main_window.interactive_graph.nodes()))
        ma = max (get_resids(main_window.interactive_graph.nodes()))
        numbers = np.arange(mi, ma+1, dtype=np.int)
    numbers -= main_window.analysis.add_missing_residues
    number_id = {number:i for i,number in enumerate(numbers)}
    segname_id = {segname:i for i,segname in enumerate(segname_colors)}
    if ui.radioButton_betweenness.isChecked():
        centrality_type = 'betweenness'
    else:
        centrality_type = 'degree'
    average_across_frames = ui.checkBox_averaged_frames.isChecked()
    normalized = ui.checkBox_normalized.isChecked()
    centrality = centralities[centrality_type][average_across_frames][normalized]
    centrality_per_segname = np.zeros((len(numbers), len(segname_colors)),  dtype=np.float)
    label_per_segname = np.empty((len(numbers), len(segname_colors)), dtype='<U12')
    for node in centrality:
        segname, resname, resid = get_segname(node), aa_three2one[get_resname(node)], get_resid(node)
        if resid not in numbers: continue
        segname_i, resid_i = segname_id[segname], number_id[resid]
        centrality_per_segname[resid_i, segname_i] = centrality[node]
        label_per_segname[resid_i, segname_i] = '{}{}'.format(resname,resid+main_window.analysis.add_missing_residues)
    return centrality_per_segname.T, label_per_segname.T
        
def plot_centrality_bar():
    if centralities is None: return
    if ui.radioButton_betweenness.isChecked():
        centrality_type = 'Betweenness'
    else:
        centrality_type = 'Degree'
    centrality_per_segname, label_per_segname = compute_centrality_bar()
    segname_id = {segname:i for i,segname in enumerate(segname_colors)}
    segname = ui.comboBox.currentText()
    integer_y = ui.radioButton_degree.isChecked() & (not ui.checkBox_averaged_frames.isChecked()) & (not ui.checkBox_normalized.isChecked())
    if segname != 'all':
        centrality, labels = centrality_per_segname[segname_id[segname]], label_per_segname[segname_id[segname]]
        bar(data=centrality, labels=labels, ylabel='{} Centrality'.format(centrality_type), integer_y=integer_y, show_zeros=False)
    else:
        centrality, labels = centrality_per_segname, label_per_segname
        multi_bar(data=centrality, labels=labels, colors=segname_colors, ylabel='{} Centrality'.format(centrality_type), integer_y=integer_y, show_zeros=False)

def compute_centrality_histogram():
    try:
        nb_bins = int(ui.lineEdit_bins.text()) + 1
    except:
        Error('Format Error', 'Please enter an integer as number of bins.')
        return None, None, None, None
    try:
        mi, ma = float(ui.lineEdit_minimum.text()), float(ui.lineEdit_maximum.text())
    except:
        Error('Format Error', 'Minimum and maximum occupancy have to be floats.')
        return None, None, None, None
    centrality_per_segname, label_per_segname = compute_centrality_bar()
    count = {segname:centrality_per_segname[i][centrality_per_segname[i] != 0] for i, segname in enumerate(segname_colors)}
    return nb_bins, mi, ma, count
    
def plot_centrality_histogram():
    nb_bins, mi, ma, count = compute_centrality_histogram()
    if nb_bins is None: return
    color_by_segment = ui.checkBox_color_segments_occupancy.isChecked()
    cumulative = ui.checkBox_cumulative_histogram.isChecked()
    if cumulative: cumulative = -1
    if not color_by_segment: 
        one_count = []
        for key, value in count.items():
            one_count += list(value)
        histogram(one_count, mi=mi, ma=ma, nb_bins=nb_bins, xlabel='Occupancy', cumulative=cumulative)
    else:
        stacked = ui.checkBox_stacked_histogram.isChecked()
        multi_histogram(count.values(), colors=segname_colors.values(), legend_labels=segname_colors.keys(), mi=mi, ma=ma, nb_bins=nb_bins, xlabel='Centrality', cumulative=cumulative, stacked=stacked)

def plot_centrality():
    if centralities is None: return
    if ui.groupBox_histogram.isChecked():
        plot_centrality_histogram()
    else:
        plot_centrality_bar()

def save_centrality():
    if centralities is None: return
    csv_columns = ['residue','degree_normalized_averaged', 'degree_normalized_not-averaged', 
                   'degree_not-normalized_averaged', 'degree_not-normalized_not-averaged', 
                   'betweenness_normalized_averaged', 'betweenness_normalized_not-averaged', 
                   'betweenness_not-normalized_averaged', 'betweenness_not-normalized_not-averaged']
    #csv_file = QFileDialog.getSaveFileName(main_window, 'Save Centrality', filter='ASCII File (*.txt);;All Files (*.*)')[0]
    #if not csv_file: return
    #try:
    #    with open(csv_file, 'w') as csvfile:
    #        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    #        writer.writeheader()
    #        for node in main_window.interactive_graph.nodes():
    #            data_row = {'residue':node,
    #                        'degree_normalized_averaged': centralities['degree'][True][True][node], 
    #                        'degree_normalized_not-averaged': centralities['degree'][False][True][node], 
    #                        'degree_not-normalized_averaged': centralities['degree'][True][False][node], 
    #                        'degree_not-normalized_not-averaged': centralities['degree'][False][False][node], 
    #                        'betweenness_normalized_averaged': centralities['betweenness'][True][True][node], 
    #                        'betweenness_normalized_not-averaged': centralities['betweenness'][False][True][node], 
    #                        'betweenness_not-normalized_averaged': centralities['betweenness'][True][False][node], 
    #                        'betweenness_not-normalized_not-averaged': centralities['betweenness'][False][False][node]}
    #            writer.writerow(data_row)
    #except IOError:
    #    Error('I/O Error!', 'Could not write to disc.')
    save_string = '\t'.join([column for column in csv_columns]) + '\n'
    for node in sorted(main_window.interactive_graph.nodes()):
        if main_window.analysis.residuewise: 
            segname, resname, resid = node.split('-')
            resid = str(int(resid)+main_window.analysis.add_missing_residues)
            node_label = '-'.join([segname, resname, resid])
        else: 
            segname, resname, resid, atom_name = node.split('-')
            resid = str(int(resid)+main_window.analysis.add_missing_residues)
            node_label = '-'.join([segname, resname, resid, atom_name])
        save_string += '\t'.join([node_label, str(centralities['degree'][True][True][node]), 
                                  str(centralities['degree'][False][True][node]), 
                                  str(centralities['degree'][True][False][node]), 
                                  str(centralities['degree'][False][False][node]), 
                                  str(centralities['betweenness'][True][True][node]), 
                                  str(centralities['betweenness'][False][True][node]), 
                                  str(centralities['betweenness'][True][False][node]), 
                                  str(centralities['betweenness'][False][False][node])]) + '\n'
    main_window.results_dialog.show_results(save_string)
            
class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        if not GroupBox.objectName():
            GroupBox.setObjectName(u"GroupBox")
        GroupBox.resize(528, 576)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GroupBox.sizePolicy().hasHeightForWidth())
        GroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(GroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(GroupBox)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.pushButton_degree_save = QPushButton(self.groupBox)
        self.pushButton_degree_save.setObjectName(u"pushButton_degree_save")

        self.horizontalLayout_7.addWidget(self.pushButton_degree_save)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.groupBox_degree = QGroupBox(GroupBox)
        self.groupBox_degree.setObjectName(u"groupBox_degree")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_degree)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButton_betweenness = QRadioButton(self.groupBox_degree)
        self.radioButton_betweenness.setObjectName(u"radioButton_betweenness")

        self.horizontalLayout_2.addWidget(self.radioButton_betweenness)

        self.radioButton_degree = QRadioButton(self.groupBox_degree)
        self.radioButton_degree.setObjectName(u"radioButton_degree")
        self.radioButton_degree.setChecked(True)

        self.horizontalLayout_2.addWidget(self.radioButton_degree)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.checkBox_averaged_frames = QCheckBox(self.groupBox_degree)
        self.checkBox_averaged_frames.setObjectName(u"checkBox_averaged_frames")
        self.checkBox_averaged_frames.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_averaged_frames)

        self.checkBox_normalized = QCheckBox(self.groupBox_degree)
        self.checkBox_normalized.setObjectName(u"checkBox_normalized")

        self.verticalLayout_3.addWidget(self.checkBox_normalized)

        self.groupBox_per_residue = QGroupBox(self.groupBox_degree)
        self.groupBox_per_residue.setObjectName(u"groupBox_per_residue")
        self.groupBox_per_residue.setCheckable(True)
        self.verticalLayout = QVBoxLayout(self.groupBox_per_residue)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_2 = QLabel(self.groupBox_per_residue)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_6.addWidget(self.label_2)

        self.comboBox = QComboBox(self.groupBox_per_residue)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_6.addWidget(self.comboBox)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_10 = QLabel(self.groupBox_per_residue)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout.addWidget(self.label_10)

        self.lineEdit_degree_residue_ids = QLineEdit(self.groupBox_per_residue)
        self.lineEdit_degree_residue_ids.setObjectName(u"lineEdit_degree_residue_ids")

        self.horizontalLayout.addWidget(self.lineEdit_degree_residue_ids)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.groupBox_per_residue)

        self.groupBox_histogram = QGroupBox(self.groupBox_degree)
        self.groupBox_histogram.setObjectName(u"groupBox_histogram")
        self.groupBox_histogram.setCheckable(True)
        self.groupBox_histogram.setChecked(False)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_histogram)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_56 = QLabel(self.groupBox_histogram)
        self.label_56.setObjectName(u"label_56")
        self.label_56.setMaximumSize(QSize(16777215, 16777215))
        self.label_56.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_56)

        self.lineEdit_bins = QLineEdit(self.groupBox_histogram)
        self.lineEdit_bins.setObjectName(u"lineEdit_bins")
        self.lineEdit_bins.setMinimumSize(QSize(50, 0))
        self.lineEdit_bins.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit_bins)

        self.label_55 = QLabel(self.groupBox_histogram)
        self.label_55.setObjectName(u"label_55")
        self.label_55.setMaximumSize(QSize(16777215, 16777215))
        self.label_55.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_55)

        self.lineEdit_minimum = QLineEdit(self.groupBox_histogram)
        self.lineEdit_minimum.setObjectName(u"lineEdit_minimum")
        self.lineEdit_minimum.setMinimumSize(QSize(50, 0))
        self.lineEdit_minimum.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit_minimum)

        self.label_17 = QLabel(self.groupBox_histogram)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.label_17)

        self.lineEdit_maximum = QLineEdit(self.groupBox_histogram)
        self.lineEdit_maximum.setObjectName(u"lineEdit_maximum")
        self.lineEdit_maximum.setMinimumSize(QSize(50, 0))
        self.lineEdit_maximum.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.lineEdit_maximum)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.checkBox_cumulative_histogram = QCheckBox(self.groupBox_histogram)
        self.checkBox_cumulative_histogram.setObjectName(u"checkBox_cumulative_histogram")

        self.horizontalLayout_8.addWidget(self.checkBox_cumulative_histogram)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_12)

        self.checkBox_stacked_histogram = QCheckBox(self.groupBox_histogram)
        self.checkBox_stacked_histogram.setObjectName(u"checkBox_stacked_histogram")

        self.horizontalLayout_8.addWidget(self.checkBox_stacked_histogram)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_11)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.checkBox_color_segments_occupancy = QCheckBox(self.groupBox_histogram)
        self.checkBox_color_segments_occupancy.setObjectName(u"checkBox_color_segments_occupancy")
        self.checkBox_color_segments_occupancy.setChecked(True)

        self.horizontalLayout_9.addWidget(self.checkBox_color_segments_occupancy)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)


        self.verticalLayout_3.addWidget(self.groupBox_histogram)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.pushButton_degree_plot = QPushButton(self.groupBox_degree)
        self.pushButton_degree_plot.setObjectName(u"pushButton_degree_plot")
        self.pushButton_degree_plot.setAutoDefault(False)

        self.horizontalLayout_5.addWidget(self.pushButton_degree_plot)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)


        self.verticalLayout_2.addWidget(self.groupBox_degree)


        self.retranslateUi(GroupBox)

        QMetaObject.connectSlotsByName(GroupBox)
    # setupUi

    def retranslateUi(self, GroupBox):
        GroupBox.setWindowTitle(QCoreApplication.translate("GroupBox", u"GroupBox", None))
        self.groupBox.setTitle(QCoreApplication.translate("GroupBox", u"All centrality measures", None))
        self.pushButton_degree_save.setText(QCoreApplication.translate("GroupBox", u"Data", None))
        self.groupBox_degree.setTitle(QCoreApplication.translate("GroupBox", u"Plots", None))
        self.radioButton_betweenness.setText(QCoreApplication.translate("GroupBox", u"betweenness centrality", None))
        self.radioButton_degree.setText(QCoreApplication.translate("GroupBox", u"degree centrality", None))
#if QT_CONFIG(tooltip)
        self.checkBox_averaged_frames.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p align=\"justify\">Toggle, if absolute number of connections or time averaged number of connections are used.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_averaged_frames.setText(QCoreApplication.translate("GroupBox", u"average across frames", None))
        self.checkBox_normalized.setText(QCoreApplication.translate("GroupBox", u"normalized", None))
        self.groupBox_per_residue.setTitle(QCoreApplication.translate("GroupBox", u"Per Residue", None))
        self.label_2.setText(QCoreApplication.translate("GroupBox", u"segment: ", None))
        self.label_10.setText(QCoreApplication.translate("GroupBox", u"residue ids: ", None))
        self.lineEdit_degree_residue_ids.setPlaceholderText(QCoreApplication.translate("GroupBox", u"e.g. 0-12, 20, 70-90", None))
        self.groupBox_histogram.setTitle(QCoreApplication.translate("GroupBox", u"Histogram", None))
        self.label_56.setText(QCoreApplication.translate("GroupBox", u"# of bins", None))
        self.lineEdit_bins.setText(QCoreApplication.translate("GroupBox", u"10", None))
        self.label_55.setText(QCoreApplication.translate("GroupBox", u"min. value", None))
        self.lineEdit_minimum.setText(QCoreApplication.translate("GroupBox", u"0.0", None))
        self.label_17.setText(QCoreApplication.translate("GroupBox", u"max. value", None))
        self.lineEdit_maximum.setText(QCoreApplication.translate("GroupBox", u"1.0", None))
        self.checkBox_cumulative_histogram.setText(QCoreApplication.translate("GroupBox", u"cumulative", None))
        self.checkBox_stacked_histogram.setText(QCoreApplication.translate("GroupBox", u"stacked", None))
#if QT_CONFIG(tooltip)
        self.checkBox_color_segments_occupancy.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p align=\"justify\">Toggle if histogram bars are colored by segment or molecule. With colors turned on, comparing to other analyses is not possible.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_color_segments_occupancy.setText(QCoreApplication.translate("GroupBox", u"color by segment", None))
#if QT_CONFIG(tooltip)
        self.pushButton_degree_plot.setToolTip(QCoreApplication.translate("GroupBox", u"<html><head/><body><p align=\"justify\">Compute the number of H bonds per residue. Results are colored by segment.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_degree_plot.setText(QCoreApplication.translate("GroupBox", u"Plot", None))
    # retranslateUi

