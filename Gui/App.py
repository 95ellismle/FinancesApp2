import sys
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QMainWindow, QApplication, QTabWidget, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import pandas as pd

from __main__ import dict_bank_data, new_cols, act_nums


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
        
        self.myTabs = QTabWidget(self)
        for intName in act_nums:
            name = str(intName)
            tabWidget = QWidget()
            tabTable = QTableWidget()
            self.createTable(tabTable, dict_bank_data[intName])
        
            tabLayout = QVBoxLayout()
            tabLayout.addWidget(tabTable)
            tabWidget.setLayout(tabLayout)
            
            self.myTabs.addTab(tabWidget, name)
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.myTabs)
        self.setLayout(mainLayout)
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
            