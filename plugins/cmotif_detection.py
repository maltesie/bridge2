# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'motif_detection.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

#from PySide2.QtGui import (QColor, QPalette, QBrush)
from PySide2.QtCore import (QCoreApplication, QMetaObject)
from PySide2.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout,
     QSpacerItem, QSizePolicy, QPushButton, QCheckBox)

main_window = None
plugin_widget = None
title = 'H Bond Motifs'
ui = None

def load(parent):
    global plugin_widget, main_window, ui
    main_window = parent
    plugin_widget = QGroupBox()
    plugin_widget.setTitle('')
    ui = Ui_GroupBox()
    ui.setupUi(plugin_widget)
    ui.checkBox_asp_asn.clicked.connect(show_motifs)
    ui.checkBox_glu_his.clicked.connect(show_motifs)
    ui.checkBox_his_his.clicked.connect(show_motifs)
    ui.checkBox_ser_backbone.clicked.connect(show_motifs)
    ui.checkBox_his_ser.clicked.connect(show_motifs)
    ui.checkBox_asp_ser.clicked.connect(show_motifs)

def update(parent):
    global main_window
    main_window = parent
    if (main_window._analysis_type == 'hb') and (not main_window.analysis.residuewise): 
        plugin_widget.setEnabled(True)
        plugin_widget.setTitle('')
    else: 
        plugin_widget.setEnabled(False)
        plugin_widget.setTitle('(perform H-bond analysis with residuewise unchecked)')

def split_node(node):
    return node.split('-')

def is_asp_glu(res, atom):
    return ((res in ['ASP', 'GLU']) and (atom.startswith('O') and (len(atom)>1)))

def is_ser_thr(res, atom):
    return ((res in ['THR', 'SER']) and (atom.startswith('O') and (len(atom)>1)))

def is_his(res, atom):
    return ((res in ['HIS', 'HSD', 'HSE', 'HSP']) and (atom in ['ND1', 'NE2']))

def is_asn(res, atom):
    return ((res == 'ASN') and (atom in ['ND1', 'OD2']))

def is_backbone(res, atom):
    return (atom=='O')

def reset_text_color():
    ui.checkBox_asp_asn.setStyleSheet("color: black")
    ui.checkBox_asp_ser.setStyleSheet("color: black")
    ui.checkBox_glu_his.setStyleSheet("color: black")
    ui.checkBox_his_his.setStyleSheet("color: black")
    ui.checkBox_his_ser.setStyleSheet("color: black")
    ui.checkBox_ser_backbone.setStyleSheet("color: black")

def show_motifs():
    reset_text_color()
    main_window.interactive_graph.reset_selected_nodes()
    for node, other_node, edge_data in main_window.interactive_graph.edges():
        segn1, resn1, reid1, atom1 = split_node(node)
        segn2, resn2, reid2, atom2 = split_node(other_node)
        if ui.checkBox_asp_asn.isChecked():
            if (is_asp_glu(resn1, atom1) and is_asn(resn2, atom2)) or (is_asp_glu(resn2, atom2) and is_asn(resn1, atom1)):
                ui.checkBox_asp_asn.setStyleSheet("color: red")
                main_window.interactive_graph.selected_nodes += [node, other_node]
                edge_data['color'] = 'red'
                continue
        if ui.checkBox_asp_ser.isChecked():
            if (is_asp_glu(resn1, atom1) and is_ser_thr(resn2, atom2)) or (is_asp_glu(resn2, atom2) and is_ser_thr(resn1, atom1)):
                ui.checkBox_asp_ser.setStyleSheet("color: blue")
                main_window.interactive_graph.selected_nodes += [node, other_node]
                edge_data['color'] = 'blue'
                continue
        if ui.checkBox_glu_his.isChecked():
            if (is_asp_glu(resn1, atom1) and is_his(resn2, atom2)) or (is_asp_glu(resn2, atom2) and is_his(resn1, atom1)):
                ui.checkBox_glu_his.setStyleSheet("color: darkCyan")
                main_window.interactive_graph.selected_nodes += [node, other_node]
                edge_data['color'] = 'darkCyan'
                continue
        if ui.checkBox_his_his.isChecked():
            if (is_his(resn1, atom1) and is_his(resn2, atom2)):
                ui.checkBox_his_his.setStyleSheet("color: green")
                main_window.interactive_graph.selected_nodes += [node, other_node]
                edge_data['color'] = 'green'
                continue
        if ui.checkBox_his_ser.isChecked():
            if (is_his(resn1, atom1) and is_ser_thr(resn2, atom2)) or (is_his(resn2, atom2) and is_ser_thr(resn1, atom1)):
                ui.checkBox_his_ser.setStyleSheet("color: brown")
                main_window.interactive_graph.selected_nodes += [node, other_node]
                edge_data['color'] = 'brown'
                continue
        if ui.checkBox_ser_backbone.isChecked():
            if (is_ser_thr(resn1, atom1) and is_backbone(resn2, atom2)) or (is_ser_thr(resn2, atom2) and is_backbone(resn1, atom1)):
                ui.checkBox_ser_backbone.setStyleSheet("color: orange")
                main_window.interactive_graph.selected_nodes += [node, other_node]
                edge_data['color'] = 'orange'
                continue
        edge_data['color'] = 'black'
    main_window.interactive_graph.selected_nodes = list(set(main_window.interactive_graph.selected_nodes))
    main_window.interactive_graph.process_selected_nodes()
    main_window.interactive_graph.set_edge_color()
    
