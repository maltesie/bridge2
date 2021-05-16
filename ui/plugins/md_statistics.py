# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'md_statistics.ui'
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

