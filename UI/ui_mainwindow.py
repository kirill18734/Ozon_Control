# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'application.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(550, 400)
        MainWindow.setMinimumSize(QSize(550, 400))
        MainWindow.setMaximumSize(QSize(550, 400))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMaximumSize(QSize(16777215, 16777215))
        self.centralwidget.setStyleSheet(u"")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 550, 400))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.label_text_select_printer = QLabel(self.frame)
        self.label_text_select_printer.setObjectName(u"label_text_select_printer")
        self.label_text_select_printer.setGeometry(QRect(20, 100, 211, 31))
        font = QFont()
        font.setPointSize(14)
        self.label_text_select_printer.setFont(font)
        self.label_text_select_printer.setStyleSheet(u"width:100%;")
        self.label_text_select_printer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lable_title_printer = QLabel(self.frame)
        self.lable_title_printer.setObjectName(u"lable_title_printer")
        self.lable_title_printer.setGeometry(QRect(10, 60, 521, 31))
        self.lable_title_printer.setMinimumSize(QSize(400, 0))
        self.lable_title_printer.setFont(font)
        self.lable_title_printer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title_window = QLabel(self.frame)
        self.label_title_window.setObjectName(u"label_title_window")
        self.label_title_window.setGeometry(QRect(19, 145, 511, 41))
        font1 = QFont()
        font1.setPointSize(14)
        font1.setKerning(True)
        self.label_title_window.setFont(font1)
        self.label_title_window.setStyleSheet(u"")
        self.label_title_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(490, 10, 41, 41))
        self.pushButton.setStyleSheet(u"")
        self.label_error_show = QLabel(self.frame)
        self.label_error_show.setObjectName(u"label_error_show")
        self.label_error_show.setGeometry(QRect(30, 40, 211, 20))
        self.label_error_show.setStyleSheet(u"color:red;")
        self.label_error_show.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_error_printer = QLabel(self.frame)
        self.label_error_printer.setObjectName(u"label_error_printer")
        self.label_error_printer.setGeometry(QRect(30, 20, 211, 20))
        self.label_error_printer.setStyleSheet(u"color:red;")
        self.label_error_printer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.select_printer = QComboBox(self.frame)
        self.select_printer.setObjectName(u"select_printer")
        self.select_printer.setGeometry(QRect(260, 100, 271, 31))
        self.select_printer.setMinimumSize(QSize(250, 0))
        self.btn_show = QPushButton(self.frame)
        self.btn_show.setObjectName(u"btn_show")
        self.btn_show.setGeometry(QRect(10, 190, 241, 100))
        self.btn_show.setMinimumSize(QSize(0, 100))
        self.btn_show.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setPointSize(10)
        self.btn_show.setFont(font2)
        self.btn_change = QPushButton(self.frame)
        self.btn_change.setObjectName(u"btn_change")
        self.btn_change.setGeometry(QRect(260, 190, 281, 100))
        self.btn_change.setMinimumSize(QSize(0, 100))
        self.btn_change.setMaximumSize(QSize(16777215, 16777215))
        self.btn_change.setFont(font2)
        self.label_title_format_number = QLabel(self.frame)
        self.label_title_format_number.setObjectName(u"label_title_format_number")
        self.label_title_format_number.setGeometry(QRect(10, 290, 511, 41))
        self.label_title_format_number.setFont(font1)
        self.label_title_format_number.setStyleSheet(u"")
        self.label_title_format_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.select_format_number = QComboBox(self.frame)
        self.select_format_number.setObjectName(u"select_format_number")
        self.select_format_number.setGeometry(QRect(260, 330, 271, 31))
        self.select_format_number.setMinimumSize(QSize(250, 0))
        self.label_text_select_format_number = QLabel(self.frame)
        self.label_text_select_format_number.setObjectName(u"label_text_select_format_number")
        self.label_text_select_format_number.setGeometry(QRect(0, 330, 251, 31))
        self.label_text_select_format_number.setFont(font)
        self.label_text_select_format_number.setStyleSheet(u"width:100%;")
        self.label_text_select_format_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        MainWindow.setCentralWidget(self.centralwidget)

        # self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043c\u043e\u043d\u0438\u0442\u043e\u0440\u0438\u043d\u0433\u0430 \u044d\u043a\u0440\u0430\u043d\u0430 \u0438 \u043f\u0435\u0447\u0430\u0442\u0438", None))
        self.label_text_select_printer.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u043e\u0440 \u043f\u0440\u0438\u043d\u0442\u0435\u0440\u0430", None))
        self.lable_title_printer.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043d\u0442\u0435\u0440", None))
        self.label_title_window.setText(QCoreApplication.translate("MainWindow", u" \u041e\u0431\u043b\u0430\u0441\u0442\u044c \u044d\u043a\u0440\u0430\u043d\u0430", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\ud83c\udf19 ", None))
        self.label_error_show.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043b\u0430\u0441\u0442\u044c \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u043d\u0438\u044f \u043d\u0435 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0430", None))
        self.label_error_printer.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043d\u0442\u0435\u0440 \u043d\u0435 \u0443\u043a\u0430\u0437\u0430\u043d", None))
        self.btn_show.setText(QCoreApplication.translate("MainWindow", u"\ud83d\udd0d \u041f\u043e\u043a\u0430\u0437\u0430\u0442\u044c \u0442\u0435\u043a\u0443\u0449\u0443\u044e \u043e\u0431\u043b\u0430\u0441\u0442\u044c ", None))
        self.btn_change.setText(QCoreApplication.translate("MainWindow", u"\u270f \u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c \u043e\u0431\u043b\u0430\u0441\u0442\u044c \u043e\u0442\u0441\u043b\u0435\u0436\u0438\u0432\u0430\u043d\u0438\u044f", None))
        self.label_title_format_number.setText(QCoreApplication.translate("MainWindow", u"\u0424\u043e\u0440\u043c\u0430\u0442 \u043f\u043e\u0438\u0441\u043a\u0430 \u043d\u043e\u043c\u0435\u0440\u0430", None))
        self.label_text_select_format_number.setText(QCoreApplication.translate("MainWindow", u"\u041a\u0430\u043a\u043e\u0439 \u0444\u043e\u0440\u043c\u0430\u0442 \u043d\u043e\u043c\u0435\u0440\u0430 \u0438\u0449\u0435\u043c", None))
    # retranslateUi

