#!/usr/bin/python3
"""
    AboutHTMLEdit:  HTML Editor program logo.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    February 2016, San Diego California United States of America
"""
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyhtmleditor.ui_abouthtmledit import Ui_AboutHTMLEdit

class AboutHTMLEdit(QDialog, Ui_AboutHTMLEdit):
    """ HTML Editor program logo. With my info in it.
    """
    # Class global parent object.
    def __init__(self, parent=None, text=""):
        super(AboutHTMLEdit, self).__init__(parent)
        self.setupUi(self)
        
