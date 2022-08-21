# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1638, 967)
        icon = QIcon()
        icon.addFile(u":/icons/bridge.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        icon1 = QIcon()
        icon1.addFile(u":/icons/new.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionNew.setIcon(icon1)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        icon2 = QIcon()
        icon2.addFile(u":/icons/open.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        icon3 = QIcon()
        icon3.addFile(u":/icons/save.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave.setIcon(icon3)
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName(u"actionSaveAs")
        icon4 = QIcon()
        icon4.addFile(u":/icons/save-as.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSaveAs.setIcon(icon4)
        self.actionEditParameter = QAction(MainWindow)
        self.actionEditParameter.setObjectName(u"actionEditParameter")
        self.actionLoadSecond = QAction(MainWindow)
        self.actionLoadSecond.setObjectName(u"actionLoadSecond")
        icon5 = QIcon()
        icon5.addFile(u":/icons/compare.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionLoadSecond.setIcon(icon5)
        self.actionDocumentation = QAction(MainWindow)
        self.actionDocumentation.setObjectName(u"actionDocumentation")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionToolbar = QAction(MainWindow)
        self.actionToolbar.setObjectName(u"actionToolbar")
        self.actionToolbar.setCheckable(True)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionAddComputationPlugin = QAction(MainWindow)
        self.actionAddComputationPlugin.setObjectName(u"actionAddComputationPlugin")
        self.actionDefaultAtomNames = QAction(MainWindow)
        self.actionDefaultAtomNames.setObjectName(u"actionDefaultAtomNames")
        self.actionShowAtoms = QAction(MainWindow)
        self.actionShowAtoms.setObjectName(u"actionShowAtoms")
        self.actionExport_Analysis_Summary = QAction(MainWindow)
        self.actionExport_Analysis_Summary.setObjectName(u"actionExport_Analysis_Summary")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_5 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.layout_interactive = QVBoxLayout()
        self.layout_interactive.setObjectName(u"layout_interactive")
        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.layout_interactive.addItem(self.horizontalSpacer_12)


        self.horizontalLayout_5.addLayout(self.layout_interactive)

        self.toolBox = QToolBox(self.centralwidget)
        self.toolBox.setObjectName(u"toolBox")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QSize(520, 0))
        self.toolBox.setMaximumSize(QSize(520, 16777215))
        self.toolBoxPage_layout = QWidget()
        self.toolBoxPage_layout.setObjectName(u"toolBoxPage_layout")
        self.toolBoxPage_layout.setGeometry(QRect(0, 0, 532, 738))
        self.verticalLayout_3 = QVBoxLayout(self.toolBoxPage_layout)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_3 = QGroupBox(self.toolBoxPage_layout)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.radioButton_rotation_pca = QRadioButton(self.groupBox_3)
        self.radioButton_rotation_pca.setObjectName(u"radioButton_rotation_pca")
        self.radioButton_rotation_pca.setChecked(True)

        self.horizontalLayout_12.addWidget(self.radioButton_rotation_pca)

        self.radioButton_rotation_zy = QRadioButton(self.groupBox_3)
        self.radioButton_rotation_zy.setObjectName(u"radioButton_rotation_zy")

        self.horizontalLayout_12.addWidget(self.radioButton_rotation_zy)

        self.radioButton_rotation_xy = QRadioButton(self.groupBox_3)
        self.radioButton_rotation_xy.setObjectName(u"radioButton_rotation_xy")

        self.horizontalLayout_12.addWidget(self.radioButton_rotation_xy)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_9)


        self.verticalLayout_5.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_15.addWidget(self.label_2)

        self.horizontalSlider_frame = QScrollBar(self.groupBox_3)
        self.horizontalSlider_frame.setObjectName(u"horizontalSlider_frame")
        self.horizontalSlider_frame.setMinimumSize(QSize(300, 0))
        self.horizontalSlider_frame.setOrientation(Qt.Horizontal)

        self.horizontalLayout_15.addWidget(self.horizontalSlider_frame)

        self.label_frame = QLabel(self.groupBox_3)
        self.label_frame.setObjectName(u"label_frame")

        self.horizontalLayout_15.addWidget(self.label_frame)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_10)


        self.verticalLayout_5.addLayout(self.horizontalLayout_15)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_colors = QGroupBox(self.toolBoxPage_layout)
        self.groupBox_colors.setObjectName(u"groupBox_colors")
        self.verticalLayout = QVBoxLayout(self.groupBox_colors)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton_colors = QRadioButton(self.groupBox_colors)
        self.radioButton_colors.setObjectName(u"radioButton_colors")
        self.radioButton_colors.setChecked(True)

        self.horizontalLayout.addWidget(self.radioButton_colors)

        self.comboBox_segnames = QComboBox(self.groupBox_colors)
        self.comboBox_segnames.setObjectName(u"comboBox_segnames")

        self.horizontalLayout.addWidget(self.comboBox_segnames)

        self.comboBox_colors = QComboBox(self.groupBox_colors)
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.addItem("")
        self.comboBox_colors.setObjectName(u"comboBox_colors")

        self.horizontalLayout.addWidget(self.comboBox_colors)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_14)

        self.checkBox_segnames_legend = QCheckBox(self.groupBox_colors)
        self.checkBox_segnames_legend.setObjectName(u"checkBox_segnames_legend")
        self.checkBox_segnames_legend.setChecked(True)

        self.horizontalLayout.addWidget(self.checkBox_segnames_legend)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.radioButton_color = QRadioButton(self.groupBox_colors)
        self.radioButton_color.setObjectName(u"radioButton_color")
        self.radioButton_color.setChecked(False)

        self.horizontalLayout_3.addWidget(self.radioButton_color)

        self.comboBox_single_color = QComboBox(self.groupBox_colors)
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.addItem("")
        self.comboBox_single_color.setObjectName(u"comboBox_single_color")

        self.horizontalLayout_3.addWidget(self.comboBox_single_color)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_13)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.groupBox_centralities = QGroupBox(self.groupBox_colors)
        self.groupBox_centralities.setObjectName(u"groupBox_centralities")
        self.groupBox_centralities.setCheckable(False)
        self.groupBox_centralities.setChecked(False)
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_centralities)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, -1, -1)
        self.radioButton_betweenness = QRadioButton(self.groupBox_centralities)
        self.radioButton_betweenness.setObjectName(u"radioButton_betweenness")
        self.radioButton_betweenness.setEnabled(True)

        self.horizontalLayout_9.addWidget(self.radioButton_betweenness)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_18)

        self.checkBox_color_legend = QCheckBox(self.groupBox_centralities)
        self.checkBox_color_legend.setObjectName(u"checkBox_color_legend")
        self.checkBox_color_legend.setChecked(True)

        self.horizontalLayout_9.addWidget(self.checkBox_color_legend)


        self.verticalLayout_8.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, -1, -1)
        self.radioButton_degree = QRadioButton(self.groupBox_centralities)
        self.radioButton_degree.setObjectName(u"radioButton_degree")
        self.radioButton_degree.setEnabled(True)

        self.horizontalLayout_2.addWidget(self.radioButton_degree)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_17)

        self.checkBox_centralities_norm = QCheckBox(self.groupBox_centralities)
        self.checkBox_centralities_norm.setObjectName(u"checkBox_centralities_norm")

        self.horizontalLayout_2.addWidget(self.checkBox_centralities_norm)


        self.verticalLayout_8.addLayout(self.horizontalLayout_2)


        self.verticalLayout.addWidget(self.groupBox_centralities)


        self.verticalLayout_3.addWidget(self.groupBox_colors)

        self.groupBox = QGroupBox(self.toolBoxPage_layout)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_10.addWidget(self.label_3)

        self.horizontalSlider_nodes = QSlider(self.groupBox)
        self.horizontalSlider_nodes.setObjectName(u"horizontalSlider_nodes")
        self.horizontalSlider_nodes.setSliderPosition(50)
        self.horizontalSlider_nodes.setOrientation(Qt.Horizontal)

        self.horizontalLayout_10.addWidget(self.horizontalSlider_nodes)

        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_19)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, 0, -1, -1)
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_13.addWidget(self.label_6)

        self.horizontalSlider_edges = QSlider(self.groupBox)
        self.horizontalSlider_edges.setObjectName(u"horizontalSlider_edges")
        self.horizontalSlider_edges.setValue(50)
        self.horizontalSlider_edges.setOrientation(Qt.Horizontal)

        self.horizontalLayout_13.addWidget(self.horizontalSlider_edges)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, 0, -1, -1)
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_14.addWidget(self.label_7)

        self.horizontalSlider_labels = QSlider(self.groupBox)
        self.horizontalSlider_labels.setObjectName(u"horizontalSlider_labels")
        self.horizontalSlider_labels.setValue(50)
        self.horizontalSlider_labels.setOrientation(Qt.Horizontal)

        self.horizontalLayout_14.addWidget(self.horizontalSlider_labels)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_11)


        self.verticalLayout_7.addLayout(self.horizontalLayout_14)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.toolBoxPage_layout)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_7.addWidget(self.label_4)

        self.checkBox_bonds_graph_labels = QCheckBox(self.groupBox_2)
        self.checkBox_bonds_graph_labels.setObjectName(u"checkBox_bonds_graph_labels")
        self.checkBox_bonds_graph_labels.setChecked(True)

        self.horizontalLayout_7.addWidget(self.checkBox_bonds_graph_labels)

        self.checkBox_white = QCheckBox(self.groupBox_2)
        self.checkBox_white.setObjectName(u"checkBox_white")

        self.horizontalLayout_7.addWidget(self.checkBox_white)

        self.horizontalSpacer_15 = QSpacerItem(461, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_15)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_8.addWidget(self.label_5)

        self.checkBox_bonds_occupancy = QCheckBox(self.groupBox_2)
        self.checkBox_bonds_occupancy.setObjectName(u"checkBox_bonds_occupancy")

        self.horizontalLayout_8.addWidget(self.checkBox_bonds_occupancy)

        self.checkBox_bonds_endurance = QCheckBox(self.groupBox_2)
        self.checkBox_bonds_endurance.setObjectName(u"checkBox_bonds_endurance")

        self.horizontalLayout_8.addWidget(self.checkBox_bonds_endurance)

        self.checkBox_nb_water = QCheckBox(self.groupBox_2)
        self.checkBox_nb_water.setObjectName(u"checkBox_nb_water")
        self.checkBox_nb_water.setEnabled(False)

        self.horizontalLayout_8.addWidget(self.checkBox_nb_water)

        self.horizontalSpacer = QSpacerItem(52, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_8)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.toolBox.addItem(self.toolBoxPage_layout, u"Layout")
        self.toolBoxPage_filters = QWidget()
        self.toolBoxPage_filters.setObjectName(u"toolBoxPage_filters")
        self.toolBoxPage_filters.setGeometry(QRect(0, 0, 660, 738))
        self.verticalLayout_4 = QVBoxLayout(self.toolBoxPage_filters)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_6)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_current_filter = QLabel(self.toolBoxPage_filters)
        self.label_current_filter.setObjectName(u"label_current_filter")

        self.horizontalLayout_4.addWidget(self.label_current_filter)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.pushButton_remove_filter = QPushButton(self.toolBoxPage_filters)
        self.pushButton_remove_filter.setObjectName(u"pushButton_remove_filter")

        self.horizontalLayout_4.addWidget(self.pushButton_remove_filter)

        self.pushButton_apply_filter = QPushButton(self.toolBoxPage_filters)
        self.pushButton_apply_filter.setObjectName(u"pushButton_apply_filter")

        self.horizontalLayout_4.addWidget(self.pushButton_apply_filter)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        self.groupBox_occupancy = QGroupBox(self.toolBoxPage_filters)
        self.groupBox_occupancy.setObjectName(u"groupBox_occupancy")
        self.groupBox_occupancy.setCheckable(True)
        self.groupBox_occupancy.setChecked(False)
        self.horizontalLayout_18 = QHBoxLayout(self.groupBox_occupancy)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_45 = QLabel(self.groupBox_occupancy)
        self.label_45.setObjectName(u"label_45")

        self.horizontalLayout_18.addWidget(self.label_45)

        self.line_bonds_occupancy = QLineEdit(self.groupBox_occupancy)
        self.line_bonds_occupancy.setObjectName(u"line_bonds_occupancy")
        self.line_bonds_occupancy.setMinimumSize(QSize(50, 0))
        self.line_bonds_occupancy.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_18.addWidget(self.line_bonds_occupancy)

        self.horizontalSpacer_32 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_32)


        self.verticalLayout_4.addWidget(self.groupBox_occupancy)

        self.groupBox_connected = QGroupBox(self.toolBoxPage_filters)
        self.groupBox_connected.setObjectName(u"groupBox_connected")
        self.groupBox_connected.setCheckable(True)
        self.groupBox_connected.setChecked(False)
        self.gridLayout_30 = QGridLayout(self.groupBox_connected)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.label_48 = QLabel(self.groupBox_connected)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_30.addWidget(self.label_48, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_30.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)

        self.line_bonds_connected_root = QLineEdit(self.groupBox_connected)
        self.line_bonds_connected_root.setObjectName(u"line_bonds_connected_root")
        self.line_bonds_connected_root.setMinimumSize(QSize(180, 0))
        self.line_bonds_connected_root.setMaximumSize(QSize(180, 16777215))

        self.gridLayout_30.addWidget(self.line_bonds_connected_root, 0, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_connected)

        self.groupBox_shortest_paths = QGroupBox(self.toolBoxPage_filters)
        self.groupBox_shortest_paths.setObjectName(u"groupBox_shortest_paths")
        self.groupBox_shortest_paths.setCheckable(True)
        self.groupBox_shortest_paths.setChecked(False)
        self.gridLayout_27 = QGridLayout(self.groupBox_shortest_paths)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.line_bonds_path_goal = QLineEdit(self.groupBox_shortest_paths)
        self.line_bonds_path_goal.setObjectName(u"line_bonds_path_goal")
        self.line_bonds_path_goal.setMinimumSize(QSize(180, 0))
        self.line_bonds_path_goal.setMaximumSize(QSize(180, 16777215))

        self.gridLayout_27.addWidget(self.line_bonds_path_goal, 1, 2, 1, 1)

        self.label_46 = QLabel(self.groupBox_shortest_paths)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_27.addWidget(self.label_46, 1, 1, 1, 1)

        self.line_bonds_path_root = QLineEdit(self.groupBox_shortest_paths)
        self.line_bonds_path_root.setObjectName(u"line_bonds_path_root")
        self.line_bonds_path_root.setMinimumSize(QSize(180, 0))
        self.line_bonds_path_root.setMaximumSize(QSize(180, 16777215))

        self.gridLayout_27.addWidget(self.line_bonds_path_root, 0, 2, 1, 1)

        self.label_47 = QLabel(self.groupBox_shortest_paths)
        self.label_47.setObjectName(u"label_47")

        self.gridLayout_27.addWidget(self.label_47, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_27.addItem(self.horizontalSpacer_6, 0, 3, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_shortest_paths)

        self.groupBox_specific_path = QGroupBox(self.toolBoxPage_filters)
        self.groupBox_specific_path.setObjectName(u"groupBox_specific_path")
        self.groupBox_specific_path.setCheckable(True)
        self.groupBox_specific_path.setChecked(False)
        self.gridLayout_29 = QGridLayout(self.groupBox_specific_path)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_29.addItem(self.horizontalSpacer_7, 0, 1, 1, 1)

        self.lineEdit_specific_path = QLineEdit(self.groupBox_specific_path)
        self.lineEdit_specific_path.setObjectName(u"lineEdit_specific_path")
        self.lineEdit_specific_path.setMinimumSize(QSize(400, 0))

        self.gridLayout_29.addWidget(self.lineEdit_specific_path, 0, 0, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_specific_path)

        self.groupBox_between_segments = QGroupBox(self.toolBoxPage_filters)
        self.groupBox_between_segments.setObjectName(u"groupBox_between_segments")
        self.groupBox_between_segments.setCheckable(True)
        self.groupBox_between_segments.setChecked(False)
        self.gridLayout_9 = QGridLayout(self.groupBox_between_segments)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.groupBox_10 = QGroupBox(self.groupBox_between_segments)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_13 = QGridLayout(self.groupBox_10)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.line_bonds_filter_resida = QLineEdit(self.groupBox_10)
        self.line_bonds_filter_resida.setObjectName(u"line_bonds_filter_resida")

        self.gridLayout_13.addWidget(self.line_bonds_filter_resida, 2, 0, 1, 2)

        self.comboBox_filter_segna = QComboBox(self.groupBox_10)
        self.comboBox_filter_segna.setObjectName(u"comboBox_filter_segna")

        self.gridLayout_13.addWidget(self.comboBox_filter_segna, 1, 0, 1, 1)

        self.comboBox_filter_resna = QComboBox(self.groupBox_10)
        self.comboBox_filter_resna.setObjectName(u"comboBox_filter_resna")

        self.gridLayout_13.addWidget(self.comboBox_filter_resna, 1, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_10)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_13.addWidget(self.label_8, 0, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox_10)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_13.addWidget(self.label_9, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_10, 1, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_8, 1, 2, 1, 1)

        self.groupBox_11 = QGroupBox(self.groupBox_between_segments)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.gridLayout_14 = QGridLayout(self.groupBox_11)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.line_bonds_filter_residb = QLineEdit(self.groupBox_11)
        self.line_bonds_filter_residb.setObjectName(u"line_bonds_filter_residb")

        self.gridLayout_14.addWidget(self.line_bonds_filter_residb, 2, 0, 1, 2)

        self.comboBox_filter_resnb = QComboBox(self.groupBox_11)
        self.comboBox_filter_resnb.setObjectName(u"comboBox_filter_resnb")

        self.gridLayout_14.addWidget(self.comboBox_filter_resnb, 1, 1, 1, 1)

        self.comboBox_filter_segnb = QComboBox(self.groupBox_11)
        self.comboBox_filter_segnb.setObjectName(u"comboBox_filter_segnb")

        self.gridLayout_14.addWidget(self.comboBox_filter_segnb, 1, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox_11)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_14.addWidget(self.label_10, 0, 0, 1, 1)

        self.label_11 = QLabel(self.groupBox_11)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_14.addWidget(self.label_11, 0, 1, 1, 1)


        self.gridLayout_9.addWidget(self.groupBox_11, 1, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.groupBox_between_segments)

        self.checkBox_selected_nodes = QCheckBox(self.toolBoxPage_filters)
        self.checkBox_selected_nodes.setObjectName(u"checkBox_selected_nodes")

        self.verticalLayout_4.addWidget(self.checkBox_selected_nodes)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.toolBox.addItem(self.toolBoxPage_filters, u"Filters")
        self.toolBoxPage_computations = QWidget()
        self.toolBoxPage_computations.setObjectName(u"toolBoxPage_computations")
        self.toolBoxPage_computations.setGeometry(QRect(0, 0, 520, 752))
        self.verticalLayout_6 = QVBoxLayout(self.toolBoxPage_computations)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label = QLabel(self.toolBoxPage_computations)
        self.label.setObjectName(u"label")

        self.horizontalLayout_11.addWidget(self.label)

        self.comboBox_plugins = QComboBox(self.toolBoxPage_computations)
        self.comboBox_plugins.setObjectName(u"comboBox_plugins")

        self.horizontalLayout_11.addWidget(self.comboBox_plugins)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_2)


        self.verticalLayout_6.addLayout(self.horizontalLayout_11)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.verticalLayout_plugin = QVBoxLayout()
        self.verticalLayout_plugin.setObjectName(u"verticalLayout_plugin")

        self.verticalLayout_6.addLayout(self.verticalLayout_plugin)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_3)

        self.toolBox.addItem(self.toolBoxPage_computations, u"Computations and Plots")

        self.horizontalLayout_5.addWidget(self.toolBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1638, 31))
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuEdit.addAction(self.actionEditParameter)
        self.menuEdit.addAction(self.actionDefaultAtomNames)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionAddComputationPlugin)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionShowAtoms)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_Analysis_Summary)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSaveAs)
        self.toolBar.addSeparator()

        self.retranslateUi(MainWindow)

        self.comboBox_filter_segna.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Bridge", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New...", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open...", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionSaveAs.setText(QCoreApplication.translate("MainWindow", u"Save As...", None))
        self.actionEditParameter.setText(QCoreApplication.translate("MainWindow", u"Analysis parameter", None))
        self.actionLoadSecond.setText(QCoreApplication.translate("MainWindow", u"Load second analysis", None))
        self.actionDocumentation.setText(QCoreApplication.translate("MainWindow", u"Documentation", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"Bridge on github", None))
        self.actionToolbar.setText(QCoreApplication.translate("MainWindow", u"Toolbar", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionAddComputationPlugin.setText(QCoreApplication.translate("MainWindow", u"Add computation plugin", None))
        self.actionDefaultAtomNames.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.actionShowAtoms.setText(QCoreApplication.translate("MainWindow", u"Current parameters", None))
        self.actionExport_Analysis_Summary.setText(QCoreApplication.translate("MainWindow", u"Export Analysis Summary", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Projection plane", None))
        self.radioButton_rotation_pca.setText(QCoreApplication.translate("MainWindow", u"best view PCA plane", None))
        self.radioButton_rotation_zy.setText(QCoreApplication.translate("MainWindow", u"ZY plane", None))
        self.radioButton_rotation_xy.setText(QCoreApplication.translate("MainWindow", u"XY plane", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"frame", None))
        self.label_frame.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.groupBox_colors.setTitle(QCoreApplication.translate("MainWindow", u"Colors", None))
        self.radioButton_colors.setText(QCoreApplication.translate("MainWindow", u"per segment", None))
        self.comboBox_colors.setItemText(0, QCoreApplication.translate("MainWindow", u"seagreen", None))
        self.comboBox_colors.setItemText(1, QCoreApplication.translate("MainWindow", u"red", None))
        self.comboBox_colors.setItemText(2, QCoreApplication.translate("MainWindow", u"blue", None))
        self.comboBox_colors.setItemText(3, QCoreApplication.translate("MainWindow", u"yellow", None))
        self.comboBox_colors.setItemText(4, QCoreApplication.translate("MainWindow", u"grey", None))
        self.comboBox_colors.setItemText(5, QCoreApplication.translate("MainWindow", u"lightblue", None))
        self.comboBox_colors.setItemText(6, QCoreApplication.translate("MainWindow", u"orange", None))
        self.comboBox_colors.setItemText(7, QCoreApplication.translate("MainWindow", u"maroon", None))
        self.comboBox_colors.setItemText(8, QCoreApplication.translate("MainWindow", u"olive", None))
        self.comboBox_colors.setItemText(9, QCoreApplication.translate("MainWindow", u"skyblue", None))
        self.comboBox_colors.setItemText(10, QCoreApplication.translate("MainWindow", u"pink", None))
        self.comboBox_colors.setItemText(11, QCoreApplication.translate("MainWindow", u"silver", None))
        self.comboBox_colors.setItemText(12, QCoreApplication.translate("MainWindow", u"peru", None))
        self.comboBox_colors.setItemText(13, QCoreApplication.translate("MainWindow", u"fuchsia", None))
        self.comboBox_colors.setItemText(14, QCoreApplication.translate("MainWindow", u"lavender", None))

        self.checkBox_segnames_legend.setText(QCoreApplication.translate("MainWindow", u"legend", None))
        self.radioButton_color.setText(QCoreApplication.translate("MainWindow", u"single color", None))
        self.comboBox_single_color.setItemText(0, QCoreApplication.translate("MainWindow", u"seagreen", None))
        self.comboBox_single_color.setItemText(1, QCoreApplication.translate("MainWindow", u"red", None))
        self.comboBox_single_color.setItemText(2, QCoreApplication.translate("MainWindow", u"blue", None))
        self.comboBox_single_color.setItemText(3, QCoreApplication.translate("MainWindow", u"yellow", None))
        self.comboBox_single_color.setItemText(4, QCoreApplication.translate("MainWindow", u"grey", None))
        self.comboBox_single_color.setItemText(5, QCoreApplication.translate("MainWindow", u"lightblue", None))
        self.comboBox_single_color.setItemText(6, QCoreApplication.translate("MainWindow", u"orange", None))
        self.comboBox_single_color.setItemText(7, QCoreApplication.translate("MainWindow", u"maroon", None))
        self.comboBox_single_color.setItemText(8, QCoreApplication.translate("MainWindow", u"olive", None))
        self.comboBox_single_color.setItemText(9, QCoreApplication.translate("MainWindow", u"skyblue", None))
        self.comboBox_single_color.setItemText(10, QCoreApplication.translate("MainWindow", u"pink", None))
        self.comboBox_single_color.setItemText(11, QCoreApplication.translate("MainWindow", u"silver", None))
        self.comboBox_single_color.setItemText(12, QCoreApplication.translate("MainWindow", u"peru", None))
        self.comboBox_single_color.setItemText(13, QCoreApplication.translate("MainWindow", u"fuchsia", None))
        self.comboBox_single_color.setItemText(14, QCoreApplication.translate("MainWindow", u"lavender", None))

        self.groupBox_centralities.setTitle(QCoreApplication.translate("MainWindow", u"centrality measures", None))
        self.radioButton_betweenness.setText(QCoreApplication.translate("MainWindow", u"betweenness centrality", None))
        self.checkBox_color_legend.setText(QCoreApplication.translate("MainWindow", u"legend", None))
        self.radioButton_degree.setText(QCoreApplication.translate("MainWindow", u"degree centrality", None))
        self.checkBox_centralities_norm.setText(QCoreApplication.translate("MainWindow", u"normalized", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Sizes", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"nodes:             ", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"edges:             ", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"edge labels:   ", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Labels", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"nodes: ", None))
#if QT_CONFIG(tooltip)
        self.checkBox_bonds_graph_labels.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Toggle the use of residue names and numbers as labels.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_bonds_graph_labels.setText(QCoreApplication.translate("MainWindow", u"residue names", None))
        self.checkBox_white.setText(QCoreApplication.translate("MainWindow", u"white background", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"edges: ", None))
#if QT_CONFIG(tooltip)
        self.checkBox_bonds_occupancy.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Toggle the use of H bond occupancies as edge labels in the 2D visualization.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_bonds_occupancy.setText(QCoreApplication.translate("MainWindow", u"occupancy", None))
        self.checkBox_bonds_endurance.setText(QCoreApplication.translate("MainWindow", u"endurance time", None))
        self.checkBox_nb_water.setText(QCoreApplication.translate("MainWindow", u"# waters", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage_layout), QCoreApplication.translate("MainWindow", u"Layout", None))
        self.label_current_filter.setText(QCoreApplication.translate("MainWindow", u"current filter: none", None))
        self.pushButton_remove_filter.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.pushButton_apply_filter.setText(QCoreApplication.translate("MainWindow", u"Apply", None))
        self.groupBox_occupancy.setTitle(QCoreApplication.translate("MainWindow", u"Occupancy", None))
        self.label_45.setText(QCoreApplication.translate("MainWindow", u"minimum value", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_occupancy.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Filter for water wires with an occupancy greater than the minimum value.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_occupancy.setText("")
        self.groupBox_connected.setTitle(QCoreApplication.translate("MainWindow", u"Connected Component Analysis", None))
        self.label_48.setText(QCoreApplication.translate("MainWindow", u"root    ", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_connected_root.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Filter the graph of water wires for all nodes that can be reached from a root node.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_connected_root.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(pick node)", None))
        self.groupBox_shortest_paths.setTitle(QCoreApplication.translate("MainWindow", u"All Shortest Paths", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_path_goal.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Filter the water wire graph for all shortest paths between a root node and a target node.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_path_goal.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(pick node)", None))
        self.label_46.setText(QCoreApplication.translate("MainWindow", u"target", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_path_root.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"justify\">Filter the water wire graph for all shortest paths between a root node and a target node.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_path_root.setText("")
        self.line_bonds_path_root.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(pick node)", None))
        self.label_47.setText(QCoreApplication.translate("MainWindow", u"root", None))
        self.groupBox_specific_path.setTitle(QCoreApplication.translate("MainWindow", u"Specific Path", None))
        self.lineEdit_specific_path.setPlaceholderText(QCoreApplication.translate("MainWindow", u"(pick nodes)", None))
        self.groupBox_between_segments.setTitle(QCoreApplication.translate("MainWindow", u"Within Section or Between Sections", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"section 1", None))
        self.line_bonds_filter_resida.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ids, e.g. 20-40, 55, 60-70", None))
        self.comboBox_filter_segna.setCurrentText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"segname", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"resname", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"section 2", None))
        self.line_bonds_filter_residb.setText("")
        self.line_bonds_filter_residb.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ids, e.g. 20-40, 55, 60-70", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"segname", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"resname", None))
        self.checkBox_selected_nodes.setText(QCoreApplication.translate("MainWindow", u"Selected Nodes", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage_filters), QCoreApplication.translate("MainWindow", u"Filters", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Select plugin:", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage_computations), QCoreApplication.translate("MainWindow", u"Computations and Plots", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"About", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

