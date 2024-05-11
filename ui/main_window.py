# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1192, 894)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_control_panel = QWidget(self.centralwidget)
        self.widget_control_panel.setObjectName(u"widget_control_panel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_control_panel.sizePolicy().hasHeightForWidth())
        self.widget_control_panel.setSizePolicy(sizePolicy1)
        self.widget_control_panel.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_control_panel.setAutoFillBackground(False)
        self.widget_control_panel.setStyleSheet(u"")
        self.horizontalLayoutWidget_2 = QWidget(self.widget_control_panel)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(0, 0, 201, 761))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.label_2 = QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 12, 0, 1, 1)

        self.pushButton_next_step = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_next_step.setObjectName(u"pushButton_next_step")

        self.gridLayout.addWidget(self.pushButton_next_step, 4, 0, 1, 2)

        self.label_6 = QLabel(self.horizontalLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 15, 0, 1, 1)

        self.lineEdit_cell_size = QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_cell_size.setObjectName(u"lineEdit_cell_size")

        self.gridLayout.addWidget(self.lineEdit_cell_size, 15, 1, 1, 1)

        self.pushButton_clean_surface = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_clean_surface.setObjectName(u"pushButton_clean_surface")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.pushButton_clean_surface.sizePolicy().hasHeightForWidth())
        self.pushButton_clean_surface.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.pushButton_clean_surface, 0, 0, 1, 2)

        self.label_show_gens = QLabel(self.horizontalLayoutWidget_2)
        self.label_show_gens.setObjectName(u"label_show_gens")
        self.label_show_gens.setEnabled(True)
        self.label_show_gens.setMaximumSize(QSize(82, 36))

        self.gridLayout.addWidget(self.label_show_gens, 12, 1, 1, 1)

        self.label = QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label, 13, 0, 1, 1)

        self.lineEdit_random_ratio = QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_random_ratio.setObjectName(u"lineEdit_random_ratio")

        self.gridLayout.addWidget(self.lineEdit_random_ratio, 14, 1, 1, 1)

        self.label_current_status = QLabel(self.horizontalLayoutWidget_2)
        self.label_current_status.setObjectName(u"label_current_status")

        self.gridLayout.addWidget(self.label_current_status, 10, 1, 1, 1)

        self.label_5 = QLabel(self.horizontalLayoutWidget_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 14, 0, 1, 1)

        self.label_7 = QLabel(self.horizontalLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 16, 0, 1, 1)

        self.lineEdit_surface_width = QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_surface_width.setObjectName(u"lineEdit_surface_width")

        self.gridLayout.addWidget(self.lineEdit_surface_width, 8, 1, 1, 1)

        self.pushButton_clear_tail = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_clear_tail.setObjectName(u"pushButton_clear_tail")

        self.gridLayout.addWidget(self.pushButton_clear_tail, 17, 1, 1, 1)

        self.pushButton_start = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_start.setObjectName(u"pushButton_start")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_start.sizePolicy().hasHeightForWidth())
        self.pushButton_start.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.pushButton_start, 1, 0, 1, 2)

        self.pushButton_stop = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.gridLayout.addWidget(self.pushButton_stop, 2, 0, 1, 2)

        self.label_3 = QLabel(self.horizontalLayoutWidget_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 10, 0, 1, 1)

        self.comboBox_board_pattern = QComboBox(self.horizontalLayoutWidget_2)
        self.comboBox_board_pattern.setObjectName(u"comboBox_board_pattern")

        self.gridLayout.addWidget(self.comboBox_board_pattern, 16, 1, 1, 1)

        self.checkBox_show_tail = QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_show_tail.setObjectName(u"checkBox_show_tail")

        self.gridLayout.addWidget(self.checkBox_show_tail, 17, 0, 1, 1)

        self.label_8 = QLabel(self.horizontalLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 8, 0, 1, 1)

        self.pushButton_random_gen = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_random_gen.setObjectName(u"pushButton_random_gen")

        self.gridLayout.addWidget(self.pushButton_random_gen, 3, 0, 1, 2)

        self.checkBox_trace_1_gen = QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_trace_1_gen.setObjectName(u"checkBox_trace_1_gen")

        self.gridLayout.addWidget(self.checkBox_trace_1_gen, 18, 0, 1, 2)

        self.pushButton_reset_surface_position = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton_reset_surface_position.setObjectName(u"pushButton_reset_surface_position")

        self.gridLayout.addWidget(self.pushButton_reset_surface_position, 5, 0, 1, 2)

        self.checkBox_show_grid = QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_show_grid.setObjectName(u"checkBox_show_grid")

        self.gridLayout.addWidget(self.checkBox_show_grid, 19, 0, 1, 2)

        self.lineEdit_gens_per_sec = QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_gens_per_sec.setObjectName(u"lineEdit_gens_per_sec")

        self.gridLayout.addWidget(self.lineEdit_gens_per_sec, 13, 1, 1, 1)

        self.label_9 = QLabel(self.horizontalLayoutWidget_2)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 9, 0, 1, 1)

        self.lineEdit_surface_height = QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit_surface_height.setObjectName(u"lineEdit_surface_height")

        self.gridLayout.addWidget(self.lineEdit_surface_height, 9, 1, 1, 1)

        self.label_4 = QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.label_4, 20, 0, 1, 2)


        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.gridLayout_2.addWidget(self.widget_control_panel, 0, 0, 1, 1)

        self.widget_draw_area = QWidget(self.centralwidget)
        self.widget_draw_area.setObjectName(u"widget_draw_area")
        self.widget_draw_area.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.widget_draw_area, 0, 1, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)
        self.gridLayout_2.setColumnStretch(1, 200)
        self.gridLayout_2.setColumnMinimumWidth(0, 200)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"GenNum:", None))
        self.pushButton_next_step.setText(QCoreApplication.translate("MainWindow", u"Next generation", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Grid size:", None))
        self.pushButton_clean_surface.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.label_show_gens.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"FPS:", None))
        self.label_current_status.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Random ratio:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"border mode:", None))
        self.pushButton_clear_tail.setText(QCoreApplication.translate("MainWindow", u"clear tail", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"State:", None))
        self.checkBox_show_tail.setText(QCoreApplication.translate("MainWindow", u"Show tail", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Width:", None))
        self.pushButton_random_gen.setText(QCoreApplication.translate("MainWindow", u"Random initialization", None))
        self.checkBox_trace_1_gen.setText(QCoreApplication.translate("MainWindow", u"Leave traces after death", None))
        self.pushButton_reset_surface_position.setText(QCoreApplication.translate("MainWindow", u"Reset surface position", None))
        self.checkBox_show_grid.setText(QCoreApplication.translate("MainWindow", u"Show grid", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Height:", None))
        self.label_4.setText("")
    # retranslateUi

