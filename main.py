from __future__ import unicode_literals

### Standard Python Modules ####
import os              # A module for operating system operations

### Modules included in the repo ###
from Data import Data as dr

error_messgs = [] # A list to store anything that goes wrong...


### Telling the code where everything is
bank_statement_folder_path = '/home/ellismle/Documents/Other/Finances-App(non git)/Stats/'
categories_filename = '/home/ellismle/Documents/Other/Finances_app2/Categories.txt'
###

### Finding the Bank Statement Files and Paypal files
poss_bank_files = os.listdir(bank_statement_folder_path)
poss_bank_files = [bank_statement_folder_path + i for i in poss_bank_files if '.csv' in i]      # removing any non csv files
paypal_filepaths = [i for i in poss_bank_files if 'payp' in i]     # finding the paypal files
bank_filepaths = [i for i in poss_bank_files if 'payp' not in i]   # finding the non-paypal and therefore bank files
###

dr.data_clean(poss_bank_files)                 # Permanently removes sensitive data from statements
bank_data = dr.data_read(bank_filepaths)       # Reads the statement files and collates them into 1 dataframe
paypal_data = dr.data_read(paypal_filepaths)   # Reads the paypal files and collates into 1 dataframe.

names = {'Acc Num':['account number'], 
         'Balance':['balance'], 
         'In':['in','credit'], 
         'Out':['out','debit'], 
         'Date':['date'],
         'Description':['descr','name'],
         'Type':['type','code'],
         'Time':['tim']}

### Changing the names of the statement columns
cols = bank_data.columns
new_cols = dr.dict_value_search(list(cols),names)
bank_data.columns = new_cols
###

### Converting the type from string to something more useful
dr.convert_col(bank_data,'Date','date',error_messgs)
dr.convert_col(bank_data,'Balance',float,error_messgs)
dr.convert_col(bank_data,'In',float,error_messgs)
dr.convert_col(bank_data,'Out',float,error_messgs)
dr.convert_col(bank_data,'Acc Num',int,error_messgs)
###

### Sorting data from different bank accounts
bank_data = bank_data.sort('Date',0)
bank_data['Description'] = bank_data['Description'].apply(dr.up)
act_nums = set(list(bank_data['Acc Num'])) # Finding the unique account numbers
dict_bank_data = {i:bank_data.loc[bank_data['Acc Num'] == i] for i in act_nums}
###

### Reading the file containing info on categorising the data
categories_file = open(categories_filename,'r')
categories_txt = categories_file.read()
categories_file.close()

# Parsing file data
x = [i.replace('\n','').replace(' ','').replace('\_',' ') for i in categories_txt.split(';')]
cats = {i.split(':\t')[0]:i.split(':\t')[1].split(',') for i in x} #
###




# embedding_in_qt5.py --- Simple Qt5 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#               2015 Jens H Nielsen
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        self.axes = fig.add_subplot(111)
        self.axes.get_xaxis().tick_bottom()
        self.axes.get_yaxis().tick_left()
        self.axes.spines["top"].set_visible(False)
        self.axes.spines["right"].set_visible(False)
        self.axes.spines["bottom"].set_visible(False)
        self.axes.spines["left"].set_visible(False)
        
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        bal = dict_bank_data[27274868].groupby('Date')['Balance'].last()
        dat = dict_bank_data[27274868].groupby('Date')['Date'].first()
        self.axes.plot(dat,bal)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Finances App 2")

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """embedding_in_qt5.py example
Copyright 2005 Florent Rougon, 2006 Darren Dale, 2015 Jens H Nielsen

This program is a simple example of a Qt5 application embedding matplotlib
canvases.

It may be used and modified with no restriction; raw copies as well as
modified versions may be distributed without limitation.

This is modified from the embedding in qt4 example to show the difference
between qt4 and qt5"""
                                )


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()