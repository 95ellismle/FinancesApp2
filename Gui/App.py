import sys

from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QMainWindow, QTableView, QApplication, QWidget, QVBoxLayout, QTabWidget

import numpy as np
import pandas as pd

from __main__ import dict_bank_data, new_cols, act_nums

len_data = 5000
data = pd.DataFrame({i:['bob']*len_data for i in 'abcdefghijklmnopqrstuvwxyz'}, index=range(len_data))

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = np.array(data.values)
        self._cols = data.columns
        self.r, self.c = np.shape(self._data)

    def rowCount(self, parent=None):
        return self.r

    def columnCount(self, parent=None):
        return self.c

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return self._data[index.row(),index.column()]
        return None


    def headerData(self, p_int, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._cols[p_int]
            elif orientation == Qt.Vertical:
                return p_int
        return None
    
    

class Main(QWidget): # Create a class inheriting from the QMainWindow
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setWindowTitle('App')  # Set the title of the app
        self.setGeometry(400, 400, 800, 800) # Set the Geometry of the Window
        self.initUI() # Call the initUI function to initialise things

    def initUI(self):               
        
        self.myTabs = QTabWidget() # Creates the tab widget to hold the tabs
        
        for name in act_nums:
            tabWidget =  QWidget() # Creating a widget to hold a single tab
            self.view = QTableView(self) # Creating a table view to eventually put a pandas dataframe in
            
            tabLayout = QVBoxLayout() #Creating a layout for the tabs
            tabLayout.addWidget(self.view) # Adding the view to the tab
            
            tabWidget.setLayout(tabLayout) # fixing the layout of the tabs with the created one above.
            
            self.myTabs.addTab(tabWidget, str(name))
            
            #self.setCentralWidget(self.view) # Changes the layout of the table view
    
            self.createTable(dict_bank_data[name]) # Call the create table function to create a table
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.myTabs)
        self.setLayout(mainLayout)
        
        self.show() # show the entire app

    def createTable(self, data):
                
        self.head = data.columns
        self.model = PandasModel(data)
        self.view.setModel(self.model)
        self.view.show()