# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'atom_names.ui'
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
        Dialog.resize(627, 339)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plainTextEdit_acceptors = QPlainTextEdit(self.groupBox)
        self.plainTextEdit_acceptors.setObjectName(u"plainTextEdit_acceptors")

        self.verticalLayout.addWidget(self.plainTextEdit_acceptors)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plainTextEdit_donors = QPlainTextEdit(self.groupBox_2)
        self.plainTextEdit_donors.setObjectName(u"plainTextEdit_donors")

        self.verticalLayout_2.addWidget(self.plainTextEdit_donors)


        self.horizontalLayout_2.addWidget(self.groupBox_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.groupBox_3 = QGroupBox(Dialog)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_water = QLineEdit(self.groupBox_3)
        self.lineEdit_water.setObjectName(u"lineEdit_water")

        self.horizontalLayout_3.addWidget(self.lineEdit_water)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(Dialog)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.groupBox_4)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.lineEdit_threads = QLineEdit(self.groupBox_4)
        self.lineEdit_threads.setObjectName(u"lineEdit_threads")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_threads.sizePolicy().hasHeightForWidth())
        self.lineEdit_threads.setSizePolicy(sizePolicy)
        self.lineEdit_threads.setMinimumSize(QSize(60, 0))

        self.horizontalLayout_4.addWidget(self.lineEdit_threads)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_cancel = QPushButton(Dialog)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")

        self.horizontalLayout.addWidget(self.pushButton_cancel)

        self.pushButton_reset = QPushButton(Dialog)
        self.pushButton_reset.setObjectName(u"pushButton_reset")

        self.horizontalLayout.addWidget(self.pushButton_reset)

        self.pushButton_save = QPushButton(Dialog)
        self.pushButton_save.setObjectName(u"pushButton_save")

        self.horizontalLayout.addWidget(self.pushButton_save)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Additional Options", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Acceptor atom names", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Donor atom names", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Dialog", u"Water oxygen selection", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Dialog", u"Additional settings", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Threads", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pushButton_reset.setText(QCoreApplication.translate("Dialog", u"Default", None))
        self.pushButton_save.setText(QCoreApplication.translate("Dialog", u"Save", None))
    # retranslateUi

