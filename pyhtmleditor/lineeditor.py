"""
    LineEditor:  A subclass for QLineEdit to catch the "Return" keypress
    and the loss of focus event.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    August 15, 2016, San Diego California United States of America
"""
import os, sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class LineEditor(QLineEdit):
    """ A subclass for QLineEdit to catch the "Return" keypress
        and the loss of focus event.
    """
    
    returnval = Qt.Key_Return
    firereturn = None
    firefocus = None
    
    def __init__(self, parent=None):
        """ Initialize the class.
        """
        super(LineEditor, self).__init__(parent)
        self.firereturn = QAction("Fire Return", self)
        self.firefocus = QAction("Out of Focus", self)
        return

    def keyPressEvent(self, event):
        """ Catch the <RETURN> key.
        """
        key = event.key()
        if key == self.returnval:
            self.firereturn.trigger()
            return
        QLineEdit.keyPressEvent(self, event)
          
    def focusOutEvent(self, event):
        """ Catch the Focus Out event.
        """
        self.firefocus.trigger()
        QLineEdit.focusOutEvent(self, event)