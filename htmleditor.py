#!/usr/bin/python3
"""
    HTML Editor:  Hyper-Text Markup Language and Cascading Style Sheet Editor.
    Created By Edward Charles Eberle <eberdeed@eberdeed.net>
    January 2016, San Diego, CA, United States of America
"""
import os, sys, io, math, shlex, subprocess
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qsci import *
from pyhtmleditor.ui_htmleditor import Ui_HTMLEditor
from pyhtmleditor.htmldata import HTMLData
from pyhtmleditor.cssproperties import CSSProperties
from pyhtmleditor.findreplace import FindReplace
from pyhtmleditor.abouthtmledit import AboutHTMLEdit
from pyhtmleditor.preferences import Preferences
from pyhtmleditor.unsaved import Unsaved

class HTMLEditor(QMainWindow, Ui_HTMLEditor):
    """ A HTML and CSS editor to allow
        for the creation of well-formed HTML documents.
        This program uses QScintilla for the colorization
        of the CSS and HTML documents.
    """
    # Class global variables.
    app = None
    baseEdit = QsciScintillaBase
    # The HTML editor.
    htmlEdit = None
    # The CSS editor.
    cssEdit = None
    # Window configuration variables.
    height1 = 0
    width1 = 0
    tmpx = 0
    tmpy = 0
    lowtmpy = 0
    lowtmpx = 0
    lowtmpheight = 0
    lowtmpwidth = 0
    hightmpheight = 0
    # The current open/save directory.
    currdir = ''
    # The program configuration directory.
    progdir = ''
    # The name of the general configuration directory.
    confdir = ".config"
    # The data for the HTML tag list.
    htmldata = None
    # The data for the CSS tag list.
    cssdata = None
    # The separator for the various list.
    sep = " "
    # The start of the data tag.
    opening = ''
    # The closing of the data tag.
    closing = ''
    # The property text.
    proptext = ''
    # The type of window.
    # 1 = HTML, 2 = CSS
    window = 1
    # The user's home directory.
    usrdir = ''
    # The file object.
    textfile = ''
    # The name of the HTML file.
    htmlfile = ''
    # The name of the CSS file.
    cssfile = ''
    # The status display values.
    cssindex = 0
    htmllines = 1
    csslines = 1
    # The location in the document.
    mainindex = 0
    # Status display object and data.
    status = None
    statuslabel = None
    # Flag for data change in the document.
    changed = [False, False]
    # Flag for search direction.
    findprev = False
    # Flag for more unprocessed data.
    moredata = True
    # Flag for operation abort.
    aborted = False
    srcvisible = None
    # Flags to ensure cursor visibility due to
    # two different editors being used.
    htmlvisible = None
    cssvisible = None
    # The file name extension value.
    docext = '.html'
    # The documents themselves.
    textdoc = ''
    htmldoc = ''
    cssdoc = ''
    # The beginning and end of the selections.
    htmlbegin = 0
    htmlend = 0
    cssbegin = 0
    cssend = 0
    # Tag value.
    tag = ''
    # Indentation value.
    indent = 12
    # The QsciScintilla Lexers that highlight 
    # the documents.
    HTMLLexer = None
    CSSLexer = None
    # The name of the selected font.
    progfont = None
    # The Find/Replace GUI object.
    findgui = None
    # The regular expression flag.
    regex = False
    # Tags that need a URL.
    needurl = list(["<img>", "<source>", "<link>", "<a>", \
        "<object>"])
    # The find string for text in a document.
    findstr = ''
    # The replace string for text in a document.
    replacestr = ''
    # The color values for HTML highlighting.
    htmlstyles = dict()
    # The color values for CSS highlighting.
    cssstyles = dict()
    # Document size.
    htmlsize = 0
    csssize = 0
    # Add a save message flag.
    savemessage = True
    # Document file list.
    filelist = list()
    # Current open document tabs menu.
    currentTabs = None
    # Current tabs menu icon.
    tabIcon = None
    # Recent documents menu.
    recentDocs = None
    # Recent documents menu icon.
    docIcon = None
    # Name of the default web browser.
    webbrowser = "firefox-esr"
    # The recommended website for HTML information.
    w3cschool = "www.w3schools.com"
    # The file name for the program configuration data.
    proggeom = 'htmledit.geom'
    # The location of the HTML help data.
    helpfile = '/usr/share/htmleditor/resources/editorhelp.html'
    # The replace all flag.
    replaceall = False
    # The initial HTML document.
    htmltemplate = """<!DOCTYPE html>
<html>
<head>
<title>HTML Document</title>
<link href='stylesheet.css' rel='stylesheet' type='text/css'>
</head>
<body>
</body>
</html>"""
    # The initial CSS document.
    csstemplate = """BODY   {      
            font-family: Sans-Serif;
            font-size: 14.0pt;
            background: #FFFFFF;
            color: #000000;
            margin-bottom: 1in;
            margin-right: 1in;
            margin-left: 1in;
            margin-top: 1in;
            line-height: 150%;
        }
A:active {
            color: #BC433E;
        }
A:link {
            color: #E6C13B;
        }

A:visited {
            color: #A19465;
        }
OBJECT {
            width:900px;
            height:450px;
        }
P       {
            text-align:left;
        }
H1      {
            text-align:center;
            line-height: 40%;
        }
        
H2      {
            text-align:center;
            line-height: 40%;
        }
H3      {
            text-align:center;
            line-height: 40%;
        }
IMG     {
            vertical-align: top;
        }
.left { 
            position: absolute;
            left: 300px;
        }
.center {
            text-align:center;
        }
.red    {
            color: #FF0000;
        }
.right  {
            position:absolute;
            right: 300px;
        }
"""

    def __init__(self, app, parent=None):
        """ An initialization method to gather program 
            configuration data and connect signals and slots.
            app = QApplication
            parent = containing QWidget
        """
        geomlist = list()
        self.app = app
        self.progfont = app.font()
        super(HTMLEditor, self).__init__(parent)
        self.setupUi(self)
        # Hide a floating unused gui element.
        self.cssList.setVisible(False)
        # Assign a QLabel.
        self.statuslabel = QLabel()
        self.tabWidget.clear()
        # Create and enable the lexers (for colored text).
        self.htmlEdit = QsciScintilla()
        self.HTMLLexer = QsciLexerHTML()
        self.htmlEdit.setLexer(self.HTMLLexer)
        self.cssEdit = QsciScintilla()
        self.CSSLexer = QsciLexerCSS()
        self.cssEdit.setLexer(self.CSSLexer)
        count = 0
        while(len(self.HTMLLexer.description(count)) > 0):
            item = list()
            item.append(self.HTMLLexer.description(count))
            item.append(self.HTMLLexer.color(count))
            self.htmlstyles[count] = item
            count += 1
        self.htmlsize = len(self.htmlstyles)
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETMULTIPLESELECTION, True)
 
        count = 0
        while(len(self.CSSLexer.description(count)) > 0):
            item = list()
            item.append(self.CSSLexer.description(count))
            item.append(self.CSSLexer.color(count))
            self.cssstyles[count] = item
            count += 1
        self.csssize = len(self.cssstyles)
        self.HTMLLexer.setFont(self.progfont)
        self.CSSLexer.setFont(self.progfont)
        # Define the CSS highlighting.
        self.htmlEdit.setFont(self.progfont)
        self.cssEdit.setFont(self.progfont)
        
        # Ensure that only one item at a time is selected from
        # the lists. The tagList is a list of HTML tags.
        # The cssList is a list of CSS properties.
        self.tagList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.cssList.setSelectionMode(QAbstractItemView.SingleSelection)

        # HTML tag data.
        self.htmldata = HTMLData()

        # Cascading style sheet properties
        self.cssdata = CSSProperties()

        # The home directory location in storage.
        self.usrdir = os.environ['HOME']

        # If the user's configuration directory does not exist, then 
        # create it.  This allows the user to delete the configuration
        # data and then restart the program with the default values.
        self.confdir = os.path.join(self.usrdir, self.confdir)
        if not os.path.exists(self.confdir):
            try:
                os.mkdir(self.confdir)
            except Exception as e:
                QMessageBox.critical(self, "Fatal Error", "Could not create the directory " \
                    + self.confdir + "\n" +  str(e), QMessageBox.Ok, QMessageBox.Ok)
                sys.exit(1)
        else:
            self.progdir = os.path.join(self.confdir, "htmleditor")
            # if the programs configure directory does not exist, create it.
            if not os.path.exists(self.progdir):
                try:
                    os.mkdir(self.progdir)
                except Exception as e:
                    QMessageBox.critical(self, "Fatal Error", "Could not create the directory " \
                        + self.progdir + "\n" +  str(e), QMessageBox.Ok, QMessageBox.Ok)
                    sys.exit(1)
            else:
                # The directory exists, so load the window geometry.
                fname = os.path.join(self.progdir, self.proggeom)
                if os.path.exists(fname):
                    # Open the configuration file for reading.
                    try:
                        textfile = open(fname, newline='\n', encoding='utf-8')
                        geomlist = textfile.readlines()
                        textfile.close()
                    except Exception as e:
                        QMessageBox.warning(self, "Program Error", "Could not read the configuration file:  " \
                            + fname + " Error:  " +  str(e), QMessageBox.Ok, QMessageBox.Ok)
                    # A series of try/excepts to convert the
                    # data from string to float values.
                    try:
                        tmpstr = geomlist[0].rstrip('\n')
                        self.width1 = float(tmpstr)
                    except Exception as e:
                        print("Error converting geometry:  " + str(e))
                    try:
                        tmpstr = geomlist[1].rstrip('\n')
                        self.height1 = float(tmpstr)
                    except Exception as e:
                        print("Error converting geometry:  " + str(e))
                    try:
                        tmpstr = geomlist[2].rstrip('\n')
                        self.tmpx = float(tmpstr)
                    except Exception as e:
                        print("Error converting geometry:  " + str(e))
                    try:
                        tmpstr = geomlist[3].rstrip('\n')
                        self.tmpy = float(tmpstr)
                    except Exception as e:
                        print("Error converting geometry:  " + str(e))
                    try:
                        tmpstr = geomlist[4].rstrip('\n')
                        self.window = int(tmpstr)
                    except Exception as e:
                        print("Error converting window configuration:  " + str(e))
                    try:
                        self.webbrowser = geomlist[5].rstrip('\n')
                    except Exception as e:
                        print("Error converting web browser name:  " + str(e))
                    # Convert the HTML highlighting values
                    # from string to integer.
                    try:
                        count = 0
                        self.htmlstyles.clear()
                        for x in range(0, 4 * self.htmlsize, 4):
                            tmplist = list()
                            tmplist.append(geomlist[7 + x].rstrip('\n'))
                            red = int(geomlist[8 + x].rstrip('\n'))
                            green = int(geomlist[9 + x].rstrip('\n'))
                            blue = int(geomlist[10 + x].rstrip('\n'))
                            tmpcolor = QColor(red, green, blue)
                            tmplist.append(tmpcolor)
                            self.htmlstyles[count] = tmplist
                            count += 1
                    except Exception as e:
                        print("Error converting HTML styles at ", count, " error: ", str(e))
                    # Convert the CSS highlighting values
                    # from string to integer.
                    try:
                        count = 0
                        self.cssstyles.clear()
                        adjust = 4 * self.htmlsize
                        for x in range(0, 4 * self.csssize, 4):
                            tmplist = list()
                            tmplist.append(geomlist[7 + adjust + x].rstrip('\n'))
                            red = int(geomlist[8 + adjust + x].rstrip('\n'))
                            green = int(geomlist[9 + adjust + x].rstrip('\n'))
                            blue = int(geomlist[10 + adjust + x].rstrip('\n'))
                            tmpcolor = QColor(red, green, blue)
                            tmplist.append(tmpcolor)
                            self.cssstyles[count] = tmplist
                            count += 1
                    except Exception as e:
                        print("Error converting CSS styles at ", count, " error: ", str(e))
                    adjust += (4 * self.csssize) + 7
                    self.filelist = geomlist[adjust:]
                    for x in range(len(self.filelist)):
                        if (self.filelist[x] == '\n'):
                            self.filelist.pop(x)
                            x -= 1
                        else:
                            self.filelist[x] = self.filelist[x].rstrip('\n')
                    # Get the program font.
                    try:
                        self.progfont = QFont()
                        tmpstr = geomlist[6].rstrip('\n')
                        self.progfont.fromString(tmpstr)
                        self.app.setFont(self.progfont)
                        self.htmlEdit.setFont(self.progfont)
                        self.cssEdit.setFont(self.progfont)
                        self.HTMLLexer.setFont(self.progfont)
                        self.CSSLexer.setFont(self.progfont)
                        keys = self.htmlstyles.keys()
                        entries = list(keys)
                        entries.sort()
                        for x in entries:
                            tmplist = self.htmlstyles[x]
                            self.HTMLLexer.setColor(tmplist[1], x)
                        keys = self.cssstyles.keys()
                        entries = list(keys)
                        entries.sort()
                        for x in entries:
                            tmplist = self.cssstyles[x]
                            self.CSSLexer.setColor(tmplist[1], x)
                    except Exception as e:
                        print("Error converting data:  " + str(e))
                    # Set the necessary components visible and resize the window.
                    self.setGeometry(self.tmpx, self.tmpy , self.width1, self.height1)
        # Load the HTML tag list.
        for x in range(len(self.htmldata.opentags)):
            if x > 1:
                itemtxt = self.htmldata.opentags[x] + ">" + self.sep + self.htmldata.closetags[x]
            else:
                itemtxt = self.htmldata.opentags[x] + self.sep + self.htmldata.closetags[x]
            item = QListWidgetItem(itemtxt)
            self.tagList.addItem(item)

        # Load the style sheet properties list.
        keys = self.cssdata.cssprops.keys()
        items = list(keys)
        items.sort()
        for x in items:
            item = QListWidgetItem(x)
            self.cssList.addItem(item)

        # Let the program know which editor you are working in.
        # Uses the "window" variable to indicate which window the cursor is in.
        self.htmlEdit.SCN_FOCUSIN.connect(self.chooseHTML)
        self.cssEdit.SCN_FOCUSIN.connect(self.chooseCSS)
        # Connect the list items and so they can return their values.
        self.tagList.itemClicked.connect(self.getTag)
        self.cssList.itemClicked.connect(self.getCSS)
        
        # Various file menu actions.
        self.actionOpen.triggered.connect(self.openFile)
        self.actionNew.triggered.connect(self.newHTML)
        self.actionNew_CSS.triggered.connect(self.newCSS)
        self.recentDocs = QMenu("Recent Docs", self.menuFile)
        self.docIcon = QIcon("/usr/share/htmleditor/resources/fileopen.png")
        self.displayDocs()
        self.currentTabs = QMenu("Current Tabs", self.menuTabs)
        self.tabIcon = QIcon("/usr/share/htmleditor/resources/textedit.png")
        self.actionCloseCurrent.triggered.connect(self.removeTab)
        self.actionCloseAll.triggered.connect(self.removeAllTabs)
        self.actionSave.triggered.connect(self.saveFile)
        self.actionSave_As.triggered.connect(self.saveAsFile)
        self.actionSave_All.triggered.connect(self.saveAll)
        self.actionExit.triggered.connect(self.close)
        self.actionClose.triggered.connect(self.removeTab)
        self.actionClose_All.triggered.connect(self.removeAllTabs)

        # Change the view of the program to the web browser.
        self.actionWeb_Browser.triggered.connect(self.openWebBrowser)
        
        # Set up the help menu.
        self.actionW3C_org_School.triggered.connect(self.goToSchool)
        self.actionHelp.triggered.connect(self.displayHelp)
        self.actionAbout_HTML_Editor.triggered.connect(self.displayLogo)
        self.actionPreferences.triggered.connect(self.setPrefs)
        self.actionSave_Preferences.triggered.connect(self.saveSettings)
        self.actionLoad_Preferences.triggered.connect(self.loadSettings)
        
        # Keep the cursor visible.
        self.htmlvisible = QAction("HTML Cursor Visible", self)
        self.cssvisible = QAction("CSS Cursor Visible", self)
        self.htmlvisible.triggered.connect(self.htmlEdit.ensureCursorVisible)
        self.cssvisible.triggered.connect(self.cssEdit.ensureCursorVisible)
        
        # Define the actions.
        self.htmlcut = QAction("HTML Cut", self)
        self.csscut = QAction("CSS Cut", self)
        self.htmlcopy = QAction("HTML Copy", self)
        self.csscopy = QAction("CSS Copy", self)
        self.htmlpaste = QAction("HTML Paste", self)
        self.csspaste = QAction("CSS Paste", self)
        self.htmlredo = QAction("HTML Redo", self)
        self.cssredo = QAction("CSS Redo", self)
        self.htmlundo = QAction("HTML Undo", self)
        self.cssundo = QAction("CSS Undo", self)
        self.htmlcut.triggered.connect(self.htmlEdit.cut)
        self.csscut.triggered.connect(self.cssEdit.cut)
        self.htmlcopy.triggered.connect(self.htmlEdit.copy)
        self.csscopy.triggered.connect(self.cssEdit.copy)
        self.htmlpaste.triggered.connect(self.htmlEdit.paste)
        self.csspaste.triggered.connect(self.cssEdit.paste)
        self.htmlredo.triggered.connect(self.htmlEdit.redo)
        self.cssredo.triggered.connect(self.cssEdit.redo)
        self.htmlundo.triggered.connect(self.htmlEdit.undo)
        self.cssundo.triggered.connect(self.cssEdit.undo)
       

        # Keep track of the undos and redos.
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        
        # Keep track of the cuts.
        self.actionCut.triggered.connect(self.cut)

        # Keep track of the copies.
        self.actionCopy.triggered.connect(self.copy)

        # Keep track of the pastes.
        self.actionPaste.triggered.connect(self.paste)

        # Keep track of the select alls.
        self.actionSelect_All.triggered.connect(self.selectAll)
        
        # Find and replace dialog connection.
        self.actionFind_and_Replace.triggered.connect(self.findReplace)
        
        # Connect the tab widget to properly display the 
        # current tab.
        self.tabWidget.currentChanged.connect(self.setCurrentIndex)
        # Set the default data for the HTML and CSS editors.
        self.cssdoc = self.csstemplate
        self.cssEdit.setText(self.cssdoc)
        self.htmldoc = self.htmltemplate
        self.htmlEdit.setText(self.htmldoc)
        self.tabWidget.addTab(self.htmlEdit, "newfile.html")
        self.tabWidget.addTab(self.cssEdit, "newfile.css")
        self.htmlEdit = self.tabWidget.widget(0)
        self.cssEdit = self.tabWidget.widget(1)
        # The "current directory" initially set to the home directory.
        self.currdir = self.usrdir
        self.htmlfile = os.path.join(self.currdir, "newfile.html")
        self.tabWidget.setTabToolTip(0, self.htmlfile)
        self.cssfile = os.path.join(self.currdir, "newfile.css")
        self.tabWidget.setTabToolTip(1, self.cssfile)
        # Set the cursor in typing position in the HTML document.
        index = self.htmldoc.find("<body>")
        if (index > 0):
            index += 6
            self.htmlEdit.setFocus()
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, index)
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, index)
        

        # Set the status bar.
        self.status = self.statusBar()
        self.statuslabel = QLabel()
        self.statuslabel.setGeometry(10, self.height1 - 40, 550, 30)
        self.status.addPermanentWidget(self.statuslabel, 1)
        self.htmlEdit.textChanged.connect(self.htmlChanged)
        self.cssEdit.textChanged.connect(self.cssChanged)
        self.htmlEdit.cursorPositionChanged.connect(self.updateStatus)
        self.cssEdit.cursorPositionChanged.connect(self.updateStatus)
        self.window = 1
        self.updateStatus()
        # Set the inital configuration.
        self.displayTabs()

    
    def resizeEvent(self, event):
        """ Handles the resizing of the GUI in its five
            configurations.
            event = QEvent
        """
        dim = event.size()
        self.height1 = dim.height()
        self.width1 = dim.width()
        self.tmpx = 10
        self.tmpy = 10
        self.tmpwidth = self.width1 - 20
        hscalar = self.height1 / 600
        self.tmpheight = 380 * hscalar
        self.lowtmpx = self.width1 / 2
        self.lowtmpy = self.tmpy + self.tmpheight + 4
        self.lowtmpwidth = (self.tmpwidth / 2)- 4
        self.lowtmpheight = self.height1 - (self.tmpheight + 80)
        self.hightmpheight = self.height1 - 20
        self.tabWidget.setGeometry(self.tmpx, self.tmpy, self.tmpwidth, self.tmpheight)
        # HTML editor configuration.
        if(self.window == 1):
            self.cssEdit.setVisible(False)
            self.htmlEdit.setVisible(True)
            self.htmlEdit.setGeometry(self.tmpx, self.tmpy, self.tmpwidth, self.tmpheight)
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETSCROLLWIDTH, self.tmpwidth - 50)
            self.tagList.setGeometry(self.tmpx, self.lowtmpy, self.tmpwidth, self.lowtmpheight)
            self.cssList.setVisible(False)
            self.tagList.setVisible(True)
            return
        
        # CSS editor configuration.
        elif(self.window == 2):
            self.cssEdit.setVisible(True)
            self.htmlEdit.setVisible(False)
            self.cssEdit.setGeometry(self.tmpx, self.tmpy, self.tmpwidth, self.tmpheight)
            self.cssEdit.SendScintilla(self.baseEdit.SCI_SETSCROLLWIDTH, self.tmpwidth - 50)
            self.tagList.setGeometry(self.tmpx, self.lowtmpy, self.lowtmpwidth, self.lowtmpheight)
            self.cssList.setGeometry(self.lowtmpx, self.lowtmpy, self.lowtmpwidth, self.lowtmpheight)
            self.cssList.setVisible(True)
            self.tagList.setVisible(True)
            return
        
    
    def chooseHTML(self):
        """ Let the program know we are editing HTML.
        """
        self.window = 1
 
    def chooseCSS(self):
        """ Let the program know we are editing the stylesheet.
        """
        self.window = 2
        
    def htmlChanged(self):
        """ Let the program know the HTML document has changed.
        """
        index = self.tabWidget.currentIndex()
        self.changed[index] = True
        self.updateStatus()
        
    def cssChanged(self):
        """ Let the program know the CSS document has changed.
        """
        index = self.tabWidget.currentIndex()
        self.changed[index] = True
        self.updateStatus()
        
    def htmlEditor(self):
        """ Set the HTML editor configuration.
        """
        self.window = 1
        begin = 0
        end = 0
        self.htmlEdit.setFocus()
        self.htmldoc = self.htmlEdit.text()
        if (len(self.htmlfile)):
            self.currdir, filename = os.path.split(self.htmlfile)
        else:
            filename = ""
        self.setWindowTitle("HTML Editor -- " + filename)
        cursize = self.size()
        sizeevent = QResizeEvent(cursize, cursize)
        self.resizeEvent(sizeevent)
        self.htmlvisible.trigger()
        self.htmlEdit.setFocus()
         
    def cssEditor(self):
        """ Set the stylesheet editor configuration.
        """
        self.window = 2
        begin = 0
        end = 0
        self.cssEdit.setFocus()
        if (len(self.cssfile) > 0):
            self.currdir, tmptxt = os.path.split(self.cssfile)
        else:
            tmptxt = ""
        self.setWindowTitle("CSS Editor -- " + tmptxt)
        cursize = self.size()
        sizeevent = QResizeEvent(cursize, cursize)
        self.resizeEvent(sizeevent)
        self.cssvisible.trigger()
        self.cssEdit.setFocus()
         
    def openWebBrowser(self):
        """  Open a seperate program (Firefox-ESR) using the current HTML document.
        """
        tmpwin = self.window
        self.htmldoc = self.htmlEdit.text()
        self.savemessage = False
        self.window = 1
        self.saveFile()
        self.savemessage = True
        self.window = tmpwin
        command = self.webbrowser + " " + self.htmlfile
        commandlist = shlex.split(command)
        try:
            subprocess.Popen(commandlist)
        except Exception as e:
            QMessageBox.warning(self, "Warning -- " + self.webbrowser,\
                "This program requires the web browser " + self.webbrowser \
                + " to be installed." \
                + "  The error is as follows:  " + str(e), \
                QMessageBox.Ok, QMessageBox.Ok)
        
    def goToSchool(self):
        """  Open a seperate program (Firefox-ESR) onto the W3C 
             Schools website.
        """
        command = self.webbrowser + " " + self.w3cschool
        commandlist = shlex.split(command)
        try:
            subprocess.Popen(commandlist)
        except Exception as e:
            QMessageBox.warning(self, "Warning -- " + self.webbrowser,\
                "This program requires the web browser " + self.webbrowser \
                + " to be installed." \
                + "  The error is as follows:  " + str(e), \
                QMessageBox.Ok, QMessageBox.Ok)
    
    def displayDocs(self):
        """ Set the recent documents menu values.
        """
        self.recentDocs.clear()
        self.recentDocs.setIcon(self.docIcon)
        for x in self.filelist:
            tmpact = QAction(self.recentDocs)
            tmpact.setText(x)
            self.recentDocs.addAction(tmpact)
            tmpact.triggered.connect(self.fileClicked)
        self.menuFile.insertMenu(self.actionSave, self.recentDocs)
    
    def fileClicked(self):
        """ Open a document from the recent documents
            file list.
        """
        tmpact = self.sender()
        fname = tmpact.text()
        fname = fname.replace('&', '')
        found = False
        index = 0
        for x in range(self.tabWidget.count()):
            if (fname == self.tabWidget.tabToolTip(x)):
                found = True
                index = x
                break
        if (found):
            self.tabWidget.setCurrentIndex(index)
            return
        try:
            textfile = open(fname, "r", newline="\n", encoding="utf-8")
            doc = textfile.read()
            textfile.close()
        except Exception as e:
            QMessageBox.warning(self, "File IO Error", "The file: "\
                + fname + " did not open.  Error:  " + str(e), QMessageBox.Ok, \
                QMessageBox.Ok)
            return
        stem, self.docext = os.path.splitext(fname)
        # Assign a new editor to the document,
        # based on the type of document opened.
        if(self.docext.lower() == '.css'):
            self.cssfile = fname
            self.cssEdit = QsciScintilla()
            self.cssEdit.setLexer(self.CSSLexer)
            self.cssEdit.setFont(self.progfont)
            self.cssdoc = doc
            self.cssEdit.setText(doc)
            self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
            stem, name = os.path.split(self.cssfile)
            self.tabWidget.addTab(self.cssEdit, name)
            index = self.tabWidget.indexOf(self.cssEdit)
            self.tabWidget.setTabToolTip(index, self.cssfile)
            self.cssEdit.textChanged.connect(self.cssChanged)
            self.cssEdit.cursorPositionChanged.connect(self.updateStatus)
            self.cssEditor()
        # Handle the rest as a web page.
        else:
            self.htmlfile = fname
            self.htmlEdit = QsciScintilla()
            self.htmlEdit.setLexer(self.HTMLLexer)
            self.htmlEdit.setFont(self.progfont)
            self.htmldoc = doc
            self.htmlEdit.setText(doc)
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
            stem, name = os.path.split(self.htmlfile)
            self.tabWidget.addTab(self.htmlEdit, name)
            index = self.tabWidget.indexOf(self.htmlEdit)
            self.htmlEdit.textChanged.connect(self.htmlChanged)
            self.htmlEdit.cursorPositionChanged.connect(self.updateStatus)
            self.tabWidget.setTabToolTip(index, self.htmlfile)
            self.htmlEditor()
        self.changed.append(False)
        for x in range(len(self.changed)):
            print("Changed: Document, Value ", x, self.changed[x])
        print("Current Document: ", index, self.changed[index])        
        self.setCurrentIndex(index)
        self.displayTabs()
        self.setTitle()
        self.mainindex = 0
        self.updateStatus()
        return
    
    def displayHelp(self):
        """  Open a seperate program (Chromium) onto the help file.
        """
        command = self.webbrowser + " " + self.helpfile
        commandlist = shlex.split(command)
        try:
            subprocess.Popen(commandlist)
        except Exception as e:
            QMessageBox.warning(self, "Warning -- " + self.webbrowser,\
                "This program requires the web browser " + self.webbrowser \
                + " to be installed." \
                + "  The error is as follows:  " + str(e), \
                QMessageBox.Ok, QMessageBox.Ok)
        
    def displayLogo(self):
        """ Display the About HTML Editor GUI.
        """
        editorlogo = AboutHTMLEdit(self)
        editorlogo.show()
        
    def setPrefs(self):
        """ Display the Preferences GUI.
        """
        prefObj = Preferences(self)
        prefObj.show()
        
    def updateStatus(self):
        """ Update the document status widget.
            Seen at the bottom of the screen.
        """
        index = 1
        self.htmllines = 1
        self.csslines = 1
        message = ""
        """ Check for an open tab and, if there is one,
            give the status of the document.
        """
        if (self.tabWidget.count() > 0):
            tabindex = self.tabWidget.currentIndex()
            fname = self.tabWidget.tabToolTip(tabindex)
            stem, self.docext = os.path.splitext(fname)
            if(self.docext.lower() == '.css'):
                self.cssEdit = self.tabWidget.widget(tabindex)
                self.cssdoc = self.cssEdit.text()
                csspos = self.cssEdit.SendScintilla(self.baseEdit.SCI_GETCURRENTPOS)
                index = self.cssdoc.find("\n", 0, csspos)
                index += 1
                while (index > 0):
                    self.csslines += 1
                    index = self.cssdoc.find("\n", index, csspos)
                    index += 1
                
                message += "     CSS:  "
                path, filename = os.path.split(self.cssfile)
                message += filename
                if self.changed[tabindex]:
                    message += " * "
                message += " Line "
                message += str(self.csslines)
                message += " Position "
                message += str(csspos)
            else:
                self.htmlEdit = self.tabWidget.widget(tabindex)
                self.htmldoc = self.htmlEdit.text()
                htmlpos = self.htmlEdit.SendScintilla(self.baseEdit.SCI_GETCURRENTPOS)
                csspos = index = self.htmldoc.find("\n", 0, htmlpos)
                index += 1
                while (index > 0):
                    self.htmllines += 1
                    index = self.htmldoc.find("\n", index, htmlpos)
                    index += 1
                message += " HTML:  "
                path, filename = os.path.split(self.htmlfile)
                message += filename
                if self.changed[tabindex]:
                    message += " * "
                message += " Line "
                message += str(self.htmllines)
                message += " Position "
                message += str(htmlpos)        
        self.statuslabel.setText(message)
        
        
        

    def cut(self):
        """ Cut some text from the document.
        """
        if (self.window == 1):
           self.htmlcut.trigger()
        elif (self.window == 2):
           self.csscut.trigger()

    def copy(self):
        """ Copy some text from the document.
        """
        if (self.window == 1):
            self.htmlcopy.trigger()
        elif (self.window == 2):
            self.csscopy.trigger()

    def paste(self):
        """ Paste some text from the document.
        """
        if (self.window == 1):
            self.htmlpaste.trigger()
        elif (self.window == 2):
            self.csspaste.trigger()

    def undo(self):
        """ Undo the last action taken.
        """
        if (self.window == 1):
            self.htmlundo.trigger()
        elif (self.window == 2):
            self.cssundo.trigger()
            
    def redo(self):
        """ Redo the last action taken.
        """
        if (self.window == 1):
            self.htmlredo.trigger()
        elif (self.window == 2):
            self.cssredo.trigger()

    def selectAll(self):
        """ Select all the data in an editor.
        """
        if (self.window == 1):
            self.htmlEdit.selectAll(True)
        elif (self.window == 2):
            self.cssEdit.selectAll(True)
            
    def getTag(self):
        """ Retrieve a tag from the tag list.
        """
        tagtext = ''
        tagval = self.tagList.selectedItems()
        tagtext = tagval[0].text()
        if not (tagtext):
            QMessageBox.warning(self, "Program Error", \
                "No tag to process. ", \
                QMessageBox.Ok, QMessageBox.Ok)
            return
        self.opening, self.closing = tagtext.split()
        # Get a tag from the HTML tag list and insert it 
        # into the document.
        if (self.window == 1):
            if  self.matchedTags():
                self.htmldoc = self.htmlEdit.text()
                self.htmlbegin = self.htmlEdit.SendScintilla(self.baseEdit.SCI_GETSELECTIONSTART)
                self.htmlend = self.htmlEdit.SendScintilla(self.baseEdit.SCI_GETSELECTIONEND)
                self.opening = self.checkURL(self.opening)
                if self.aborted:
                    QMessageBox.warning(self, "Action Cancelled", \
                        "The  action was cancelled.", \
                        QMessageBox.Ok, QMessageBox.Ok)
                    self.aborted = False
                    return
                if (self.closing != "None"):
                    self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.htmlend)
                    self.htmlEdit.insert(self.closing)
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.htmlbegin)
                self.htmlEdit.insert(self.opening)
                self.htmlendabs = self.htmlbegin + len(self.opening)
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.htmlendabs)
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, self.htmlendabs)
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_GETFOCUS)
                self.htmlvisible.trigger()
                self.htmlEdit.setFocus()
                return
            else:
                QMessageBox.warning(self, "Tag Error", \
                    "You have the unmatched tag:  " \
                    + self.unmatchedtag + " in your selection.", \
                    QMessageBox.Ok, QMessageBox.Ok)
                return
        # In the CSS editor add a tag entry.
        elif (self.window == 2):
            self.cssdoc = self.cssEdit.text()
            self.tag = self.opening
            self.tag = self.tag.strip("<>")
            self.tag = self.tag.upper()
            # Finding a CSS tag.
            if (self.cssEdit.hasSelectedText()):
                self.cssindex = self.cssEdit.SendScintilla(self.baseEdit.SCI_GETSELECTIONEND)
                self.cssindex = self.cssdoc.find(self.tag, self.cssindex)
            else:
                self.cssindex = self.cssdoc.find(self.tag + " ")
            if self.cssindex >= 0:
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETSELECTIONSTART, self.cssindex)
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, self.cssindex)
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETSELECTIONEND, self.cssindex + len(self.tag))
                self.cssvisible.trigger()
                self.cssEdit.setFocus()
            else:
                self.addTagVal()
            return
    
    def checkURL(self, tmptag):
        """ Add a filepath to the HTML elements requiring it.
            tmptag = the HTML tag to add the URL to.
        """
        if (tmptag in self.needurl):
            filestr = self.getFileStr()
            if not (filestr):
                self.aborted = True
                self.htmlEdit.setFocus()
                return
        if (tmptag == self.needurl[0]) or (tmptag == self.needurl[1]):
            tmptag = tmptag.rstrip(">")
            tmptag += " src=\""
            tmptag += filestr
            tmptag += "\"/>"
        elif(tmptag == self.needurl[2]) or (tmptag == self.needurl[3]):
            tmptag = tmptag.rstrip(">")
            tmptag += " href=\""
            tmptag += filestr
            if (tmptag == self.needurl[2]):
                tmptag += "\"/>"
            else:
                tmptag += "\">"
        elif (tmptag == self.needurl[4]):
            tmptag = tmptag.rstrip(">")
            tmptag += " data=\""
            tmptag += filestr
            tmptag += "\">"
        return tmptag

    def getFileStr(self):
        """ Obtain a file name for the tags requiring it.
        """
        fname, mask = QFileDialog.getOpenFileName(self, \
            "Get a File String.", self.currdir, \
            "All Files(*.*);;Images(*.jpg *.JPG *.jpeg *.JPEG *.jpe "
            + "*.JPE *.png *.PNG *.gif *.GIF *.tiff *.TIFF *.tga *.TGA"
            + "*.bmp *.BMP *.xpm *.XPM *.xcf *.XCF *.ico *.ICO);;"
            + "Web Pages(*.html *htm *.HTML *.htm *.php *.PHP);;" \
            + "Stylesheets(*.css *.CSS);;" \
            + "Text Files (*.txt *.text *.TXT *.TEXT);;")
        if (fname):
            return fname
        else:
            return None
        
    def addTagVal(self):
        """ Add a tag to a CSS document.
        """
        self.cssindex = len(self.cssdoc)
        if (self.cssdoc[self.cssindex -1] != "\n"):
            self.cssdoc += "\n"
            self.cssindex += 1
        self.length = len(self.tag)
        if (self.length > self.indent - 1):
            tmpint = 2
        else:
            tmpint = self.indent - self.length
        spacestr = " " * tmpint
        entry = self.tag
        entry += spacestr + "{\n"
        spacestr = " " * self.indent
        entry += spacestr
        self.cssindex = len(self.cssdoc) + len(entry)
        entry += "\n"
        entry += spacestr + "}\n"
        self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, len(self.cssdoc))
        self.cssEdit.insert(entry)
        self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.cssindex)
        self.cssEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, self.cssindex)
        self.cssvisible.trigger()
        self.cssEdit.setFocus()

    def markDoc(self, forward):
        """ Marks all the "find" items in a document.
            forward = forward/backward boolean.
        """
        index = 0
        if (self.window == 1):
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
            tmptext = self.htmlEdit.text()
            if (self.findstr in tmptext):
                if (forward):
                    index = tmptext.find(self.findstr, self.mainindex)
                else:
                    index = tmptext.rfind(self.findstr, 0, self.mainindex)
                self.mainindex = index
                if (self.mainindex < len(tmptext)):
                    self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETSELECTION, self.mainindex, self.mainindex + len(self.findstr))
                    lineno = self.htmlEdit.SendScintilla(self.baseEdit.SCI_GETCURLINE)
                    self.htmlEdit.SendScintilla(self.baseEdit.SCI_SCROLLCARET, lineno)
            return
        elif (self.window == 2):
            self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
            tmptext = self.cssEdit.text()
            if (self.findstr in tmptext):
                if (forward):
                    index = tmptext.find(self.findstr, self.mainindex)
                else:
                    index = tmptext.rfind(self.findstr, 0, self.mainindex)
                self.mainindex = index
                if (self.mainindex < len(tmptext)):
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SETSELECTION, self.mainindex, self.mainindex + len(self.findstr))
                    lineno = self.cssEdit.SendScintilla(self.baseEdit.SCI_GETCURLINE)
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SCROLLCARET, lineno)
            return

            
    def findReplace(self):
        """ Instantiates the find-replace GUI and sends along 
            any selected text as find string material.
        """
        self.findstr = None
        self.replacestr = None
        if (self.window == 1):
            self.findstr = self.htmlEdit.selectedText()
        if (self.window == 2):
            self.findstr = self.cssEdit.selectedText()
        self.findgui = FindReplace(self)
        self.findgui.show()        
        
    def replaceHTML(self):
        """ Replace the piece of matched 
            text in the HTML window. 
        """
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
        found = False
        if self.findprev:
            self.findPrevHTML()
        else:
            self.findNextHTML()
        tmptext = self.htmlEdit.text()
        if (self.findstr in tmptext):
            self.htmlEdit.replaceSelectedText(self.replacestr)
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.mainindex)
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETSELECTION, self.mainindex, self.mainindex + len(self.replacestr))
        self.mainindex += len(self.replacestr)
        return
    
    def replaceAllHTML(self):
        """ Replace all instances of the find string
            in the HTML window.
        """
        self.window = 1
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_GOTOPOS, 0)
        self.mainindex = 0
        tmptext = self.htmlEdit.text()
        self.replaceall = True
        while(self.findstr in tmptext):
            self.findNextHTML()
            self.htmlEdit.replaceSelectedText(self.replacestr)
            tmptext = self.htmlEdit.text()
            self.mainindex = self.htmlEdit.SendScintilla(self.baseEdit.SCI_GETCURRENTPOS)
        self.replaceall = False
        
    def replaceAllCSS(self):
        """ Replace all instances of the find string in the
            CSS window.
        """
        self.window = 2
        self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
        self.cssEdit.SendScintilla(self.baseEdit.SCI_GOTOPOS, 0)
        tmptext = self.cssEdit.text()
        self.replaceall = True
        self.mainindex = 0
        while(self.findstr in tmptext):
            self.findNextCSS()
            self.cssEdit.replaceSelectedText(self.replacestr)
            tmptext = self.cssEdit.text()
            self.mainindex = self.cssEdit.SendScintilla(self.baseEdit.SCI_GETCURRENTPOS)
            print(self.mainindex, self.replaceall)
        self.replaceall = False
            
    def findNextHTML(self): 
        """ Find the next piece of text to replace in the HTML window.
        """
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
        tmptext = self.htmlEdit.text()
        index = tmptext.find(self.findstr, self.mainindex)
        if (not self.findstr in tmptext) and (not self.replaceall):
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
            answer = QMessageBox.warning(self, "End of Document", \
                "You have reached the end of the HTML document." \
                + "  Do you wish to continue?", QMessageBox.Yes, \
                QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.mainindex = 0
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
                if (not self.findstr in tmptext):
                    self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
                    QMessageBox.warning(self, "Search Error", \
                        "There are no more instances" \
                        + " in the HTML document.", QMessageBox.Ok, \
                        QMessageBox.Ok)
                else:
                    self.markDoc(True)
        elif (self.findstr in tmptext):
            self.markDoc(True)
        return                

    def findPrevHTML(self): 
        """ Find the previous piece of text to replace in the HTML window.
        """
        tmptext = self.htmlEdit.text()
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
        index = tmptext.rfind(self.findstr, 0, self.mainindex)
        if (not self.findstr in tmptext):
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.htmlEdit.length() - 1)
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
            answer = QMessageBox.warning(self, "End of Document", \
                "You have reached the end of the HTML document." \
                + "  Do you wish to continue?", QMessageBox.Yes, \
                QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.mainindex = self.htmlEdit.length() - 1
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.mainindex)
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
                if (not self.findstr in tmptext):
                    QMessageBox.warning(self, "Search Error", \
                        "There are no more instances" \
                        + " in the HTML document.", QMessageBox.Ok, \
                        QMessageBox.Ok)
                    self.moredata = False
                else:
                    self.markDoc(False)
        else:
            self.markDoc(False)
        return                
    
    def replaceCSS(self):
        """ Replace the piece of matched text in the CSS window.
        """
        found = False
        if self.findprev:
            self.findPrevCSS()
        else:
            self.findNextCSS()
        tmptext = self.cssEdit.text()
        if (self.findstr in tmptext):
            self.cssEdit.replaceSelectedText(self.replacestr)
        self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.mainindex)
        self.cssEdit.SendScintilla(self.baseEdit.SCI_SETSELECTION, self.mainindex, self.mainindex + len(self.replacestr))
        self.mainindex += len(self.replacestr)
        return
        
    def findNextCSS(self):
        """ Find the next piece of text to replace in the CSS window.
        """
        self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
        tmptext = self.cssEdit.text()
        index = tmptext.find(self.findstr, self.mainindex)
        if (not self.findstr in tmptext) and (not self.replaceall):
            self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
            self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
            answer = QMessageBox.warning(self, "End of Document", \
                "You have reached the end of the CSS document." \
                + "  Do you wish to continue?", QMessageBox.Yes, \
                QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.mainindex = 0
                if (not self.findstr in tmptext):
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
                    QMessageBox.warning(self, "Search Error", \
                        "There are no more instances of:  " \
                        + self.findstr + " in the CSS document.", QMessageBox.Ok, \
                        QMessageBox.Ok)
                    self.moredata = False
                else:
                    self.markDoc(True)
        elif (self.findstr in tmptext):
            self.markDoc(True)
        return                
        
    def findPrevCSS(self):
        """ Find the previous piece of text to replace in the CSS window.
        """
        tmptext = self.cssEdit.text()
        self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
        index = tmptext.rfind(self.findstr, 0, self.mainindex)
        if (not self.findstr in tmptext):
            self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.cssEdit.length() - 1)
            self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
            answer = QMessageBox.warning(self, "End of Document", \
                "You have reached the end of the CSS document." \
                + "  Do you wish to continue?", QMessageBox.Yes, \
                QMessageBox.No)
            if answer == QMessageBox.Yes:
                self.mainindex = self.cssEdit.length() - 1
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.mainindex)
                self.cssEdit.SendScintilla(self.baseEdit.SCI_CLEARSELECTIONS)
                if (not self.findstr in tmptext):
                    QMessageBox.warning(self, "Search Error", \
                        "There are no more instances of:  " \
                        + self.findstr + " in the CSS document.", QMessageBox.Ok, \
                        QMessageBox.Ok)
                else:   
                    self.markDoc(False)
        else:
            self.markDoc(False)
        return                

    def getCSS(self):
        """ Retrieve a stylesheet property from the list, adding
            it to the existing document in the given tag.
        """
        tmptext = ""
        self.cssdoc = self.cssEdit.text()
        propindex = self.cssList.selectedItems()
        self.proptext = propindex[0].text()
        if (self.cssEdit.hasSelectedText()):
            if self.cssEdit.hasSelectedText():
                tagstart = self.cssEdit.SendScintilla(self.baseEdit.SCI_GETSELECTIONEND)
                begin = self.cssdoc.find("{", tagstart)
                end = self.cssdoc.find("}", tagstart)
                propbegin = self.cssdoc.find(self.proptext, begin, end)
                if propbegin > 0:
                    propbegin += len(self.proptext)
                    if self.cssdoc[propbegin] != ":":
                        self.cssdoc[propbegin] = ":"
                    propbegin += 1
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, propbegin)
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, propbegin)
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_GETFOCUS)
                    self.cssEdit.setFocus()
                    return
                else:
                    begin += 1
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, begin)
                    end = begin # Move the index inside the brace.
                    self.spacestr = " " * self.indent
                    tmptext = "\n" + self.spacestr + self.proptext + ":"
                    self.adjust = len(tmptext) + begin # Grab the index pointing to the empty property.
                    tmptext += ";"
                    self.cssEdit.insert(tmptext)
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.adjust)
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, self.adjust)
                    self.cssEdit.SendScintilla(self.baseEdit.SCI_GETFOCUS)
                    self.cssvisible.trigger()
                    self.cssEdit.setFocus()
        else:
            begin = self.cssEdit.SendScintilla(self.baseEdit.SCI_GETCURRENTPOS)
            elementbegin = begin
            begin = self.cssdoc.rfind("{", 0, begin)
            end = self.cssdoc.find("}", begin)
            propbegin = self.cssdoc.find(self.proptext, begin, end)
            if propbegin > 0:
                propbegin += len(self.proptext)
                if self.cssdoc[propbegin] != ":":
                    self.cssdoc[propbegin] = ":"
                propbegin += 1
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, propbegin)
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, propbegin)
                self.cssEdit.SendScintilla(self.baseEdit.SCI_GETFOCUS)
                self.cssvisible.trigger()
                self.cssEdit.setFocus()
                return
            else:
                begin = elementbegin
            tmptext += self.proptext + ":"
            self.adjust = len(tmptext)  + begin # Grab the index pointing to the empty property.
            tmptext += ";"
            self.cssEdit.insert(tmptext)
            self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, self.adjust)
            self.cssEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, self.adjust)
            self.cssEdit.SendScintilla(self.baseEdit.SCI_GETFOCUS)
            self.cssvisible.trigger()
            self.cssEdit.setFocus()
            
            
    def openFile(self):
        """ Open a file, putting the file in the appropriate window.
        """
        doc = ''
        fname, mask = QFileDialog.getOpenFileName(self, \
            "Open a text, HTML or CSS File.", self.currdir, \
            "All Files(*.*);;" \
            + "Web Pages(*.html *htm *.HTML *.htm *.php *.PHP);;" \
            + "Stylesheets(*.css *.CSS);;" \
            + "Text Files (*.txt *.text *.TXT *.TEXT)")
        # The file has been chosen.
        if(fname):
            found = False
            index = 0
            for x in range(self.tabWidget.count()):
                if (fname == self.tabWidget.tabToolTip(x)):
                    found = True
                    index = x
                    break
            if (found):
                self.tabWidget.setCurrentIndex(index)
                return True
            try:
                textfile = open(fname, "r", newline="\n", encoding="utf-8")
                doc = textfile.read()
                textfile.close()
            except Exception as e:
                QMessageBox.warning(self, "File IO Error", "The file: "\
                    + fname + " did not open.  Error:  " + str(e), QMessageBox.Ok, \
                    QMessageBox.Ok)
                return
            stem, self.docext = os.path.splitext(fname)
            if(self.docext.lower() == '.css'):
                self.window = 2
                self.cssfile = fname
                self.cssEdit = QsciScintilla()
                self.cssEdit.setLexer(self.CSSLexer)
                self.cssEdit.setFont(self.progfont)
                self.cssdoc = doc
                self.cssEdit.setText(doc)
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
                stem, name = os.path.split(self.cssfile)
                self.tabWidget.addTab(self.cssEdit, name)
                index = self.tabWidget.indexOf(self.cssEdit)
                self.tabWidget.setTabToolTip(index, self.cssfile)
                self.cssEdit.textChanged.connect(self.cssChanged)
                self.cssEdit.cursorPositionChanged.connect(self.updateStatus)
            # Handle the rest as a web page.
            else:
                self.window = 1
                self.htmlfile = fname
                self.htmlEdit = QsciScintilla()
                self.htmlEdit.setLexer(self.HTMLLexer)
                self.htmlEdit.setFont(self.progfont)
                self.htmldoc = doc
                self.htmlEdit.setText(doc)
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
                stem, name = os.path.split(self.htmlfile)
                self.tabWidget.addTab(self.htmlEdit, name)
                index = self.tabWidget.indexOf(self.htmlEdit)
                self.tabWidget.setTabToolTip(index, self.htmlfile)
                self.htmlEdit.textChanged.connect(self.htmlChanged)
                self.htmlEdit.cursorPositionChanged.connect(self.updateStatus)
            self.changed.append(False)
            self.updateStatus()
            self.setCurrentIndex(index)
            self.setTitle()
            self.mainindex = 0
            self.displayTabs()
            found = False
            for x in range(len(self.filelist)):
                if (fname == self.filelist[x]):
                    found = True
                    break
            if (found):
                self.setCurrentIndex(index)
                return
            self.filelist.insert(0, fname)
            if (len(self.filelist) > 20):
                self.filelist = self.filelist[:20]
            self.setCurrentIndex(index)
            self.displayDocs()
        # The file was not selected.
        else:
            QMessageBox.warning(self, "Warning", "Operation canceled.", \
                QMessageBox.Ok, QMessageBox.Ok)
        return True

    def setTitle(self):  
        """ Set the title at the top of the GUI.  Gives the user
            the configuration and the name of the open HTML  or 
            CSS file.
        """
        if (self.window == 1):
            tmptext = self.currdir
            self.currdir, filename = os.path.split(self.htmlfile)
            self.setWindowTitle("HTML Editor -- " + filename)
        elif (self.window == 2):
            self.currdir, tmptext = os.path.split(self.cssfile)
            self.setWindowTitle("CSS Editor -- " +  tmptext)
    
    def saveFile(self):
        """ Save a file in the appropriate window.
        """
        index = self.tabWidget.currentIndex()
        fname = self.tabWidget.tabToolTip(index)
        fname = fname.replace("&", "")
        stem, self.docext = os.path.splitext(fname)
        if (self.docext.lower() == ".css"):
            if (len(fname) < 1):
                fname, typelist = QFileDialog.getSaveFileName(None, 'Save CSS File', \
                self.currdir, 'All Files(*.*);;CSS Files(*.css *.CSS)')
            if not (fname):
                QMessageBox.warning(self, "Action Cancelled", "The action was cancelled.", \
                    QMessageBox.Ok, QMessageBox.Ok)
                return
            self.cssdoc = self.cssEdit.text()
            self.cssfile = fname
            try:
                cssfile = open(fname, 'w', newline='\n', encoding='utf-8')
                cssfile.write(self.cssdoc)
                cssfile.close()
                if(self.savemessage):
                    QMessageBox.information(self, "Success!", "The file:  " + fname \
                        + ' has been written successfully.', \
                        QMessageBox.Ok, QMessageBox.Ok)
            except Exception as e:
                QMessageBox.warning(self, "Warning: File Error", "Could not write file:  " + fname \
                    + " Error: " + str(e), QMessageBox.Ok, QMessageBox.Ok)
        if (self.docext.lower() == ".html"):
            if (len(fname) < 1) and (self.savemessage) :
                fname =  None
                fname, typelist = QFileDialog.getSaveFileName(None, 'Save HTML File', \
                self.currdir, 'All Files(*.*);;Web Pages(*.html *htm *.HTML *.htm *.php *.PHP)')
                if not (fname):
                    QMessageBox.warning(self, "Action Cancelled", "The action was cancelled.", \
                        QMessageBox.Ok, QMessageBox.Ok)
                    return
            self.htmldoc = self.htmlEdit.text()
            self.htmlfile = fname
            try:
                htmlfile = open(fname, 'w', newline='\n', encoding='utf-8')
                htmlfile.write(self.htmldoc)
                htmlfile.close()
                if(self.savemessage):
                    QMessageBox.information(self, "Success!", "The file:  " + fname \
                        + ' has been written successfully.', \
                        QMessageBox.Ok, QMessageBox.Ok)
            except Exception as e:
                QMessageBox.warning(self, "Warning: File Error", "Could not write file:  " + fname \
                    + " Error: " + str(e), QMessageBox.Ok, QMessageBox.Ok)
        self.changed[index] = False
        self.updateStatus()
        return

    def saveAsFile(self):
        """ Save a file with a new name in the appropriate window.
        """
        fname = ""
        index = self.tabWidget.currentIndex()
        fname = self.tabWidget.tabToolTip(index)
        fname = fname.replace("&", "")
        stem, self.docext = os.path.splitext(fname)
        if (self.docext.lower() == ".css"):
            fname, typelist = QFileDialog.getSaveFileName(None, 'Save CSS File as', \
                self.currdir, 'All Files(*.*);;Stylesheets(*.css *.CSS)')
            if (fname):
                self.cssfile = fname
                index = self.tabWidget.currentIndex()
                self.currdir, filename = os.path.split(self.cssfile)
                self.tabWidget.setTabText(index, filename)
                self.tabWidget.setTabToolTip(index, fname)
                self.cssdoc = self.cssEdit.text()
                try:
                    cssfile = open(self.cssfile, 'w', newline='\n', encoding='utf-8')
                    cssfile.write(self.cssdoc)
                    cssfile.close()
                    QMessageBox.information(self, "Success!", "The file:  " + self.cssfile \
                        + ' has been written successfully.', \
                        QMessageBox.Ok, QMessageBox.Ok)
                except Exception as e:
                    QMessageBox.warning(self, "Warning: File Error", "Could not write file:  " + self.cssfile \
                        + " Error: " + str(e), QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Warning", "Operation canceled.", \
                    QMessageBox.Ok, QMessageBox.Ok)
        else:
            fname, typelist = QFileDialog.getSaveFileName(None, 'Save HTML File as', \
                self.currdir, 'All Files(*.*);;Web Pages(*.html *htm *.HTML *.htm *.php *.PHP)')
            if (fname):
                self.htmlfile = fname
                self.currdir, filename = os.path.split(self.htmlfile)
                self.tabWidget.setTabText(index, filename)
                self.tabWidget.setTabToolTip(index, fname)
                self.htmldoc = self.htmlEdit.text()
                try:
                    htmlfile = open(self.htmlfile, 'w', newline='\n', encoding='utf-8')
                    htmlfile.write(self.htmldoc)
                    htmlfile.close()
                    QMessageBox.information(self, "Success!", "The file:  " + self.htmlfile \
                        + ' has been written successfully.', \
                        QMessageBox.Ok, QMessageBox.Ok)
                except Exception as e:
                    QMessageBox.warning(self, "Warning: File Error", "Could not write file:  " + self.htmlfile \
                        + " Error: " + str(e), QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Warning", "Operation canceled.", \
                    QMessageBox.Ok, QMessageBox.Ok)
        self.changed[index] = False
        self.updateStatus()
        self.setTitle()  
        found = False
        for x in self.filelist:
            if (fname == x):
                found = True
                break
        if not found:
            self.filelist.insert(0, fname)
        if (len(self.filelist) > 20):
            self.filelist = self.filelist[:20]
        self.displayDocs()
        
    def saveAll(self):
        """ Save all the files
        """
        for x in range(self.tabWidget.count()):
            doc = self.tabWidget.widget(x).text()
            fname = self.tabWidget.tabToolTip(x)
            self.htmlfile = fname
            if (len(self.htmlfile) == 0):
                self.htmlfile, typelist = QFileDialog.getSaveFileName(None, 'Save File as', 
                    self.currdir, 'All Files(*.*);;Web Pages(*.html *htm *.HTML *.htm *.php *.PHP)')
                if not (self.htmlfile):
                    QMessageBox.warning(self, "Warning", 
                    "Operation canceled.", QMessageBox.Ok, QMessageBox.Ok)
                    return
            try:
                htmlfile = open(self.htmlfile, 'w', newline='\n', encoding='utf-8')
                htmlfile.write(doc)
                htmlfile.close()
            except Exception as e:
                QMessageBox.critical(self, "File Error", "Could not write the html file:  " + self.htmlfile \
                    + "\nError:  " +  str(e), QMessageBox.Ok, QMessageBox.Ok)
                return False
        return True
        
    def setCurrentIndex(self, index):
        """ Set the current editor to the open tab's widget.
            index = the current tab's index.
        """
        if (self.tabWidget.count() > 0):
            self.tabWidget.setCurrentIndex(index)
            fname = self.tabWidget.tabToolTip(index)
            stem, self.docext = os.path.splitext(fname)
            if(self.docext.lower() == '.css'):
                self.window = 2
                self.cssEdit = self.tabWidget.widget(index)
                self.cssfile = fname
                self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
                self.cssEditor()
            # Handle the rest as a web page.
            else:
                self.window = 1
                self.htmlEdit = self.tabWidget.widget(index)
                self.htmlfile = fname
                self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
                self.htmlEditor()
            self.connectEditor()
        self.updateStatus()
        return
    
    def displayTabs(self):
        """ Add all the tabs to the tab list for the tab list menu.
        """
        total = self.tabWidget.count()
        self.currentTabs.clear()
        for x in range(total):
            fname = self.tabWidget.tabText(x)
            fname.replace("&", "")
            tmpact = QAction(self.currentTabs)
            tmpact.setText(fname)
            self.currentTabs.addAction(tmpact)
            tmpact.triggered.connect(self.tabClicked)
        self.menuTabs.insertMenu(self.actionCloseCurrent, self.currentTabs)
    
    def tabClicked(self):
        """ Grab the tab clicked on and add the editor 
            according to the given index.
        """
        actions = self.currentTabs.actions()
        index = actions.index(self.sender())
        self.setCurrentIndex(index)
    
    def connectEditor(self):
        """ Connect the new editor.
        """
        # Connect the new.
        self.htmlcut.triggered.connect(self.htmlEdit.cut)
        self.csscut.triggered.connect(self.cssEdit.cut)
        self.htmlcopy.triggered.connect(self.htmlEdit.copy)
        self.csscopy.triggered.connect(self.cssEdit.copy)
        self.htmlpaste.triggered.connect(self.htmlEdit.paste)
        self.csspaste.triggered.connect(self.cssEdit.paste)
        self.htmlredo.triggered.connect(self.htmlEdit.redo)
        self.cssredo.triggered.connect(self.cssEdit.redo)
        self.htmlundo.triggered.connect(self.htmlEdit.undo)
        self.cssundo.triggered.connect(self.cssEdit.undo)
        
    def removeTab(self):
        """ Remove the current tab.
        """
        index = self.tabWidget.currentIndex()
        if (self.changed[index]):
            tmptxt = self.tabWidget.tabText(index)
            tmptxt = tmptxt[1:]
            retBttn = QMessageBox.critical(self, "Unsaved File", 
            "The file " + tmptxt + " is not saved.  Save now?", QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
            if (retBttn == QMessageBox.Ok):
                tmptxt = self.tabWidget.tabToolTip(index)
                tmptxt.replace("&", "")
                try:
                    textfile = open(tmptxt, 'w', newline='\n', encoding='utf-8')
                    editor = self.tabWidget.widget(index)
                    doc = editor.text()
                    textfile.write(doc)
                    textfile.close()
                except Exception as e:
                    QMessageBox.critical(self, "File Error", 
                    "Could not write the file:  " + tmptxt + 
                    "\nError:  " +  str(e), QMessageBox.Ok, 
                    QMessageBox.Ok)
        self.tabWidget.removeTab(index)
        if (self.tabWidget.count() == 0):
            self.removeAllTabs()
        self.displayTabs()
        return
    
    def removeAllTabs(self):
        """ Remove all the open documents and
            give the default HTML and CSS documents.
        """
        saved = True
        self.htmlEdit = self.tabWidget.widget(0)
        doc = self.htmlEdit.text()
        print(doc)
        for x in self.changed:
            if (x):
                saved = False
        if not (saved):
            unsaved = Unsaved(self)
            unsaved.exec()
        self.tabWidget.clear()
        self.cssEdit = QsciScintilla()
        self.cssEdit.setLexer(self.CSSLexer)
        self.cssEdit.setFont(self.progfont)
        self.cssdoc = self.csstemplate
        self.cssEdit.clear()
        self.cssEdit.setText(self.cssdoc)
        self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
        self.cssEdit.textChanged.connect(self.cssChanged)
        self.cssEdit.cursorPositionChanged.connect(self.updateStatus)
        self.htmlEdit = QsciScintilla()
        self.htmlEdit.setLexer(self.HTMLLexer)
        self.htmlEdit.setFont(self.progfont)
        self.htmldoc = self.htmltemplate
        self.htmlEdit.setText(self.htmldoc)
        # Set the cursor in typing position in the HTML document.
        index = self.htmldoc.find("<body>")
        if (index > 0):
            index += 6
            self.htmlEdit.setFocus()
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, index)
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, index)
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
        self.htmlEdit.textChanged.connect(self.htmlChanged)
        self.htmlEdit.cursorPositionChanged.connect(self.updateStatus)
        self.tabWidget.addTab(self.htmlEdit, "newfile.html")
        self.tabWidget.addTab(self.cssEdit, "newfile.css")
        self.htmlfile = os.path.join(self.currdir, "newfile.html")
        self.tabWidget.setTabToolTip(0, self.htmlfile)
        self.cssfile = os.path.join(self.currdir, "newfile.css")
        self.tabWidget.setTabToolTip(1, self.cssfile)
        self.changed = [False, False]
        self.updateStatus()
        self.displayTabs()
    
    def newHTML(self):
        """ Add a new tab with a new HTML editor.
        """
        self.htmlEdit = QsciScintilla()
        self.htmlEdit.setLexer(self.HTMLLexer)
        self.htmlEdit.setFont(self.progfont)
        self.htmldoc = self.htmltemplate
        self.htmlEdit.setText(self.htmldoc)
        # Set the cursor in typing position in the HTML document.
        index = self.htmldoc.find("<body>")
        if (index > 0):
            index += 6
            self.htmlEdit.setFocus()
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, index)
            self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETANCHOR, index)
        self.htmlEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
        self.tabWidget.addTab(self.htmlEdit, "newfile.html")
        self.htmlfile = os.path.join(self.currdir, "newfile.html")
        index = self.tabWidget.indexOf(self.htmlEdit)
        self.tabWidget.setTabToolTip(index, self.htmlfile)
        self.htmlEdit.textChanged.connect(self.htmlChanged)
        self.htmlEdit.cursorPositionChanged.connect(self.updateStatus)
        self.changed.append(False)
        self.updateStatus()
        self.displayTabs()
        self.setCurrentIndex(index)
 
    def newCSS(self):
        """ Add a new tab with a new CSS editor.
        """
        self.cssEdit = QsciScintilla()
        self.cssEdit.setLexer(self.CSSLexer)
        self.cssEdit.setFont(self.progfont)
        self.cssdoc = self.csstemplate
        self.cssEdit.clear()
        self.cssEdit.setText(self.cssdoc)
        self.cssEdit.SendScintilla(self.baseEdit.SCI_SETCURRENTPOS, 0)
        self.tabWidget.addTab(self.cssEdit, "newfile.css")
        self.cssfile = os.path.join(self.currdir, "newfile.css")
        index = self.tabWidget.indexOf(self.cssEdit)
        self.tabWidget.setTabToolTip(index, self.cssfile)
        self.cssEdit.textChanged.connect(self.cssChanged)
        self.cssEdit.cursorPositionChanged.connect(self.updateStatus)
        self.changed.append(False)
        self.updateStatus()
        self.displayTabs()
        self.setCurrentIndex(index)
            
    def closeEvent(self, event):
        """ Exit the program and save all the configuration data.
            event = QEvent
        """
        saved = True
        for x in self.changed:
            if (x):
                saved = False
        if not (saved):
            unsaved = Unsaved(self)
            unsaved.exec()
        progfont = self.app.font()
        fname = os.path.join(self.progdir, self.proggeom)
        try:
            tmppos = self.pos()
            tmpx = tmppos.x()
            if tmpx < 0:
                tmpx = 0
            tmpy = tmppos.y()
            if tmpy < 0:
                tmpy = 0
            textfile = open(fname, "w", newline="\n", encoding="utf-8")
            textfile.write(str(self.width1) + "\n")
            textfile.write(str(self.height1) + "\n")
            textfile.write(str(tmpx) + "\n")
            textfile.write(str(tmpy) + "\n")
            textfile.write(str(self.window) + "\n")
            textfile.write(self.webbrowser + "\n")
            textfile.write(progfont.toString() + "\n")
            keys = self.htmlstyles.keys()
            entries = list(keys)
            for x in entries:
                tmplist = self.htmlstyles[x]
                textfile.write(tmplist[0] + '\n')
                red = tmplist[1].red()
                green = tmplist[1].green()
                blue = tmplist[1].blue()
                textfile.write(str(red) + '\n')
                textfile.write(str(green) + '\n')
                textfile.write(str(blue) + '\n')
            keys = self.cssstyles.keys()
            entries = list(keys)
            for x in entries:
                tmplist = self.cssstyles[x]
                textfile.write(tmplist[0] + '\n')
                red = tmplist[1].red()
                green = tmplist[1].green()
                blue = tmplist[1].blue()
                textfile.write(str(red) + '\n')
                textfile.write(str(green) + '\n')
                textfile.write(str(blue) + '\n')
            for x in self.filelist:
                textfile.write(x + '\n')
            textfile.close()
        except Exception as e:
            QMessageBox.critical(self, "File Error", "Could not write the configuration file:  " + fname \
                + "\nError:  " +  str(e), QMessageBox.Ok, QMessageBox.Ok)

        event.accept()
        
    def saveSettings(self):
        """ Save a configuration file to a specified file.
        """
        progfont = self.app.font()
        fname, typelist = QFileDialog.getSaveFileName(self, "Choose a configuration file to save.", \
            self.usrdir, "All files(*.*);;Configuration Files(*.cnf *.CNF *.conf *.CONF)")
        try:
            pos = self.pos()
            tmpx = pos.x()
            if tmpx < 0:
                tmpx = 0
            tmpy = pos.y()
            if tmpy < 0:
                tmpy = 0
            textfile = open(fname, "w", newline="\n", encoding="utf-8")
            textfile.write(str(self.width1) + "\n")
            textfile.write(str(self.height1) + "\n")
            textfile.write(str(tmpx) + "\n")
            textfile.write(str(tmpy) + "\n")
            textfile.write(str(self.window) + "\n")
            textfile.write(self.webbrowser + "\n")
            textfile.write(progfont.toString() + "\n")
            keys = self.htmlstyles.keys()
            entries = list(keys)
            for x in entries:
                tmplist = self.htmlstyles[x]
                textfile.write(tmplist[0] + '\n')
                red = tmplist[1].red()
                green = tmplist[1].green()
                blue = tmplist[1].blue()
                textfile.write(str(red) + '\n')
                textfile.write(str(green) + '\n')
                textfile.write(str(blue) + '\n')
            keys = self.cssstyles.keys()
            entries = list(keys)
            for x in entries:
                tmplist = self.cssstyles[x]
                textfile.write(tmplist[0] + '\n')
                red = tmplist[1].red()
                green = tmplist[1].green()
                blue = tmplist[1].blue()
                textfile.write(str(red) + '\n')
                textfile.write(str(green) + '\n')
                textfile.write(str(blue) + '\n')
            textfile.close()
        except Exception as e:
            QMessageBox.critical(self, "File Error", "Could not write the configuration file:  " + fname \
                + "\nError:  " +  str(e), QMessageBox.Ok, QMessageBox.Ok)
            
         
    def loadSettings(self):
        """ Load a configuration file from a specified file.
        """
        geomlist = list()
        fname, typelist = QFileDialog.getOpenFileName(self, "Select a configuration file to open.", \
            self.usrdir, "All files(*.*);;Configuration Files(*.cnf *.CNF *.conf *.CONF)")
        try:
            textfile = open(fname, "r", newline='\n', encoding='utf-8')
            geomlist = textfile.readlines()
            textfile.close()
        except Exception as e:
            QMessageBox.warning(self, "Program Error", "Could not read the configuration file:  " \
                + fname + " Error:  " +  str(e), QMessageBox.Ok, QMessageBox.Ok)
        try:
            tmpstr = geomlist[0].rstrip('\n')
            self.width1 = float(tmpstr)
        except Exception as e:
            print("Error converting geometry:  " + str(e))
        try:
            tmpstr = geomlist[1].rstrip('\n')
            self.height1 = float(tmpstr)
        except Exception as e:
            print("Error converting geometry:  " + str(e))
        try:
            tmpstr = geomlist[2].rstrip('\n')
            self.tmpx = float(tmpstr)
        except Exception as e:
            print("Error converting geometry:  " + str(e))
        try:
            tmpstr = geomlist[3].rstrip('\n')
            self.tmpy = float(tmpstr)
        except Exception as e:
            print("Error converting geometry:  " + str(e))
        try:
            tmpstr = geomlist[4].rstrip('\n')
            self.window = int(tmpstr)
        except Exception as e:
            print("Error converting window configuration:  " + str(e))
        try:
            self.webbrowser = geomlist[5].rstrip('\n')
        except Exception as e:
            print("Error converting web browser name:  " + str(e))
        try:
            count = 0
            self.htmlstyles.clear()
            for x in range(0, 4 * self.htmlsize, 4):
                tmplist = list()
                tmplist.append(geomlist[7 + x].rstrip('\n'))
                red = int(geomlist[8 + x].rstrip('\n'))
                green = int(geomlist[9 + x].rstrip('\n'))
                blue = int(geomlist[10 + x].rstrip('\n'))
                tmpcolor = QColor(red, green, blue)
                tmplist.append(tmpcolor)
                self.htmlstyles[count] = tmplist
                count += 1
        except Exception as e:
            print("Error converting HTML styles at ", count, " error: ", str(e))
        try:
            count = 0
            self.cssstyles.clear()
            adjust = self.htmlsize * 4
            for x in range(0, 4 * self.csssize, 4):
                tmplist = list()
                tmplist.append(geomlist[7 + adjust + x].rstrip('\n'))
                red = int(geomlist[8 + adjust + x].rstrip('\n'))
                green = int(geomlist[9 + adjust + x].rstrip('\n'))
                blue = int(geomlist[10 + adjust + x].rstrip('\n'))
                tmpcolor = QColor(red, green, blue)
                tmplist.append(tmpcolor)
                self.cssstyles[count] = tmplist
                count += 1
        except Exception as e:
            print("Error converting CSS styles at ", count, " error: ", str(e))
        try:
            self.progfont = QFont()
            tmpstr = geomlist[6].rstrip('\n')
            self.progfont.fromString(tmpstr)
            self.app.setFont(self.progfont)
            self.htmlEdit.setFont(self.progfont)
            self.cssEdit.setFont(self.progfont)
            self.HTMLLexer.setFont(self.progfont)
            self.CSSLexer.setFont(self.progfont)
            keys = self.htmlstyles.keys()
            entries = list(keys)
            entries.sort()
            for x in entries:
                tmplist = self.htmlstyles[x]
                self.HTMLLexer.setColor(tmplist[1], x)
            keys = self.cssstyles.keys()
            entries = list(keys)
            entries.sort()
            for x in entries:
                tmplist = self.cssstyles[x]
                self.CSSLexer.setColor(tmplist[1], x)
        except Exception as e:
            print("Error converting program font:  " + str(e))
        # Set the necessary components visible and resize the window.
        self.setGeometry(self.tmpx, self.tmpy , self.width1, self.height1)
        adjust += (4 * self.csssize) + 7
        self.filelist = geomlist[adjust:]
        for x in range(len(self.filelist)):
            if (self.filelist[x] == '\n'):
                self.filelist.pop(x)
                x -= 1
            else:
                self.filelist[x] = self.filelist[x].rstrip('\n')
        
def main():  # Remember the Maine.
    if (len(sys.argv) == 1):
        app = QApplication(sys.argv)
        # Instantiate the above class and display it.
        editor = HTMLEditor(app)
        editor.show()
        app.exec()
    return 0
# Call the main method.
main()
