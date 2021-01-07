# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uifiles/preferences.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName("Preferences")
        Preferences.resize(355, 392)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../usr/share/htmleditor/resources/htmledit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Preferences.setWindowIcon(icon)
        self.fontBttn = QtWidgets.QPushButton(Preferences)
        self.fontBttn.setGeometry(QtCore.QRect(80, 60, 181, 51))
        self.fontBttn.setObjectName("fontBttn")
        self.webBttn = QtWidgets.QPushButton(Preferences)
        self.webBttn.setGeometry(QtCore.QRect(80, 120, 181, 51))
        self.webBttn.setObjectName("webBttn")
        self.label = QtWidgets.QLabel(Preferences)
        self.label.setGeometry(QtCore.QRect(80, 14, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.quitBttn = QtWidgets.QPushButton(Preferences)
        self.quitBttn.setGeometry(QtCore.QRect(80, 300, 181, 51))
        self.quitBttn.setObjectName("quitBttn")
        self.htmlBttn = QtWidgets.QPushButton(Preferences)
        self.htmlBttn.setGeometry(QtCore.QRect(80, 180, 181, 51))
        self.htmlBttn.setObjectName("htmlBttn")
        self.cssBttn = QtWidgets.QPushButton(Preferences)
        self.cssBttn.setGeometry(QtCore.QRect(80, 240, 181, 51))
        self.cssBttn.setObjectName("cssBttn")

        self.retranslateUi(Preferences)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        _translate = QtCore.QCoreApplication.translate
        Preferences.setWindowTitle(_translate("Preferences", "HTML Editor Preferences"))
        self.fontBttn.setText(_translate("Preferences", "Font"))
        self.webBttn.setText(_translate("Preferences", "Web Browser"))
        self.label.setText(_translate("Preferences", "Prerferences"))
        self.quitBttn.setText(_translate("Preferences", "Quit"))
        self.htmlBttn.setText(_translate("Preferences", "HTML Colors"))
        self.cssBttn.setText(_translate("Preferences", "CSS Colors"))

