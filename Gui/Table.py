# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtWidgets import QAbstractScrollArea, QTableView, QWidget, QTabWidget, QHeaderView, QLineEdit, QFrame, QLabel, QCheckBox
from PyQt5.QtGui import QFont, QColor

# Other Imports
from numpy import shape, column_stack, arange
from numpy.ma import masked_where, compressed
from pandas import DataFrame

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure

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
        
    # A function to change the data displayed in the table.
    def updateData(self, dataIn ,parent = QModelIndex()):
        self.beginRemoveRows(parent, 0, self.r-1) # Remove previous data
        self.endRemoveRows()
        #
        self._cols = dataIn.columns # update the table with the newly entered data.
        self.r, self.c = shape(dataIn) # Reset the vital stats of the table
        self.beginInsertRows(parent, 0, self.r-1) # insert the new data
        self._data = dataIn.values
        self.endInsertRows()
        
        
        return True


    
        
# The TablePage Widget, this will be shown in the main window when pressed.    
class TablePage(QWidget): # Create a class inheriting from the QMainWindow
    def __init__(self, parent=None):
        super(TablePage, self).__init__(parent)
        self.setGeometry(500, 500, 1600, 880) # Set the Geometry of the Window   
        
        ### Setting the Colour of the app background
        p = self.palette()
        b_col = QColor(*St.background_colour)
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
        
        self.tabbar = self.myTabs.tabBar()
        
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
    def searchOpen(self):
        self.SearchBar.setHidden(False)
        self.SearchBar.lineedit.selectAll()
        self.SearchBar.lineedit.setFocus()  
        
    def SearchAndDisplay(self):
        search_item = self.SearchBar.lineedit.text()
        Account_Number = int(self.tabbar.tabText(self.tabbar.currentIndex()))
        if search_item.lower() == '' or search_item.lower() == 'all':
            search_data = dict_bank_data[Account_Number]
        else:
            df = dict_bank_data[Account_Number]
            check_boxes = self.SearchBar.CheckBoxes.bxs
            cols = [check_boxes[i].text() for i in check_boxes if check_boxes[i].isChecked()]
            mask = column_stack([df[col].apply(str).apply(dr.lower).str.contains(search_item.lower(), na=False) for col in cols])
            search_data = df.loc[mask.any(axis=1)]
        xdata,ydata = self.dataPrep(search_data)
        self.SearchBar.CatPlot.plot(ydata, xdata)
        self.models[Account_Number].updateData(search_data)
        self.SearchBar.SearchCountLabel.setText("Search Count = %s"%str(self.models[Account_Number].r))
    
    # Preps data for the bar plot of the categories
    def dataPrep(self, data):
        try:
            data = data.loc[:,['Category','Out']]
            data['Out'] = data['Out'].apply(dr.dataPrep)
            data['Out'] = data['Out'].fillna(0)
            data = data.groupby('Category').sum()
            xdata = list(data.index)
            ydata = data.values[:,0]
            xdata = compressed(masked_where(ydata == 0, xdata))
            ydata = compressed(masked_where(ydata == 0, ydata))
            print(xdata,ydata)
            return (xdata,ydata)
        except KeyError:
            pass
    
    # Binds events to key presses
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_F: # Open search with Cntrl-F
                self.searchOpen()   
                
        if e.modifiers() == Qt.AltModifier: # Change between tabs with Alt-number
            self.tabbar.setCurrentIndex(e.key()-49)
            
        if e.key() == Qt.Key_Escape: # Exit the Search with Esc
            self.SearchBar.setHidden(True)
            self.setFocus()
            
        elif e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter and self.SearchBar.lineedit.hasFocus(): # Search for something with Enter
            self.SearchAndDisplay()            
            self.setFocus()


# The search bar frame
class Search(QFrame):
    
    def __init__(self):
        super(Search, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.Title = QLabel("Search Bar")
        self.Title.setAlignment(Qt.AlignCenter)
        self.Title.setFont(QFont(*St.Title_Font))
        
        self.lineedit = QLineEdit("Search...")
        self.lineedit.setFont(QFont(*St.Search_Bar_Font))
        self.lineedit.setStyleSheet(St.StyleSheets['Search'])
        
        self.CheckBoxes = CheckBoxes()
        
        self.CatPlot = PlotCanvas([],[])
        #self.CatPlot.setHidden(True)
        
        self.SearchCountLabel = QLabel("Search Count = ")  
        self.SearchCountLabel.setFont(QFont(*St.Search_Info_Font))
        Funcs.AllInOneLayout(self,[self.Title, self.lineedit, self.CheckBoxes, self.SearchCountLabel, self.CatPlot], VH='v', Stretches=[1,1,1,10,10], Align=Qt.AlignTop)

        self.show()
        
        

# A frame to hold the CheckBoxes horizontally
class CheckBoxes(QFrame):
    
    def __init__(self):
        super(CheckBoxes, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.bxs = {}
        for name in dict_bank_data[27274868].columns:
            self.bxs[name] = QCheckBox(str(name), self)
            self.bxs[name].setChecked(True)
            self.bxs[name].setStyleSheet(St.StyleSheets['Check Boxes'])
        
        Funcs.AllInOneLayout(self,list(self.bxs.values()),VH='h',Align=Qt.AlignTop)
        self.show()        
    
    
class PlotCanvas(FigureCanvas):
 
    def __init__(self,XData, YData, parent=None):
        self.parent = parent
        self.fig = self.make_figure()
        self.ax = self.fig.add_subplot(111)
        self.plot([],[])
        
    def plot(self, ydata, xlabels):
        error = False
        self.ax.cla()
        ind = arange(len(ydata))  # the x locations for the groups
        width = 0.05       # the width of the bars
        self.ax.bar(range(len(ydata)),ydata)
        self.ax.set_xticks(ind + width / 2)
        self.ax.set_xticklabels(xlabels, rotation='vertical')
        self.draw()
        self.ax.tick_params(labelsize=7)
        self.ax.set_ylabel("Count", fontsize=7)
        self.ax.set_xlabel("Category", fontsize=7)
        
        return error

            
    def make_figure(self):
        fig = Figure(facecolor='white')
        fig.subplots_adjust(0.1,0.25,0.95,0.95)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(self.parent)
 
        FigureCanvas.updateGeometry(self)
        return fig