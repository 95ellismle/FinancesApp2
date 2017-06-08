import sys
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QApplication, QTabWidget, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import pandas as pd

from __main__ import dict_bank_data, new_cols


class Table(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.TabWidget = QTabWidget(self)
        self.Vbox = QVBoxLayout()
        
        count = 1
        for i in dict_bank_data:
            self.page1 = QWidget()
            self.Table1 = QTableWidget()
            self.Vbox.addWidget(self.Table1)
            self.page1.setLayout(self.Vbox)
            
            self.TabWidget.addTab(self.page1,"Account %i"%count)
            count += 1
            self.createTable(self.Table1, dict_bank_data[i])
        # Show widget
        self.show()
 
    def insert_values(self, table, dataframe):
        for x in range(len(dataframe)):
            countY = 0
            for y in dataframe.columns:
                table.setItem(x,countY, QTableWidgetItem(str(dataframe.loc[x,y])))
                countY += 1
            table.setHorizontalHeaderLabels(new_cols)
        
    def createTable(self, table, data):
       # Create table
        table.setRowCount(len(data))
        table.setColumnCount(len(data.columns))
        self.insert_values(table, data)
            