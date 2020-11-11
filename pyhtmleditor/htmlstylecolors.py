"""
    HTMLStyleColors:  HTML Lexer Style Color Changer GUI.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    May 2016, San Diego California United States of America
"""
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from pyhtmleditor.ui_stylecolors import Ui_StyleColors


class HTMLStyleColors(QDialog, Ui_StyleColors):
    """ A configuration GUI for the parts of style list.
    """
    # Class global parent object.
    progObj = None
    window = 0
    selection = None
    tagtext = ''
    colorobj = None
    stylenum = 0
    
    def __init__(self, parent=None):
        super(HTMLStyleColors, self).__init__(parent)
        self.setupUi(self)
        self.progObj = parent.progObj
        
        # Fill the parts of style list widget.
        self.redrawList()
            
        # Connect the buttons.
        self.colorBttn.clicked.connect(self.selectColor) 
        self.styleList.itemClicked.connect(self.styleSelect)   
        self.resetBttn.clicked.connect(self.resetColors)
        self.closeBttn.clicked.connect(self.close)
        
    def styleSelect(self):
        """ Select an item from the parts of style list.
        """
        tagval = None
        self.tagtext = ''
        tagval = self.styleList.selectedItems()
        self.stylenum = self.styleList.currentRow()
        self.selection = tagval[0]
        self.tagtext = tagval[0].text()
        self.styleList.removeItemWidget(self.selection)
        tmplist = self.progObj.htmlstyles[self.stylenum]
        self.colorobj = tmplist[1]
           
    def selectColor(self):
        """ Select a color for the selected part of style.
        """
        self.colorobj = QColorDialog.getColor(self.colorobj, self, "Color for " + self.tagtext)
        tmplist = self.progObj.htmlstyles[self.stylenum]
        tmplist[1] = self.colorobj
        self.progObj.htmlstyles[self.stylenum] = tmplist
        self.redrawList()
            
    def resetColors(self):
        """ Return the colors to the default values.
        """
        self.progObj.htmlstyles.clear()
        HTMLLexer = QsciLexerHTML()
        count = 0
        while(len(HTMLLexer.description(count)) > 0):
            item = list()
            item.append(HTMLLexer.description(count))
            item.append(HTMLLexer.color(count))
            self.progObj.htmlstyles[count] = item
            count += 1
        self.redrawList()
            

    def closeEvent(self, event):
        """ Close the gui and display all the changes in the style list.
        """
        keys = self.progObj.htmlstyles.keys()
        entries = list(keys)
        entries.sort()
        for x in entries:
            tmplist = self.progObj.htmlstyles[x]
            self.progObj.HTMLLexer.setColor(tmplist[1], x)
         
    def redrawList(self):
        """ Redraw the parts of style list using the existing data.
        """
        self.styleList.clear()
        keys = self.progObj.htmlstyles.keys()
        entries = list(keys)
        entries.sort()
        for x in entries:
            tmplist = self.progObj.htmlstyles[x]
            item = QListWidgetItem(tmplist[0])
            brush = QBrush(tmplist[1])
            item.setForeground(brush)
            self.styleList.addItem(item)
