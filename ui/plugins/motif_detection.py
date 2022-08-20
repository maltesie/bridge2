# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'motif_detection.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_GroupBox(object):
    def setupUi(self, GroupBox):
        if not GroupBox.objectName():
            GroupBox.setObjectName(u"GroupBox")
        GroupBox.resize(452, 296)
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

        self.checkBox_asp_backbone = QCheckBox(self.groupBox)
        self.checkBox_asp_backbone.setObjectName(u"checkBox_asp_backbone")

        self.verticalLayout_2.addWidget(self.checkBox_asp_backbone)


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
        self.checkBox_glu_his.setText(QCoreApplication.translate("GroupBox", u"Asp/Glu carboxylate oxygen - His ND1 or NE2", None))
        self.checkBox_his_his.setText(QCoreApplication.translate("GroupBox", u"His ND1 or NE2 - His ND1 or NE2", None))
        self.checkBox_asp_asn.setText(QCoreApplication.translate("GroupBox", u"Asp/Glu carboxylate oxygen - Asn ND1 or OD2", None))
        self.checkBox_his_ser.setText(QCoreApplication.translate("GroupBox", u"His ND1 or NE2 - Ser/Thr hydroxyl oxygen", None))
        self.checkBox_asp_backbone.setText(QCoreApplication.translate("GroupBox", u"Asp/Glu carboxylate oxygen - backbone", None))
    # retranslateUi

