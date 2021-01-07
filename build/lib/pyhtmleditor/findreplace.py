"""
    FindReplace:  Find and Replace text dialog.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    January 2016, San Diego California United States of America
"""
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyhtmleditor.ui_findreplace import Ui_FindReplace

class FindReplace(QDialog, Ui_FindReplace):
    """ A text-based find and replace dialog
        to search for, replace and delete text.
    """
    # Class global parent object.
    progObj = None

    def __init__(self, parent=None):
        super(FindReplace, self).__init__(parent)
        self.setupUi(self)
        self.progObj = parent
        # Connect the buttons.
        self.nextBttn.released.connect(self.findText)
        self.previousBttn.released.connect(self.findPrevText)
        self.nextReplaceBttn.released.connect(self.findReplaceNext)
        self.previousReplaceBttn.released.connect(self.findReplacePrev)
        self.replaceAllBttn.released.connect(self.replaceAll)
        self.closeBttn.released.connect(self.closeForm)
        self.findEdit.firereturn.triggered.connect(self.findText)
        self.replaceEdit.firereturn.triggered.connect(self.findReplaceNext)
        # If there is marked text, use it as the find string.
        if (self.progObj.findstr):
            self.findEdit.setText(self.progObj.findstr)
            self.replaceEdit.setFocus()
        else:
            self.findEdit.setFocus()
        self.getIndex()
        return
        
    def getIndex(self):
        if self.progObj.window == 1:
            self.progObj.mainindex = self.progObj.htmlEdit.SendScintilla(self.progObj.baseEdit.SCI_GETCURRENTPOS)
        else:
            self.progObj.mainindex = self.progObj.cssEdit.SendScintilla(self.progObj.baseEdit.SCI_GETCURRENTPOS)
        
    def markDoc(self):
        self.progObj.markDoc(True)
        return
    
    def closeForm(self):
        self.progObj.htmlonly = False
        if self.progObj.window == 1:
            self.progObj.htmlEdit.SendScintilla(self.progObj.baseEdit.SCI_SETCURRENTPOS, self.progObj.mainindex)
            self.progObj.htmlEdit.SendScintilla(self.progObj.baseEdit.SCI_CLEARSELECTIONS)
        else:
            self.progObj.cssEdit.SendScintilla(self.progObj.baseEdit.SCI_SETCURRENTPOS, self.progObj.mainindex)
            self.progObj.cssEdit.SendScintilla(self.progObj.baseEdit.SCI_CLEARSELECTIONS)
        self.close()
        return
    
    def findText(self):
        self.getIndex()
        self.progObj.findstr = self.findEdit.text()
        if (len(self.progObj.findstr)):
            if (self.progObj.window == 1):
                self.progObj.findNextHTML()
            elif (self.progObj.window == 2):
                self.progObj.findNextCSS()
        else:
            QMessageBox.warning(self, "No Find String", "You must have a value to find.")
        return
        
    def findPrevText(self):
        index = 0
        line = 0
        self.progObj.findstr = self.findEdit.text()
        if (len(self.progObj.findstr)):
            if (self.progObj.window == 1):
                self.progObj.findPrevHTML()
            else:
                self.progObj.findPrevCSS()
        else:
            QMessageBox.warning("No Find String", "You must have a value to find.")
        return
        
    def findReplaceNext(self):
        self.getIndex()
        tmptext = ""
        self.progObj.findprev = False
        # print("In findreplace GUI.")
        self.progObj.findstr = self.findEdit.text()
        self.progObj.replacestr = self.replaceEdit.text()
        if (len(self.progObj.findstr)):
            if self.progObj.window == 1:
                self.progObj.replaceHTML()
            elif self.progObj.window == 2:
                self.progObj.replaceCSS()
        else:
            QMessageBox.warning("No Find String", "You must have a value to find.")
        return
        
    def findReplacePrev(self):
        tmptext = ""
        self.progObj.findprev = True
        self.progObj.findstr = self.findEdit.text()
        self.progObj.replacestr = self.replaceEdit.text()
        if (len(self.progObj.findstr)):
            if self.progObj.window == 1:
                self.progObj.replaceHTML()
            elif self.progObj.window == 2:
                self.progObj.replaceCSS()
        else:
            QMessageBox.warning("No Find String", "You must have a value to find.")
        return
        
    def replaceAll(self):
        self.progObj.findstr = self.findEdit.text()
        self.progObj.replacestr = self.replaceEdit.text()
        if (len(self.progObj.findstr)):
            if self.progObj.window == 1:
                self.progObj.replaceAllHTML()
            elif self.progObj.window == 2:
                self.progObj.replaceAllCSS()
        else:
            QMessageBox.warning("No Find String", "You must have a value to find.")
        return
    
