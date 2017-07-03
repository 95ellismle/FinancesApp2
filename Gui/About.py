#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 14:12:43 2017

@author: ellismle
"""

from PyQt5.QtWidgets import QTextEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QFont

from Gui import StyleSheets as St
from Gui.Funcs import AllInOneLayout


class AboutPage(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        f = open('./Gui/html/About_Page.html','r')
        help_page_html = f.read()
        f.close()
        self.Help_Box = QTextEdit()
        self.Help_Box.setHtml(help_page_html)
        self.Help_Box.setReadOnly(True)
        CFont = QFont(*St.Header_Font)
        self.Help_Box.setFont(CFont)
        self.Help_Box.setStyleSheet(St.StyleSheets['Text Frame'])
        self.Help_Box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
        AllInOneLayout(self,self.Help_Box)
        self.show()
    

