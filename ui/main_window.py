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
    QMainWindow, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1110, 894)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(0, 0, 1071, 881))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.widget_control_panel = QWidget(self.horizontalLayoutWidget)
        self.widget_control_panel.setObjectName(u"widget_control_panel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_control_panel.sizePolicy().hasHeightForWidth())
        self.widget_control_panel.setSizePolicy(sizePolicy1)
        self.widget_control_panel.setCursor(QCursor(Qt.ArrowCursor))
        self.widget_control_panel.setAutoFillBackground(False)
        self.gridLayoutWidget = QWidget(self.widget_control_panel)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 0, 202, 871))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.label_show_gens = QLabel(self.gridLayoutWidget)
        self.label_show_gens.setObjectName(u"label_show_gens")
        self.label_show_gens.setEnabled(True)
        self.label_show_gens.setMaximumSize(QSize(82, 36))

        self.gridLayout.addWidget(self.label_show_gens, 7, 1, 1, 1)

        self.checkBox_show_tail = QCheckBox(self.gridLayoutWidget)
        self.checkBox_show_tail.setObjectName(u"checkBox_show_tail")

        self.gridLayout.addWidget(self.checkBox_show_tail, 12, 0, 1, 1)

        self.pushButton_clear_tail = QPushButton(self.gridLayoutWidget)
        self.pushButton_clear_tail.setObjectName(u"pushButton_clear_tail")

        self.gridLayout.addWidget(self.pushButton_clear_tail, 12, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_4, 15, 0, 1, 2)

        self.pushButton_clean_surface = QPushButton(self.gridLayoutWidget)
        self.pushButton_clean_surface.setObjectName(u"pushButton_clean_surface")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.pushButton_clean_surface.sizePolicy().hasHeightForWidth())
        self.pushButton_clean_surface.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.pushButton_clean_surface, 0, 0, 1, 2)

        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.label, 8, 0, 1, 1)

        self.comboBox_board_pattern = QComboBox(self.gridLayoutWidget)
        self.comboBox_board_pattern.setObjectName(u"comboBox_board_pattern")

        self.gridLayout.addWidget(self.comboBox_board_pattern, 11, 1, 1, 1)

        self.pushButton_start = QPushButton(self.gridLayoutWidget)
        self.pushButton_start.setObjectName(u"pushButton_start")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.pushButton_start.sizePolicy().hasHeightForWidth())
        self.pushButton_start.setSizePolicy(sizePolicy4)

        self.gridLayout.addWidget(self.pushButton_start, 1, 0, 1, 2)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)

        self.lineEdit_cell_size = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_cell_size.setObjectName(u"lineEdit_cell_size")

        self.gridLayout.addWidget(self.lineEdit_cell_size, 10, 1, 1, 1)

        self.label_current_status = QLabel(self.gridLayoutWidget)
        self.label_current_status.setObjectName(u"label_current_status")

        self.gridLayout.addWidget(self.label_current_status, 5, 1, 1, 1)

        self.pushButton_random_gen = QPushButton(self.gridLayoutWidget)
        self.pushButton_random_gen.setObjectName(u"pushButton_random_gen")

        self.gridLayout.addWidget(self.pushButton_random_gen, 3, 0, 1, 2)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout.addWidget(self.label_7, 11, 0, 1, 1)

        self.pushButton_stop = QPushButton(self.gridLayoutWidget)
        self.pushButton_stop.setObjectName(u"pushButton_stop")

        self.gridLayout.addWidget(self.pushButton_stop, 2, 0, 1, 2)

        self.checkBox_trace_1_gen = QCheckBox(self.gridLayoutWidget)
        self.checkBox_trace_1_gen.setObjectName(u"checkBox_trace_1_gen")

        self.gridLayout.addWidget(self.checkBox_trace_1_gen, 13, 0, 1, 2)

        self.pushButton_next_step = QPushButton(self.gridLayoutWidget)
        self.pushButton_next_step.setObjectName(u"pushButton_next_step")

        self.gridLayout.addWidget(self.pushButton_next_step, 4, 0, 1, 2)

        self.lineEdit_random_ratio = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_random_ratio.setObjectName(u"lineEdit_random_ratio")

        self.gridLayout.addWidget(self.lineEdit_random_ratio, 9, 1, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 10, 0, 1, 1)

        self.lineEdit_gens_per_sec = QLineEdit(self.gridLayoutWidget)
        self.lineEdit_gens_per_sec.setObjectName(u"lineEdit_gens_per_sec")

        self.gridLayout.addWidget(self.lineEdit_gens_per_sec, 8, 1, 1, 1)

        self.checkBox_show_grid = QCheckBox(self.gridLayoutWidget)
        self.checkBox_show_grid.setObjectName(u"checkBox_show_grid")

        self.gridLayout.addWidget(self.checkBox_show_grid, 14, 0, 1, 2)

        self.checkBox_trace_1_gen.raise_()
        self.checkBox_show_tail.raise_()
        self.pushButton_stop.raise_()
        self.pushButton_start.raise_()
        self.label_4.raise_()
        self.pushButton_random_gen.raise_()
        self.pushButton_clear_tail.raise_()
        self.pushButton_clean_surface.raise_()
        self.label_3.raise_()
        self.label_current_status.raise_()
        self.label.raise_()
        self.lineEdit_gens_per_sec.raise_()
        self.pushButton_next_step.raise_()
        self.label_5.raise_()
        self.lineEdit_random_ratio.raise_()
        self.label_6.raise_()
        self.lineEdit_cell_size.raise_()
        self.comboBox_board_pattern.raise_()
        self.label_7.raise_()
        self.label_2.raise_()
        self.label_show_gens.raise_()
        self.checkBox_show_grid.raise_()
        self.widget = QWidget(self.widget_control_panel)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(230, 50, 800, 800))
        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 801, 801))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.widget_control_panel)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_show_gens.setText("")
        self.checkBox_show_tail.setText(QCoreApplication.translate("MainWindow", u"Show tail", None))
        self.pushButton_clear_tail.setText(QCoreApplication.translate("MainWindow", u"clear tail", None))
        self.label_4.setText("")
        self.pushButton_clean_surface.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"FPS:", None))
        self.pushButton_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"GenNum:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"State:", None))
        self.label_current_status.setText("")
        self.pushButton_random_gen.setText(QCoreApplication.translate("MainWindow", u"Random initialization", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"border mode:", None))
        self.pushButton_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.checkBox_trace_1_gen.setText(QCoreApplication.translate("MainWindow", u"Leave traces after death", None))
        self.pushButton_next_step.setText(QCoreApplication.translate("MainWindow", u"Next generation", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Random ratio:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Cell size:", None))
        self.checkBox_show_grid.setText(QCoreApplication.translate("MainWindow", u"Show grid", None))
    # retranslateUi

