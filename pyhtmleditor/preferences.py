#!/usr/bin/python3
"""
    Preferences:  HTML Editor preferences GUI.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    February 2016, San Diego California United States of America
"""
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyhtmleditor.ui_preferences import Ui_Preferences
from pyhtmleditor.htmlstylecolors import HTMLStyleColors
from pyhtmleditor.cssstylecolors import CSSStyleColors

class Preferences(QDialog, Ui_Preferences):
    """ HTML Editor preferences GUI.
    """
    progObj = None
    # Class global parent object.
    def __init__(self, parent=None, text=""):
        super(Preferences, self).__init__(parent)
        self.progObj = parent
        self.setupUi(self)
        self.fontBttn.clicked.connect(self.setFont)
        self.webBttn.clicked.connect(self.setBrowser)
        self.quitBttn.clicked.connect(self.close)
        self.htmlBttn.clicked.connect(self.htmlStyles)
        self.cssBttn.clicked.connect(self.cssStyles)
        
    def setFont(self):
        okay = True
        currfont = self.progObj.app.font()
        fontsel, complete = QFontDialog.getFont(self.progObj)
        if (complete):
            self.progObj.app.setFont(fontsel)
            self.progObj.HTMLLexer.setFont(fontsel)
            self.progObj.CSSLexer.setFont(fontsel)
            QMessageBox.information(self.progObj, "Font Selected", \
                "You have selected " + fontsel.family() + " as your program font.", \
                QMessageBox.Ok, QMessageBox.NoButton)
        else:
            QMessageBox.warning(self.progObj, "Action Cancelled", \
                "The action was cancelled by the user.", \
                QMessageBox.Ok, QMessageBox.NoButton)
            
    def setBrowser(self):
        bname, complete = QFileDialog.getOpenFileName(self.progObj, "Select Web Browser", "/usr/bin", "All Files(*)")
        if (complete):
            self.progObj.webbrowser = bname
            path, name = os.path.split(bname)
            QMessageBox.information(self.progObj, "Web Browser Selected", \
                "You have selected " + name + " as your web browser.", \
                QMessageBox.Ok, QMessageBox.NoButton)
        else:
            QMessageBox.warning(self.progObj, "Action Cancelled", \
                "The action was cancelled by the user.", \
                QMessageBox.Ok, QMessageBox.NoButton)
            
    def htmlStyles(self):
        print("********************")
        print("********************")
        print("********************")
        for x in self.progObj.htmlstyles:
            print(x , self.progObj.htmlstyles[x])
        styleobj = HTMLStyleColors(self)
        styleobj.show()
        
    def cssStyles(self):
        styleobj = CSSStyleColors(self)
        styleobj.show()        