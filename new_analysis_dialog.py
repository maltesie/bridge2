# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_analysis_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.resize(787, 713)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.verticalLayout_4 = QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.group_init = QGroupBox(Dialog)
        self.group_init.setObjectName(u"group_init")
        self.verticalLayout = QVBoxLayout(self.group_init)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.group_init)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)

        self.line_bonds_structure = QLineEdit(self.group_init)
        self.line_bonds_structure.setObjectName(u"line_bonds_structure")

        self.gridLayout_2.addWidget(self.line_bonds_structure, 0, 1, 1, 1)

        self.label_3 = QLabel(self.group_init)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.checkBox_bonds_donors_without_hydrogen = QCheckBox(self.group_init)
        self.checkBox_bonds_donors_without_hydrogen.setObjectName(u"checkBox_bonds_donors_without_hydrogen")

        self.gridLayout_2.addWidget(self.checkBox_bonds_donors_without_hydrogen, 0, 2, 1, 1)

        self.button_structure = QPushButton(self.group_init)
        self.button_structure.setObjectName(u"button_structure")
        self.button_structure.setText(u"Browse...")

        self.gridLayout_2.addWidget(self.button_structure, 0, 3, 1, 1)

        self.line_bonds_trajectories = QLineEdit(self.group_init)
        self.line_bonds_trajectories.setObjectName(u"line_bonds_trajectories")

        self.gridLayout_2.addWidget(self.line_bonds_trajectories, 1, 1, 1, 2)

        self.button_trajectories = QPushButton(self.group_init)
        self.button_trajectories.setObjectName(u"button_trajectories")
        self.button_trajectories.setText(u"Browse...")

        self.gridLayout_2.addWidget(self.button_trajectories, 1, 3, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.verticalLayout_4.addWidget(self.group_init)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_4.addWidget(self.label_8)

        self.line_bonds_selection = QLineEdit(self.groupBox)
        self.line_bonds_selection.setObjectName(u"line_bonds_selection")

        self.horizontalLayout_4.addWidget(self.line_bonds_selection)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.checkBox_residuewise = QCheckBox(self.groupBox)
        self.checkBox_residuewise.setObjectName(u"checkBox_residuewise")
        self.checkBox_residuewise.setChecked(True)

        self.verticalLayout_5.addWidget(self.checkBox_residuewise)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_8.addWidget(self.label_14)

        self.checkBox_all_nitrogen = QCheckBox(self.groupBox)
        self.checkBox_all_nitrogen.setObjectName(u"checkBox_all_nitrogen")

        self.horizontalLayout_8.addWidget(self.checkBox_all_nitrogen)

        self.checkBox_all_oxygen = QCheckBox(self.groupBox)
        self.checkBox_all_oxygen.setObjectName(u"checkBox_all_oxygen")

        self.horizontalLayout_8.addWidget(self.checkBox_all_oxygen)

        self.checkBox_all_sulphur = QCheckBox(self.groupBox)
        self.checkBox_all_sulphur.setObjectName(u"checkBox_all_sulphur")

        self.horizontalLayout_8.addWidget(self.checkBox_all_sulphur)

        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_8.addWidget(self.label_13)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)


        self.verticalLayout_5.addLayout(self.horizontalLayout_8)

        self.checkBox_consider_backbone = QCheckBox(self.groupBox)
        self.checkBox_consider_backbone.setObjectName(u"checkBox_consider_backbone")

        self.verticalLayout_5.addWidget(self.checkBox_consider_backbone)


        self.verticalLayout_3.addLayout(self.verticalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBox_5 = QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.horizontalLayout = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.line_bonds_start = QLineEdit(self.groupBox_5)
        self.line_bonds_start.setObjectName(u"line_bonds_start")
        self.line_bonds_start.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.line_bonds_start)

        self.label_7 = QLabel(self.groupBox_5)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout.addWidget(self.label_7)

        self.line_bonds_stop = QLineEdit(self.groupBox_5)
        self.line_bonds_stop.setObjectName(u"line_bonds_stop")
        self.line_bonds_stop.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.line_bonds_stop)

        self.label_54 = QLabel(self.groupBox_5)
        self.label_54.setObjectName(u"label_54")

        self.horizontalLayout.addWidget(self.label_54)

        self.line_bonds_step = QLineEdit(self.groupBox_5)
        self.line_bonds_step.setObjectName(u"line_bonds_step")
        self.line_bonds_step.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout.addWidget(self.line_bonds_step)


        self.horizontalLayout_7.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.groupBox)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.groupBox_6)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_4)

        self.line_bonds_distance = QLineEdit(self.groupBox_6)
        self.line_bonds_distance.setObjectName(u"line_bonds_distance")
        self.line_bonds_distance.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.line_bonds_distance)

        self.checkBox_angle = QCheckBox(self.groupBox_6)
        self.checkBox_angle.setObjectName(u"checkBox_angle")
        self.checkBox_angle.setChecked(True)

        self.horizontalLayout_2.addWidget(self.checkBox_angle)

        self.line_bonds_angle = QLineEdit(self.groupBox_6)
        self.line_bonds_angle.setObjectName(u"line_bonds_angle")
        self.line_bonds_angle.setMaximumSize(QSize(60, 16777215))

        self.horizontalLayout_2.addWidget(self.line_bonds_angle)


        self.horizontalLayout_7.addWidget(self.groupBox_6)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_15 = QGroupBox(Dialog)
        self.groupBox_15.setObjectName(u"groupBox_15")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_15)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.radio_in_selection = QRadioButton(self.groupBox_15)
        self.radio_in_selection.setObjectName(u"radio_in_selection")
        self.radio_in_selection.setChecked(True)

        self.verticalLayout_2.addWidget(self.radio_in_selection)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.radio_around = QRadioButton(self.groupBox_15)
        self.radio_around.setObjectName(u"radio_around")

        self.horizontalLayout_12.addWidget(self.radio_around)

        self.line_around_value = QLineEdit(self.groupBox_15)
        self.line_around_value.setObjectName(u"line_around_value")
        self.line_around_value.setMaximumSize(QSize(50, 16777215))
        self.line_around_value.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_12.addWidget(self.line_around_value)

        self.label = QLabel(self.groupBox_15)
        self.label.setObjectName(u"label")

        self.horizontalLayout_12.addWidget(self.label)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_7)

        self.checkBox_not_water_water = QCheckBox(self.groupBox_15)
        self.checkBox_not_water_water.setObjectName(u"checkBox_not_water_water")
        self.checkBox_not_water_water.setChecked(True)

        self.horizontalLayout_12.addWidget(self.checkBox_not_water_water)


        self.verticalLayout_2.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.radio_wire_dict = QRadioButton(self.groupBox_15)
        self.radio_wire_dict.setObjectName(u"radio_wire_dict")
        self.radio_wire_dict.setChecked(False)

        self.horizontalLayout_6.addWidget(self.radio_wire_dict)

        self.line_wire_max_water = QLineEdit(self.groupBox_15)
        self.line_wire_max_water.setObjectName(u"line_wire_max_water")
        self.line_wire_max_water.setMaximumSize(QSize(50, 16777215))
        self.line_wire_max_water.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_6.addWidget(self.line_wire_max_water)

        self.label_5 = QLabel(self.groupBox_15)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_6.addWidget(self.label_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.checkBox_wires_allow_direct_bonds = QCheckBox(self.groupBox_15)
        self.checkBox_wires_allow_direct_bonds.setObjectName(u"checkBox_wires_allow_direct_bonds")

        self.horizontalLayout_6.addWidget(self.checkBox_wires_allow_direct_bonds)

        self.checkBo_wires_convex = QCheckBox(self.groupBox_15)
        self.checkBo_wires_convex.setObjectName(u"checkBo_wires_convex")

        self.horizontalLayout_6.addWidget(self.checkBo_wires_convex)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, 0, -1, -1)
        self.radioButton_hydrophobic_contacts = QRadioButton(self.groupBox_15)
        self.radioButton_hydrophobic_contacts.setObjectName(u"radioButton_hydrophobic_contacts")

        self.horizontalLayout_5.addWidget(self.radioButton_hydrophobic_contacts)

        self.lineEdit_hydrophobic_distance = QLineEdit(self.groupBox_15)
        self.lineEdit_hydrophobic_distance.setObjectName(u"lineEdit_hydrophobic_distance")
        self.lineEdit_hydrophobic_distance.setMaximumSize(QSize(50, 16777215))
        self.lineEdit_hydrophobic_distance.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.lineEdit_hydrophobic_distance)

        self.label_12 = QLabel(self.groupBox_15)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_5.addWidget(self.label_12)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)

        self.checkBox_partially_hydrophobic = QCheckBox(self.groupBox_15)
        self.checkBox_partially_hydrophobic.setObjectName(u"checkBox_partially_hydrophobic")

        self.horizontalLayout_5.addWidget(self.checkBox_partially_hydrophobic)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_4.addWidget(self.groupBox_15)

        self.groupBox_4 = QGroupBox(Dialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.checkBox_frame_time = QCheckBox(self.groupBox_4)
        self.checkBox_frame_time.setObjectName(u"checkBox_frame_time")

        self.horizontalLayout_13.addWidget(self.checkBox_frame_time)

        self.lineEdit_frame_time = QLineEdit(self.groupBox_4)
        self.lineEdit_frame_time.setObjectName(u"lineEdit_frame_time")
        self.lineEdit_frame_time.setMaximumSize(QSize(60, 16777215))
        self.lineEdit_frame_time.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_13.addWidget(self.lineEdit_frame_time)

        self.comboBox_frame_time_unit = QComboBox(self.groupBox_4)
        self.comboBox_frame_time_unit.addItem("")
        self.comboBox_frame_time_unit.addItem("")
        self.comboBox_frame_time_unit.addItem("")
        self.comboBox_frame_time_unit.addItem("")
        self.comboBox_frame_time_unit.setObjectName(u"comboBox_frame_time_unit")
        self.comboBox_frame_time_unit.setEnabled(True)
        self.comboBox_frame_time_unit.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_13.addWidget(self.comboBox_frame_time_unit)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_11)


        self.verticalLayout_8.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_10 = QLabel(self.groupBox_4)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_14.addWidget(self.label_10)

        self.lineEdit_add_residue = QLineEdit(self.groupBox_4)
        self.lineEdit_add_residue.setObjectName(u"lineEdit_add_residue")
        self.lineEdit_add_residue.setMaximumSize(QSize(60, 16777215))
        self.lineEdit_add_residue.setLayoutDirection(Qt.LeftToRight)
        self.lineEdit_add_residue.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_14.addWidget(self.lineEdit_add_residue)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_20)


        self.verticalLayout_8.addLayout(self.horizontalLayout_14)


        self.verticalLayout_4.addWidget(self.groupBox_4)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_2)

        self.button_cancel = QPushButton(Dialog)
        self.button_cancel.setObjectName(u"button_cancel")

        self.horizontalLayout_11.addWidget(self.button_cancel)

        self.button_load = QPushButton(Dialog)
        self.button_load.setObjectName(u"button_load")

        self.horizontalLayout_11.addWidget(self.button_load)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"New Analysis", None))
        self.group_init.setTitle(QCoreApplication.translate("Dialog", u"Files", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"structure", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_structure.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">A structure file (.psf or .pdb or other) has to be provided.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_structure.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"trajectories", None))
#if QT_CONFIG(tooltip)
        self.checkBox_bonds_donors_without_hydrogen.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>For structure files, that do not contain hydrogen atoms.</p><p align=\"justify\">This option turns off the angle check in the H bond detection and uses all possible donors regardless of their protonation state. If set to false, only protonated donors are considered.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_bonds_donors_without_hydrogen.setText(QCoreApplication.translate("Dialog", u"crystal structure", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_trajectories.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">One or more trajectory files (.dcd or other) can be provided opionally.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_trajectories.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Search", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"static selection", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_selection.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">Provide a static selection. It will not be updated and cant contain timedependent parts.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_selection.setText(QCoreApplication.translate("Dialog", u"protein", None))
        self.line_bonds_selection.setPlaceholderText(QCoreApplication.translate("Dialog", u"e.g. protein (default)", None))
        self.checkBox_residuewise.setText(QCoreApplication.translate("Dialog", u"compute residuewise", None))
        self.label_14.setText(QCoreApplication.translate("Dialog", u"include all ", None))
        self.checkBox_all_nitrogen.setText(QCoreApplication.translate("Dialog", u"N*", None))
        self.checkBox_all_oxygen.setText(QCoreApplication.translate("Dialog", u"O*", None))
        self.checkBox_all_sulphur.setText(QCoreApplication.translate("Dialog", u"S*", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u" atoms as donors and acceptors", None))
        self.checkBox_consider_backbone.setText(QCoreApplication.translate("Dialog", u"include backbone atoms", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("Dialog", u"Frames", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"first", None))
        self.line_bonds_start.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"last", None))
        self.line_bonds_stop.setText(QCoreApplication.translate("Dialog", u"-1", None))
        self.label_54.setText(QCoreApplication.translate("Dialog", u"stride", None))
        self.line_bonds_step.setText(QCoreApplication.translate("Dialog", u"1", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("Dialog", u"H-bond criteria", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"distance", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_distance.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">The maximum distance between an acceptor heavy atom and a donor heavy atom.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_distance.setText(QCoreApplication.translate("Dialog", u"3.5", None))
#if QT_CONFIG(tooltip)
        self.checkBox_angle.setToolTip(QCoreApplication.translate("Dialog", u"Toggle angle check.", None))
#endif // QT_CONFIG(tooltip)
        self.checkBox_angle.setText(QCoreApplication.translate("Dialog", u"angle", None))
#if QT_CONFIG(tooltip)
        self.line_bonds_angle.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">The maximum angle between the line connecting the donor heavy atom and the hydrogen and the line connecting the acceptor heavy atom and the hydrogen. An angle of 0 relates to a straight line through donor-hydrogen-acceptor.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.line_bonds_angle.setText(QCoreApplication.translate("Dialog", u"60", None))
        self.groupBox_15.setTitle(QCoreApplication.translate("Dialog", u"Algorithm", None))
#if QT_CONFIG(tooltip)
        self.radio_in_selection.setToolTip(QCoreApplication.translate("Dialog", u"Compute all H bonds within the static selection.", None))
#endif // QT_CONFIG(tooltip)
        self.radio_in_selection.setText(QCoreApplication.translate("Dialog", u"H-bonds in static selection", None))
#if QT_CONFIG(tooltip)
        self.radio_around.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">Compute all H bonds within the union of the static selection and all water within the specified distance of the static selection.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radio_around.setText(QCoreApplication.translate("Dialog", u"H-bonds in static selection and water around", None))
#if QT_CONFIG(tooltip)
        self.line_around_value.setToolTip(QCoreApplication.translate("Dialog", u"Set the distance around the static selection for dynamic water detection.", None))
#endif // QT_CONFIG(tooltip)
        self.line_around_value.setText(QCoreApplication.translate("Dialog", u"3.5", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"[A]", None))
        self.checkBox_not_water_water.setText(QCoreApplication.translate("Dialog", u"no water-water H-bonds", None))
#if QT_CONFIG(tooltip)
        self.radio_wire_dict.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"justify\">Both algorithms result in the same. Choose dictionary for smaller systems and compressed sparse matrix for larger systems for efficiency.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.radio_wire_dict.setText(QCoreApplication.translate("Dialog", u"water wires with max.", None))
        self.line_wire_max_water.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"waters ", None))
        self.checkBox_wires_allow_direct_bonds.setText(QCoreApplication.translate("Dialog", u"direct H-bonds", None))
        self.checkBo_wires_convex.setText(QCoreApplication.translate("Dialog", u"convex hull", None))
        self.radioButton_hydrophobic_contacts.setText(QCoreApplication.translate("Dialog", u"hydrophobic contacts within ", None))
        self.lineEdit_hydrophobic_distance.setText(QCoreApplication.translate("Dialog", u"5.0", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"[A]", None))
        self.checkBox_partially_hydrophobic.setText(QCoreApplication.translate("Dialog", u"Add hydrophobic segments of polar/charged residues", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Additional Options", None))
        self.checkBox_frame_time.setText(QCoreApplication.translate("Dialog", u"set time between two frames:", None))
        self.comboBox_frame_time_unit.setItemText(0, QCoreApplication.translate("Dialog", u"ns", None))
        self.comboBox_frame_time_unit.setItemText(1, QCoreApplication.translate("Dialog", u"ps", None))
        self.comboBox_frame_time_unit.setItemText(2, QCoreApplication.translate("Dialog", u"fs", None))
        self.comboBox_frame_time_unit.setItemText(3, QCoreApplication.translate("Dialog", u"as", None))

        self.label_10.setText(QCoreApplication.translate("Dialog", u"Declare offset for n-terminal residue: ", None))
        self.lineEdit_add_residue.setText(QCoreApplication.translate("Dialog", u"0", None))
        self.button_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.button_load.setText(QCoreApplication.translate("Dialog", u"Initialize", None))
    # retranslateUi

