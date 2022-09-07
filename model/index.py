# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'index.ui'
##
## Created by: Qt User Interface Compiler version 6.0.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(712, 534)
        MainWindow.setAcceptDrops(False)
        icon = QIcon()
        icon.addFile(u"./icon/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.actionyoutube_dl = QAction(MainWindow)
        self.actionyoutube_dl.setObjectName(u"actionyoutube_dl")
        self.actionsettings = QAction(MainWindow)
        self.actionsettings.setObjectName(u"actionsettings")
        self.actionsettings.setCheckable(False)
        self.actionsettings.setChecked(False)
        self.actiontxt = QAction(MainWindow)
        self.actiontxt.setObjectName(u"actiontxt")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 4, 0, 1, 4)

        self.radioButton = QRadioButton(self.centralwidget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setCheckable(True)
        self.radioButton.setChecked(True)

        self.gridLayout.addWidget(self.radioButton, 3, 0, 1, 2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setAutoDefault(False)
        self.pushButton.setFlat(False)

        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 4)

        self.radioButton_2 = QRadioButton(self.centralwidget)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout.addWidget(self.radioButton_2, 3, 2, 1, 1)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 4)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 712, 22))
        self.menubar.setStyleSheet(u"")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.actionyoutube_dl)

        self.retranslateUi(MainWindow)

        self.pushButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"yt-dlp GUI", None))
        self.actionyoutube_dl.setText(QCoreApplication.translate("MainWindow", u"yt-dlp settings", None))
        self.actionsettings.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.actiontxt.setText(QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"directly", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"more options", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"URL(List):", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"settings", None))
    # retranslateUi

