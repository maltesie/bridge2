# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'centrality.ui'
##
## Created by: Qt User Interface Compiler version 5.15.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


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

