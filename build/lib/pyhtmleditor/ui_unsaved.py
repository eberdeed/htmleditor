# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uifiles/unsaved.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Unsaved(object):
    def setupUi(self, Unsaved):
        Unsaved.setObjectName("Unsaved")
        Unsaved.resize(800, 400)
        self.fileList = QtWidgets.QListWidget(Unsaved)
        self.fileList.setGeometry(QtCore.QRect(50, 25, 750, 280))
        self.fileList.setObjectName("fileList")
        self.saveBttn = QtWidgets.QPushButton(Unsaved)
        self.saveBttn.setGeometry(QtCore.QRect(100, 330, 150, 50))
        self.saveBttn.setObjectName("saveBttn")
        self.cancelBttn = QtWidgets.QPushButton(Unsaved)
        self.cancelBttn.setGeometry(QtCore.QRect(560, 330, 150, 50))
        self.cancelBttn.setObjectName("cancelBttn")

        self.retranslateUi(Unsaved)
        QtCore.QMetaObject.connectSlotsByName(Unsaved)

    def retranslateUi(self, Unsaved):
        _translate = QtCore.QCoreApplication.translate
        Unsaved.setWindowTitle(_translate("Unsaved", "Unsaved Files"))
        self.saveBttn.setText(_translate("Unsaved", "Save"))
        self.cancelBttn.setText(_translate("Unsaved", "Cancel"))

