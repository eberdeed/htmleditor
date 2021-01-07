# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uifiles/abouthtmledit.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AboutHTMLEdit(object):
    def setupUi(self, AboutHTMLEdit):
        AboutHTMLEdit.setObjectName("AboutHTMLEdit")
        AboutHTMLEdit.resize(555, 238)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../usr/share/htmleditor/resources/htmledit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AboutHTMLEdit.setWindowIcon(icon)
        self.logoLbl = QtWidgets.QLabel(AboutHTMLEdit)
        self.logoLbl.setGeometry(QtCore.QRect(40, 20, 91, 121))
        self.logoLbl.setText("")
        self.logoLbl.setPixmap(QtGui.QPixmap("../../../../usr/share/htmleditor/resources/htmledit.png"))
        self.logoLbl.setObjectName("logoLbl")
        self.logoTextEdit = QtWidgets.QPlainTextEdit(AboutHTMLEdit)
        self.logoTextEdit.setGeometry(QtCore.QRect(150, 20, 361, 141))
        self.logoTextEdit.setStyleSheet("background:#0000FF;color:#FFFFFF;")
        self.logoTextEdit.setDocumentTitle("")
        self.logoTextEdit.setReadOnly(True)
        self.logoTextEdit.setObjectName("logoTextEdit")
        self.okayBttn = QtWidgets.QPushButton(AboutHTMLEdit)
        self.okayBttn.setGeometry(QtCore.QRect(180, 170, 171, 51))
        self.okayBttn.setObjectName("okayBttn")

        self.retranslateUi(AboutHTMLEdit)
        self.okayBttn.clicked.connect(AboutHTMLEdit.accept)
        QtCore.QMetaObject.connectSlotsByName(AboutHTMLEdit)

    def retranslateUi(self, AboutHTMLEdit):
        _translate = QtCore.QCoreApplication.translate
        AboutHTMLEdit.setWindowTitle(_translate("AboutHTMLEdit", "About the HTML Editor"))
        self.logoTextEdit.setPlainText(_translate("AboutHTMLEdit", "The HTML Editor\n"
"by Edward Charles Eberle\n"
"<eberdeed@eberdeed.net>\n"
"San Diego, CA USA\n"
"website: www.eberdeed.net"))
        self.okayBttn.setText(_translate("AboutHTMLEdit", "Okay"))