class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        if not GroupBox.objectName():
            GroupBox.setObjectName(u"GroupBox")
        GroupBox.resize(453, 267)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GroupBox.sizePolicy().hasHeightForWidth())
        GroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(GroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(GroupBox)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 10, -1, -1)
        self.checkBox_asp_ser = QCheckBox(self.groupBox)
        self.checkBox_asp_ser.setObjectName(u"checkBox_asp_ser")

        self.verticalLayout_2.addWidget(self.checkBox_asp_ser)

        self.checkBox_ser_backbone = QCheckBox(self.groupBox)
        self.checkBox_ser_backbone.setObjectName(u"checkBox_ser_backbone")

        self.verticalLayout_2.addWidget(self.checkBox_ser_backbone)

        self.checkBox_glu_his = QCheckBox(self.groupBox)
        self.checkBox_glu_his.setObjectName(u"checkBox_glu_his")

        self.verticalLayout_2.addWidget(self.checkBox_glu_his)

        self.checkBox_his_his = QCheckBox(self.groupBox)
        self.checkBox_his_his.setObjectName(u"checkBox_his_his")

        self.verticalLayout_2.addWidget(self.checkBox_his_his)

        self.checkBox_asp_asn = QCheckBox(self.groupBox)
        self.checkBox_asp_asn.setObjectName(u"checkBox_asp_asn")

        self.verticalLayout_2.addWidget(self.checkBox_asp_asn)

        self.checkBox_his_ser = QCheckBox(self.groupBox)
        self.checkBox_his_ser.setObjectName(u"checkBox_his_ser")

        self.verticalLayout_2.addWidget(self.checkBox_his_ser)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout.addWidget(self.groupBox)


        self.retranslateUi(GroupBox)

        QMetaObject.connectSlotsByName(GroupBox)
    # setupUi

    def retranslateUi(self, GroupBox):
        GroupBox.setWindowTitle(QCoreApplication.translate("GroupBox", u"GroupBox", None))
        self.groupBox.setTitle(QCoreApplication.translate("GroupBox", u"Detect motif", None))
        self.checkBox_asp_ser.setText(QCoreApplication.translate("GroupBox", u"Asp/Glu carboxylate oxygen - Ser/Thr hydroxyl oxygen", None))
        self.checkBox_ser_backbone.setText(QCoreApplication.translate("GroupBox", u"Ser-Thr  hydroxyl oxygen - backbone carbonyl oxygen", None))
        self.checkBox_glu_his.setText(QCoreApplication.translate("GroupBox", u"Asp/Glu carboxylate oxygen - His/Hse/Hsd ND1 or NE2", None))
        self.checkBox_his_his.setText(QCoreApplication.translate("GroupBox", u"His/Hse/Hsd ND1 or NE2 - His/Hse/Hsd ND1 or NE2", None))
        self.checkBox_asp_asn.setText(QCoreApplication.translate("GroupBox", u"Asp/Glu carboxylate oxygen - Asn ND1 or OD2", None))
        self.checkBox_his_ser.setText(QCoreApplication.translate("GroupBox", u"His/Hse/Hsd ND1 or NE2 - Ser/Thr hydroxyl oxygen", None))
    # retranslateUi

