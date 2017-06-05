#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 09:11:39 2017

@author: ellismle
"""

from PyQt5.QtWidgets import QTableWidget,QTableWidgetItem,QVBoxLayout

 
class Table(QTableWidget):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, parent, data):
        QTableWidget.__init__(self, parent)
        self._data = data
        # set row count
        self.setRowCount(4)
         
        # set column count
        self.setColumnCount(2)