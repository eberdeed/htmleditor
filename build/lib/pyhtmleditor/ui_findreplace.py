# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uifiles/findreplace.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FindReplace(object):
    def setupUi(self, FindReplace):
        FindReplace.setObjectName("FindReplace")
        FindReplace.resize(447, 323)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../usr/share/htmleditor/resources/Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FindReplace.setWindowIcon(icon)
        self.guititle = QtWidgets.QLabel(FindReplace)
        self.guititle.setGeometry(QtCore.QRect(70, 0, 301, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.guititle.setFont(font)
        self.guititle.setAlignment(QtCore.Qt.AlignCenter)
        self.guititle.setObjectName("guititle")
        self.findEdit = LineEditor(FindReplace)
        self.findEdit.setGeometry(QtCore.QRect(90, 80, 261, 29))
        self.findEdit.setObjectName("findEdit")
        self.replaceEdit = LineEditor(FindReplace)
        self.replaceEdit.setGeometry(QtCore.QRect(90, 140, 261, 29))
        self.replaceEdit.setObjectName("replaceEdit")
        self.label = QtWidgets.QLabel(FindReplace)
        self.label.setGeometry(QtCore.QRect(110, 50, 231, 23))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FindReplace)
        self.label_2.setGeometry(QtCore.QRect(100, 110, 231, 23))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.nextBttn = QtWidgets.QPushButton(FindReplace)
        self.nextBttn.setGeometry(QtCore.QRect(230, 200, 180, 33))
        self.nextBttn.setAutoExclusive(True)
        self.nextBttn.setObjectName("nextBttn")
        self.previousBttn = QtWidgets.QPushButton(FindReplace)
        self.previousBttn.setGeometry(QtCore.QRect(30, 200, 180, 33))
        self.previousBttn.setAutoExclusive(True)
        self.previousBttn.setObjectName("previousBttn")
        self.previousReplaceBttn = QtWidgets.QPushButton(FindReplace)
        self.previousReplaceBttn.setGeometry(QtCore.QRect(30, 240, 180, 33))
        self.previousReplaceBttn.setAutoExclusive(True)
        self.previousReplaceBttn.setObjectName("previousReplaceBttn")
        self.nextReplaceBttn = QtWidgets.QPushButton(FindReplace)
        self.nextReplaceBttn.setGeometry(QtCore.QRect(230, 240, 180, 33))
        self.nextReplaceBttn.setAutoExclusive(True)
        self.nextReplaceBttn.setObjectName("nextReplaceBttn")
        self.closeBttn = QtWidgets.QPushButton(FindReplace)
        self.closeBttn.setGeometry(QtCore.QRect(30, 280, 180, 33))
        self.closeBttn.setObjectName("closeBttn")
        self.replaceAllBttn = QtWidgets.QPushButton(FindReplace)
        self.replaceAllBttn.setGeometry(QtCore.QRect(230, 280, 180, 33))
        self.replaceAllBttn.setAutoExclusive(True)
        self.replaceAllBttn.setObjectName("replaceAllBttn")

        self.retranslateUi(FindReplace)
        QtCore.QMetaObject.connectSlotsByName(FindReplace)

    def retranslateUi(self, FindReplace):
        _translate = QtCore.QCoreApplication.translate
        FindReplace.setWindowTitle(_translate("FindReplace", "Find and Replace"))
        self.guititle.setText(_translate("FindReplace", "Find and Replace"))
        self.label.setText(_translate("FindReplace", "Find Text"))
        self.label_2.setText(_translate("FindReplace", "Replace Text"))
        self.nextBttn.setText(_translate("FindReplace", "Find Next"))
        self.previousBttn.setText(_translate("FindReplace", "Find Previous"))
        self.previousReplaceBttn.setText(_translate("FindReplace", "Replace Prev"))
        self.nextReplaceBttn.setText(_translate("FindReplace", "Replace Next"))
        self.closeBttn.setText(_translate("FindReplace", "Close"))
        self.replaceAllBttn.setText(_translate("FindReplace", "Replace All"))

from pyhtmleditor.lineeditor import LineEditor
