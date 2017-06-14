# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtWidgets import QAbstractScrollArea, QTableView, QWidget, QTabWidget, QHeaderView, QLineEdit, QFrame
from PyQt5.QtGui import QFont, QColor

# Other Imports
from numpy import shape, column_stack, array

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
     
    ### rowCount, columnCount and data are all necessary functions to call when using the QAbstractTableModel.
    def rowCount(self, parent=None): #Controls the amount of rows in the tableview
        return self.r
    
    def columnCount(self, parent=None): #Controls the amount of columns
        return self.c

    def data(self, index, role):
        if index.isValid():
            if role == Qt.EditRole:
                return self._data[index.row(),index.column()]
                
            if role == Qt.ToolTipRole:
                column = index.column()
                row = index.row()
                return "Row: %s, Column: %s" %(str(row),str(self._cols[column]))
                
            if role == Qt.DisplayRole:
                return dr.TablePrep(self._data[index.row(),index.column()])

        return None
    ###

    # This modifies the headerData, Qt.Horizontal will edit the horizontal headers, Vertical ones will be row headers.
    # p_int is the header index
    def headerData(self, p_int, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._cols[p_int])
            elif orientation == Qt.Vertical:
                return "Item "+str(p_int)
        return None

    # Make the data editable
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractTableModel.flags(self, index)| Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable)
      
    # This will modify the data in the table if it is changed in the table
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole: 
            row = index.row()
            col = index.column()
            if type(value) == str:
                self._data[row,col] = value # Set the data to the newly typed value
                return True
            return False
        
    #=====================================================#
    #INSERTING & REMOVING DATA
    #=====================================================#
    def updateData(self, dataIn ,parent = QModelIndex()):
        self.beginInsertRows(parent, 0, len(dataIn))
        self._data = dataIn.values  
        self._cols = dataIn.columns
        self.r, self.c = shape(self._data)
        self.endInsertRows()
        
        return True


    
        
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
        self.myTabs.setTabShape(QTabWidget.TabShape(1000))
        tabbar = self.myTabs.tabBar()
        tabbar.setMovable(True)
        self.views = {}
        self.models = {}
        self.myTabs.setStyleSheet(St.StyleSheets['Tab'])
        for name in act_nums:
            self.tabWidget =  QWidget() # Creating a widget to hold a single tab
            self.views[name] = QTableView(self) # Creating a table view to eventually put a pandas dataframe in
            self.views[name].setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.tabWidget.setStyleSheet(St.StyleSheets['Tab'])
            self.views[name].setStyleSheet(St.StyleSheets['Table'])
            ### Change the header fonts
            Hfont = QFont(*St.Header_Font)
            self.headers = self.views[name].horizontalHeader()
            self.headers.setDefaultAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            self.headers.setFont(Hfont)
            
            Ifont = QFont(*St.Item_Font)
            self.views[name].setFont(Ifont)
            ###
            Funcs.AllInOneLayout(self.tabWidget,[self.views[name]]) # add the self.view object to the self.tabWidget object's layout
            
            Tfont = QFont(*St.Tab_Font)
            self.myTabs.setFont(Tfont)
            self.views[name].setAlternatingRowColors(True);
            self.myTabs.addTab(self.tabWidget, str(name)) # Add this tab to myTabs
            self.models[name] = self.createTable(dict_bank_data[name], self.views[name]) # Call the create table function to create a table
        ###
        self.SearchBar = Search()
        self.SearchBar.setHidden(True)

        ### Sorting out the Layout
        Funcs.AllInOneLayout(self,[self.myTabs,self.SearchBar],VH='h',Stretches=[4,1]) # Add the sidebar_frame and myTabs to the layout of the page horizontally.
        ###
        
        self.show() # show the entire app
    
    # This function creates the table using a TableView
    def createTable(self, data, view):
        model = PandasModel(data) # Create a model and fill it with data
        view.setModel(model)
        view.setShowGrid(St.Show_Table_Grid_Lines)
        for i in range(1,len(dict_bank_data[act_nums[0]].columns)):
                self.headers.setSectionResizeMode(int(i),QHeaderView.Stretch)  
        view.resizeColumnsToContents() # Resize the column widths to fit the contents
        view.show()
        return model

    # This function will set the focus on the search bar.
    def search(self):
        self.SearchBar.setHidden(False)
        self.SearchBar.lineedit.selectAll()
        self.SearchBar.lineedit.setFocus()  
        
    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_F:
                self.search()
            elif e.key() == Qt.Key_R:
                print('bob')
        elif e.key() == Qt.Key_Escape:
            self.SearchBar.setHidden(True)
            self.setFocus()
        elif e.key() == Qt.Key_Return and self.SearchBar.lineedit.hasFocus():
            self.SearchBar.setHidden(True)
            search_item = self.SearchBar.lineedit.text()
            tabbar = self.myTabs.tabBar()
            Account_Number = int(tabbar.tabText(tabbar.currentIndex()))
            if search_item.lower() == '' or search_item.lower() == 'all':
                search_data = dict_bank_data[Account_Number]
            else:
                df = dict_bank_data[Account_Number]
                mask = column_stack([df[col].apply(str).apply(dr.lower).str.contains(search_item.lower(), na=False) for col in df])
                search_data = df.loc[mask.any(axis=1)]
            
            self.models[Account_Number].updateData(search_data)
            self.setFocus()


class Search(QFrame):
    
    def __init__(self):
        super(Search, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.lineedit = QLineEdit("Search...")
        self.lineedit.setFont(QFont(*St.Search_Bar_Font))
        self.lineedit.setStyleSheet(St.StyleSheets['Search'])
        
        Funcs.AllInOneLayout(self,[self.lineedit],VH='v',Align=Qt.AlignTop)
        self.show()
    

    
            
    