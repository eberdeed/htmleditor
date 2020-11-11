#!/usr/bin/python3
"""
    DocGen:  Documentation Generator for the HTML Editor.
    Edward Charles Eberle <eberdeed@eberdeed.net>
    September 8, 2016, San Diego California USA
"""
import os, sys
from glob import glob

class DocGen:
    
    htmlclasses = glob('../pyhtmleditor/*')
    dirlen = len("../pyhtmleditor/")
    command = list()
    index = "index.html"
    header = \
        """
        <html>
        <head>
            <meta charset="UTF-8">
            <title>HTML Editor Documentation</title>
        <style>
            BODY   {      font-family: Serif;
                    background: white;
                    color: black;
                    line-height: 100%;
                }
           
            H1      {     font-size: 16.0pt;
                    font-family: Serif;
                    line-height: 100%;
                }
        </style>
        </head>
        <body>
        <br><br>
        <center><H1>HTML Editor Documentation</H1></center>
        <br><br>
        """    
    footer = '\n</body>\n</html>\n'
    
    def __init__(self):
        command = "rm *.html"
        os.system(command)
        self.createtopcommand()
        self.createhtml()
        self.createclasscommand()
        self.createhtml()
        self.createindex()
        print("\n\n\tDocumentation Successfully Generated\n\n")
        return

    def createtopcommand(self):
        self.command = list()
        self.command.append("pydoc3 -w ../htmleditor.py dummy")
                
    def createclasscommand(self):
        self.command = list()
        for x in self.htmlclasses:
            if (not ("pycache" in x) and not ("ui_" in x)):
                self.command.append("pydoc3 -w " + x)

                
    def createhtml(self):
        for x in self.command:
            os.system(x)
    
        
    def createindex(self):
        htmllines = ""
        htmllines += "<center><A href=\"htmleditor.html\">htmleditor.html</A></center><BR>\n"
        htmllines += "<BR><center><H1>HTML Editor Classes</H1></center><BR>"
        for x in self.htmlclasses:
            if (not ("pycache" in x) and not ("ui_" in x)):
                x = x[self.dirlen:]
                x = x.replace(".py", ".html")
                htmllines += "<center><A href=\"" + x + "\">" + x + "</A></center><BR>\n"
        htmllines = self.header + htmllines + self.footer
        htmlfile = open(self.index, "w", newline="\n", encoding="utf-8")
        htmlfile.write(htmllines)
        htmlfile.close()
        
def main():
    docs = DocGen()
    return(0)

main()
