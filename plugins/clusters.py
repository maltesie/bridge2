# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clusters.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject)
from PySide2.QtWidgets import (QGroupBox, QFileDialog, QVBoxLayout, QHBoxLayout, 
     QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, QComboBox)

main_window = None
plugin_widget = None
title = 'Cluster Analysis'
ui = None

def load(parent):
    global plugin_widget, main_window, ui
    main_window = parent
    plugin_widget = QGroupBox()
    plugin_widget.setTitle('')
    ui = Ui_GroupBox()
    ui.setupUi(plugin_widget)
    #ui.pushButton_plot.clicked.connect(plot)
    #ui.pushButton_save.clicked.connect(save_data)

def update(parent):
    global main_window
    main_window = parent
    if main_window._analysis_type == 'ww': plugin_widget.setTitle('Water wires per frame')
    elif main_window._analysis_type == 'hb': plugin_widget.setTitle('H bonds per frame')
    
def plot():
    if main_window.analysis is None: return
    if ui.checkBox_color_segments.isChecked():
        colors = {key:value for key, value in main_window._segname_colors.items()}
        figure, results = main_window.analysis.draw_multi_segment_connection_timeseries(colors=colors, return_figure=True)
    else:
        figure, results = main_window.analysis.draw_connection_timeseries(return_figure=True)
    figure.show()
    
def save_data():
    if main_window.analysis is None: return
    if ui.checkBox_color_segments.isChecked():
        colors = {key:value for key, value in main_window._segname_colors.items()}
        figure, results = main_window.analysis.draw_multi_segment_connection_timeseries(colors=colors, return_figure=True)
    else:
        figure, results = main_window.analysis.draw_connection_timeseries(return_figure=True)
    filename = QFileDialog.getSaveFileName(main_window, 'Save Data', filter='ASCII File (*.txt);;All Files (*.*)')[0]
    if filename:
        with open(filename, 'w') as f:
            f.write(results)

class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        if not GroupBox.objectName():
            GroupBox.setObjectName(u"GroupBox")
        GroupBox.resize(425, 423)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GroupBox.sizePolicy().hasHeightForWidth())
        GroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(GroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(GroupBox)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(117, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pushButton_save_clusters = QPushButton(self.groupBox)
        self.pushButton_save_clusters.setObjectName(u"pushButton_save_clusters")

        self.horizontalLayout_2.addWidget(self.pushButton_save_clusters)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.groupBox_2 = QGroupBox(GroupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.lineEdit_node_picker1 = QLineEdit(self.groupBox_2)
        self.lineEdit_node_picker1.setObjectName(u"lineEdit_node_picker1")

        self.horizontalLayout_4.addWidget(self.lineEdit_node_picker1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_5.addWidget(self.comboBox)

        self.lineEdit = QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_5.addWidget(self.lineEdit)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.pushButton_save_cluster = QPushButton(self.groupBox_2)
        self.pushButton_save_cluster.setObjectName(u"pushButton_save_cluster")

        self.horizontalLayout_3.addWidget(self.pushButton_save_cluster)

        self.pushButton_draw_cluster = QPushButton(self.groupBox_2)
        self.pushButton_draw_cluster.setObjectName(u"pushButton_draw_cluster")

        self.horizontalLayout_3.addWidget(self.pushButton_draw_cluster)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.groupBox_3 = QGroupBox(GroupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_6 = QSpacerItem(74, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)

        self.pushButton_save_bc_per_cluster = QPushButton(self.groupBox_3)
        self.pushButton_save_bc_per_cluster.setObjectName(u"pushButton_save_bc_per_cluster")

        self.horizontalLayout.addWidget(self.pushButton_save_bc_per_cluster)

        self.pushButton_draw_bc_per_cluster = QPushButton(self.groupBox_3)
        self.pushButton_draw_bc_per_cluster.setObjectName(u"pushButton_draw_bc_per_cluster")

        self.horizontalLayout.addWidget(self.pushButton_draw_bc_per_cluster)


        self.verticalLayout_2.addWidget(self.groupBox_3)


        self.retranslateUi(GroupBox)

        QMetaObject.connectSlotsByName(GroupBox)
    # setupUi

    def retranslateUi(self, GroupBox):
        GroupBox.setWindowTitle(QCoreApplication.translate("GroupBox", u"GroupBox", None))
        self.groupBox.setTitle(QCoreApplication.translate("GroupBox", u"Find all clusters", None))
        self.pushButton_save_clusters.setText(QCoreApplication.translate("GroupBox", u"Compute", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("GroupBox", u"Analyze specific cluster", None))
        self.label.setText(QCoreApplication.translate("GroupBox", u"root", None))
        self.lineEdit_node_picker1.setPlaceholderText(QCoreApplication.translate("GroupBox", u"(pick node)", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("GroupBox", u"root", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("GroupBox", u"intermediate", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("GroupBox", u"anchors", None))

        self.lineEdit.setText("")
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("GroupBox", u"color", None))
        self.pushButton_save_cluster.setText(QCoreApplication.translate("GroupBox", u"Compute", None))
        self.pushButton_draw_cluster.setText(QCoreApplication.translate("GroupBox", u"Plot", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("GroupBox", u"Distribution of cluster size vs. betweenness centrality ", None))
        self.pushButton_save_bc_per_cluster.setText(QCoreApplication.translate("GroupBox", u"Compute", None))
        self.pushButton_draw_bc_per_cluster.setText(QCoreApplication.translate("GroupBox", u"Plot", None))
    # retranslateUi

