# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uifiles/stylecolors.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StyleColors(object):
    def setupUi(self, StyleColors):
        StyleColors.setObjectName("StyleColors")
        StyleColors.resize(516, 486)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../transtext/resources/Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StyleColors.setWindowIcon(icon)
        self.styleList = QtWidgets.QListWidget(StyleColors)
        self.styleList.setGeometry(QtCore.QRect(240, 40, 256, 381))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.styleList.setFont(font)
        self.styleList.setObjectName("styleList")
        self.label = QtWidgets.QLabel(StyleColors)
        self.label.setGeometry(QtCore.QRect(0, 40, 231, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.colorBttn = QtWidgets.QPushButton(StyleColors)
        self.colorBttn.setGeometry(QtCore.QRect(40, 130, 145, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.colorBttn.setFont(font)
        self.colorBttn.setObjectName("colorBttn")
        self.closeBttn = QtWidgets.QPushButton(StyleColors)
        self.closeBttn.setGeometry(QtCore.QRect(40, 230, 145, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.closeBttn.setFont(font)
        self.closeBttn.setObjectName("closeBttn")
        self.resetBttn = QtWidgets.QPushButton(StyleColors)
        self.resetBttn.setGeometry(QtCore.QRect(40, 330, 145, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.resetBttn.setFont(font)
        self.resetBttn.setObjectName("resetBttn")

        self.retranslateUi(StyleColors)
        QtCore.QMetaObject.connectSlotsByName(StyleColors)

    def retranslateUi(self, StyleColors):
        _translate = QtCore.QCoreApplication.translate
        StyleColors.setWindowTitle(_translate("StyleColors", "HTML Editor -- Style Changer"))
        self.label.setText(_translate("StyleColors", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'DejaVu Sans\'; font-weight:600;\">HTML Editor</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'DejaVu Sans\'; font-weight:600;\">Style Changer</span></p></body></html>"))
        self.colorBttn.setText(_translate("StyleColors", "Choose Color"))
        self.closeBttn.setText(_translate("StyleColors", "Close"))
        self.resetBttn.setText(_translate("StyleColors", "Reset Colors"))

