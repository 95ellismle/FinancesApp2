# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QAbstractScrollArea, QLineEdit, QTableView, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QHeaderView
from PyQt5.QtGui import QFont, QColor

# Other Imports
from numpy import shape

# Importing some required variables from the main code
from __main__ import dict_bank_data, act_nums
from Data import Data as dr
from Gui import Funcs
import Gui.StyleSheets as St

# This is some code taken from https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame
# I found the tableWidget was flagging in terms of performance for even smallish datasets (1,000+).
# This QAbstractTableModel seems to perform much better when populating a tableView with a pandas dataframe.

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data.values            # Returns a set of numpy arrays where each array contains a row from the dataframe in order.
        self._cols = data.columns           # Gets the dataframe columns
        self.r, self.c = shape(self._data)  # Finds the dimensions of the dataframe
     
    # rowCount, columnCount and data are all necessary functions to call when using the QAbstractTableModel.
    def rowCount(self, parent=None): 
        return self.r
    
    def columnCount(self, parent=None):
        return self.c

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return self._data[index.row(),index.column()]
        return None

    # Well behaved models also implement headerData (taken from http://pyqt.sourceforge.net/Docs/PyQt4/qabstracttablemodel.html)
    def headerData(self, p_int, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._cols[p_int])
            elif orientation == Qt.Vertical:
                return p_int
        return None
    
    
# The TablePage Widget, this will be shown in the main window when pressed.    
class TablePage(QWidget): # Create a class inheriting from the QMainWindow
    def __init__(self, parent=None):
        super(TablePage, self).__init__(parent)
        self.setGeometry(500, 500, 1600, 880) # Set the Geometry of the Window   
        
        ### Setting the Colour of the app background
        p = self.palette()
        b_col = QColor(*St.table_background_colour)
        p.setColor(self.backgroundRole(), b_col)
        self.setPalette(p)   
        ###
        self.initUI() # Call the initUI function to initialise things
        
    def initUI(self):      
        ### Dealing with the Tabs         
        self.myTabs = QTabWidget(self) # Creates the tab widget to hold the tabs
        self.myTabs.setMinimumHeight(100)
        self.myTabs.setStyleSheet(St.StyleSheets['Tab'])
        for name in act_nums:
            self.tabWidget =  QWidget() # Creating a widget to hold a single tab
            self.view = QTableView(self) # Creating a table view to eventually put a pandas dataframe in
            self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.tabWidget.setStyleSheet(St.StyleSheets['Tab'])
            self.view.setStyleSheet(St.StyleSheets['Table'])
            ### Change the header fonts
            Hfont = QFont(*St.Header_Font)
            self.headers = self.view.horizontalHeader()
            self.headers.setDefaultAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            self.headers.setFont(Hfont)
            
            Ifont = QFont(*St.Item_Font)
            self.view.setFont(Ifont)
            ###
            Funcs.AllInOneLayout(self.tabWidget,[self.view]) # add the self.view object to the self.tabWidget object's layout
            
            Tfont = QFont(*St.Tab_Font)
            self.myTabs.setFont(Tfont)
            self.view.setAlternatingRowColors(True);
            self.myTabs.addTab(self.tabWidget, str(name)) # Add this tab to myTabs
            self.createTable(dict_bank_data[name]) # Call the create table function to create a table
        ###
        
        ### Sorting out the Layout
        Funcs.AllInOneLayout(self,[self.myTabs],VH='H') # Add the sidebar_frame and myTabs to the layout of the page horizontally.
        ###
        
        self.show() # show the entire app
        
    # This function creates the table using a TableView
    def createTable(self, data):
        self.Display_Data = data # Making a new dataframe to hold the data for display
        self.Display_Data['Date'] = self.Display_Data['Date'].apply(dr.date2str) # Making the datetime more readable
        self.model = PandasModel(self.Display_Data) # Create a model and fill it with data
        self.view.setModel(self.model)
        self.view.setShowGrid(St.Show_Table_Grid_Lines)
        for i in range(1,len(dict_bank_data[act_nums[0]].columns)):
                self.headers.setSectionResizeMode(int(i),QHeaderView.Stretch)  
        self.view.resizeColumnsToContents() # Resize the column widths to fit the contents
        
        self.view.show()
    
    