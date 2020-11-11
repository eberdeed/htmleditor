"""
    Unsaved:  Give the user the option of saving unsaved files.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    September 2020, San Diego California United States of America
"""
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyhtmleditor.ui_unsaved import Ui_Unsaved

class Unsaved(QDialog, Ui_Unsaved):
    """ A Clickable list widget to select and de-select
        files for saving.
    """
    # Class global parent object.
    progObj = None
    
    def __init__(self, parent=None):
        """ Connect the signals and slots.
        """
        super(Unsaved, self).__init__(parent)
        self.setupUi(self)
        self.progObj = parent
        # Connect the buttons.
        self.saveBttn.released.connect(self.saveFiles)
        self.cancelBttn.released.connect(self.closeProg)
        self.fileList.itemPressed.connect(self.changeStatus)
        self.getList()
        return
        
    def getList(self):
        """ Obtain the list of unsaved files.
        """
        for x in range(self.progObj.tabWidget.count()):
            if (self.progObj.changed[x]):
                tmptxt = self.progObj.tabWidget.tabToolTip(x)
                tmptxt = tmptxt.replace("&", "")
                self.fileList.addItem(tmptxt + " -- Save")
        
    def changeStatus(self, item):
        """ Change the saved/unsaved status of a file.
        """
        print("In change status.")
        row = self.fileList.currentRow()
        item = self.fileList.takeItem(row)
        tmptxt = item.text()
        print(tmptxt, tmptxt.find("Don\'t"))
        if (tmptxt.find("Don\'t") > 0):
            tmptxt = tmptxt.replace("Don\'t Save", "Save")
        else:
            tmptxt = tmptxt.replace("Save", "Don\'t Save")
        item.setText(tmptxt)
        self.fileList.insertItem(row, tmptxt)
            
    def saveFiles(self):
        """ Save all the selected files.
        """
        for x in range(self.fileList.count()):
            item = self.fileList.item(x)
            tmptxt = item.text()
            if (tmptxt.find("Don\'t") > 0):
                continue
            else:
                item = self.fileList.item(x)
                tmptxt = item.text()
                tmptxt = tmptxt.replace(" -- Save", "")
                try:
                    textfile = open(tmptxt, 'w', newline='\n', encoding='utf-8')
                    for x in range(self.progObj.tabWidget.count()):
                        if (tmptxt == self.progObj.tabWidget.tabToolTip(x)):
                            index = x
                            break
                    editor = self.progObj.tabWidget.widget(index)
                    doc = editor.text()
                    print("File name: ", tmptxt, " Index: ", index, " HTML File: \n", doc)
                    textfile.write(doc)
                    textfile.close()
                    print("Saved file: ", tmptxt)
                    found = False
                    for x in self.progObj.filelist:
                        if (tmptxt == x):
                            found = True
                            break
                    if not found:
                        self.progObj.filelist.insert(0, tmptxt)
                        print("Inserted file: ", tmptxt, " into the file list.")
                    if (len(self.progObj.filelist) > 20):
                        self.progObj.filelist = self.progObj.filelist[:20]
                    self.progObj.displayDocs()
                    for x in self.progObj.filelist:
                        print(x)
                except Exception as e:
                    QMessageBox.critical(self, "File Error", "Could not write the file:  " + tmptxt + "\nError:  " +  str(e), QMessageBox.Ok, QMessageBox.NoButton)
        self.accept()
                    
    def closeProg(self):
        """ Close the GUI.
        """
        self.accept()
                
