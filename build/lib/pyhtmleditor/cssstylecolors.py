"""
    CSSStyleColors:  CSS Lexer Style Color Changer GUI.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    January 2016, San Diego California United States of America
"""
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from pyhtmleditor.ui_stylecolors import Ui_StyleColors


class CSSStyleColors(QDialog, Ui_StyleColors):
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
        super(CSSStyleColors, self).__init__(parent)
        self.setupUi(self)
        self.progObj = parent.progObj
        self.label.setText("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n" \
            + "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\np, li { white-space: pre-wrap; }\n" \
            + "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:14pt; font-weight:400; font-style:normal;\">\n" \
            + "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;" \
            + " text-indent:0px;\"><span style=\" font-family:\'DejaVu Sans\'; font-weight:600;\">CSS Editor</span></p>\n" \
            + "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;" \
            + " text-indent:0px;\"><span style=\" font-family:\'DejaVu Sans\'; font-weight:600;\">Style Changer</span></p></body></html>")
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
        tmplist = self.progObj.cssstyles[self.stylenum]
        self.colorobj = tmplist[1]
           
    def selectColor(self):
        """ Select a color for the selected part of style.
        """
        self.colorobj = QColorDialog.getColor(self.colorobj, self, "Color for " + self.tagtext)
        tmplist = self.progObj.cssstyles[self.stylenum]
        tmplist[1] = self.colorobj
        self.progObj.cssstyles[self.stylenum] = tmplist
        self.redrawList()
            
    def resetColors(self):
        """ Return the colors to the default values.
        """
        self.progObj.cssstyles.clear()
        CSSLexer = QsciLexerCSS()
        count = 0
        while(len(CSSLexer.description(count)) > 0):
            item = list()
            item.append(CSSLexer.description(count))
            item.append(CSSLexer.color(count))
            self.progObj.cssstyles[count] = item
            count += 1
        self.redrawList()
            

    def closeEvent(self, event):
        """ Close the gui and display all the changes in the style list.
        """
        keys = self.progObj.cssstyles.keys()
        entries = list(keys)
        entries.sort()
        for x in entries:
            tmplist = self.progObj.cssstyles[x]
            self.progObj.CSSLexer.setColor(tmplist[1], x)
         
    def redrawList(self):
        """ Redraw the parts of style list using the existing data.
        """
        self.styleList.clear()
        keys = self.progObj.cssstyles.keys()
        entries = list(keys)
        entries.sort()
        for x in entries:
            tmplist = self.progObj.cssstyles[x]
            item = QListWidgetItem(tmplist[0])
            brush = QBrush(tmplist[1])
            item.setForeground(brush)
            self.styleList.addItem(item)
