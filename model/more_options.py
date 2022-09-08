# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'more_options.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QLabel, QLineEdit, QRadioButton,
    QSizePolicy, QTextBrowser, QVBoxLayout, QWidget)

class Ui_More_Dialog(object):
    def setupUi(self, More_Dialog):
        if not More_Dialog.objectName():
            More_Dialog.setObjectName(u"More_Dialog")
        More_Dialog.resize(562, 480)
        icon = QIcon()
        icon.addFile(u"../../icon/favicon.ico", QSize(), QIcon.Normal, QIcon.Off)
        More_Dialog.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(More_Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textBrowser = QTextBrowser(More_Dialog)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout_2.addWidget(self.textBrowser)

        self.widget = QWidget(More_Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.checkBox = QCheckBox(self.widget)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.widget)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.widget)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout.addWidget(self.checkBox_3)

        self.checkBox_4 = QCheckBox(self.widget)
        self.checkBox_4.setObjectName(u"checkBox_4")

        self.verticalLayout.addWidget(self.checkBox_4)

        self.checkBox_5 = QCheckBox(self.widget)
        self.checkBox_5.setObjectName(u"checkBox_5")

        self.verticalLayout.addWidget(self.checkBox_5)

        self.checkBox_6 = QCheckBox(self.widget)
        self.checkBox_6.setObjectName(u"checkBox_6")

        self.verticalLayout.addWidget(self.checkBox_6)

        self.checkBox_7 = QCheckBox(self.widget)
        self.checkBox_7.setObjectName(u"checkBox_7")

        self.verticalLayout.addWidget(self.checkBox_7)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.widget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setEnabled(False)

        self.verticalLayout.addWidget(self.lineEdit)

        self.radioButton = QRadioButton(self.widget)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setEnabled(False)

        self.verticalLayout.addWidget(self.radioButton)


        self.verticalLayout_2.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(More_Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(More_Dialog)
        self.buttonBox.accepted.connect(More_Dialog.accept)
        self.buttonBox.rejected.connect(More_Dialog.reject)

        QMetaObject.connectSlotsByName(More_Dialog)
    # setupUi

    def retranslateUi(self, More_Dialog):
        More_Dialog.setWindowTitle(QCoreApplication.translate("More_Dialog", u"More Options", None))
        self.checkBox.setText(QCoreApplication.translate("More_Dialog", u"write description", None))
        self.checkBox_2.setText(QCoreApplication.translate("More_Dialog", u"write meta data", None))
        self.checkBox_3.setText(QCoreApplication.translate("More_Dialog", u"write comments", None))
        self.checkBox_4.setText(QCoreApplication.translate("More_Dialog", u"only audio (need ffmpeg)", None))
        self.checkBox_5.setText(QCoreApplication.translate("More_Dialog", u"write thumbnail", None))
        self.checkBox_6.setText(QCoreApplication.translate("More_Dialog", u"skip download video", None))
        self.checkBox_7.setText(QCoreApplication.translate("More_Dialog", u"write subs", None))
        self.label.setText(QCoreApplication.translate("More_Dialog", u"sub langs", None))
        self.radioButton.setText(QCoreApplication.translate("More_Dialog", u"embed subs", None))
    # retranslateUi

