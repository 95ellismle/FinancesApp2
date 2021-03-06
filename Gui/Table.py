#!/usr/bin/python3

# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant
from PyQt5.QtWidgets import QAbstractScrollArea, QSizePolicy, QTableView, QWidget, QTabWidget, QHeaderView, QLineEdit, QFrame, QLabel, QCheckBox, QCalendarWidget, QPushButton
from PyQt5.QtGui import QFont, QColor

# Other Imports
from numpy import shape, column_stack, arange
from datetime import datetime as dt

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Importing some required variables from the main code
from __main__ import dict_DATA as dict_bank_data
from Data import Data as dr
from Data import Type_Convert as tc
from Data import Stats as stats
import Gui.Funcs as fncs
from Settings import StyleSheets as St

Editted_Items = []
test_list = ['Bob', 'Aarav', 'Afia', 'Jane']
act_nums = dr.new_act_names
colums = dict_bank_data[act_nums[0]].columns
# This is some code modified from https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame
# I found the tableWidget was flagging in terms of performance for even smallish datasets (1,000+).
# This QAbstractTableModel seems to perform much better when populating a tableView with a pandas dataframe.
class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        self.counter = 0
        QAbstractTableModel.__init__(self, parent)
        self._data = data.values            # Returns a set of numpy arrays where each array contains a row from the dataframe in order.
        self._cols = data.columns           # Gets the dataframe columns
        self.r, self.c = shape(self._data)  # Finds the dimensions of the dataframe
     
    ### rowCount, columnCount and data are all necessary functions to call when using the QAbstractTableModel.
    def rowCount(self, parent=None): #Controls the amount of rows in the tableview
        return self.r
    
    def columnCount(self, parent=None): #Controls the amount of columns
        return self.c

    def data(self, index, role): #Controls how the data looks in the table
        global Editted_Items
        if index.isValid():
            rowI, colI = index.row(), index.column()
            if role == Qt.EditRole:
                if (rowI, colI) not in Editted_Items:
                    Editted_Items.append((rowI, colI))
                return tc.tablePrep(self._data[rowI, colI])
                
            if role == Qt.DisplayRole: # Displays the data
                if type(tc.tablePrep(self._data[rowI, colI])) != str:
                    print(type(tc.tablePrep(self._data[rowI, colI])))
                return tc.tablePrep(self._data[rowI, colI])
            
            if role == Qt.TextColorRole:
                col = self._cols[colI]
                row = rowI
                if col == 'Balance' and float(self._data[row, colI]) < 0:
                    return QVariant(QColor('#ff0000')) 
            
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
                self._data[row, col] = tc.tablePrep(value) # Set the data to the newly typed value
                return True
            return False
        
    # A function to change the data displayed in the table.
    def updateData(self, dataIn, parent = QModelIndex()):
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
        b_col = QColor(St.background_colour)
        p.setColor(self.backgroundRole(), b_col)
        self.setPalette(p)   
        self.search_data = stats.statFinder(dict_bank_data[act_nums[0]])
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
            fncs.AllInOneLayout(self.tabWidget, [self.views[name]]) # add the self.view object to the self.tabWidget object's layout
            
            Tfont = QFont(*St.Tab_Font)
            self.myTabs.setFont(Tfont)
            self.views[name].setAlternatingRowColors(True);
            self.myTabs.addTab(self.tabWidget, str(name)) # Add this tab to myTabs
            self.models[name] = self.createTable(dict_bank_data[name], self.views[name]) # Call the create table function to create a table
        ###
        
        
        self.tabbar = self.myTabs.tabBar()
                
        self.SearchBar = Search(self)
        self.SearchBar.setHidden(True)

        ### Sorting out the Layout
        fncs.AllInOneLayout(self, [self.myTabs, self.SearchBar], VH='h', Stretches=[4, 1]) # Add the sidebar_frame and myTabs to the layout of the page horizontally.
        ###
        
        self.show() # show the entire app
    
    # This function creates the table using a TableView
    def createTable(self, data, view):
        model = PandasModel(data) # Create a model and fill it with data
        view.setModel(model)
        view.setShowGrid(St.Show_Table_Grid_Lines)
        for i in range(1, len(dict_bank_data[act_nums[0]].columns)):
                self.headers.setSectionResizeMode(int(i), QHeaderView.Stretch)  
        view.resizeColumnsToContents() # Resize the column widths to fit the contents
        view.show()
        return model

    # This function will set the focus on the search bar.
    def searchOpen(self):
        self.SearchBar.setHidden(False)
        self.SearchBar.lineedit.selectAll()
        self.SearchBar.lineedit.setFocus()  
    
    # A function to search the data and display the required items
    def SearchAndDisplay(self):
        search_item = self.SearchBar.lineedit.text().lower() #grab the search text
        Account_Number = self.tabbar.tabText(self.tabbar.currentIndex()) #Find the account number
        if search_item == '' or search_item == 'all' or search_item == "search...":
            self.search_data = dict_bank_data[Account_Number] # reset the data if the above are typed in ^
            self.search_data = dr.DateSplice(self.search_data, self.SearchBar.date1, self.SearchBar.date2)
        else:
            df = dict_bank_data[Account_Number] # find the data that corresponds to the tab currently selected
            df = dr.DateSplice(df, self.SearchBar.date1, self.SearchBar.date2)
            check_boxes = self.SearchBar.CheckBoxes.bxs 
            cols = [check_boxes[i].text() for i in check_boxes if check_boxes[i].isChecked()] # find which columns to search according to the check boxes
            mask = column_stack([df[col].apply(tc.lower).str.contains(search_item, na=False) for col in cols]) # The actual search. This constructs a Ndarray of booleans (a mask). True means the search condition has been met.
            self.search_data = df.loc[mask.any(axis=1)] # Applying the mask to the data.
        
        self.plotCategories(self.search_data) # Plots a little bar chart of the categorised data
        self.models[Account_Number].updateData(self.search_data)
        self.SearchBar.model.updateData(stats.statFinder(self.search_data))
        

    # Plot the categories in a bar chart
    def plotCategories(self, data):
        xdata,ydata = stats.catFinder(data)
        self.SearchBar.CatPlot.plot(xdata, ydata)
        
    
    # Binds events to key presses
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_F: # Open search with Cntrl-F
                self.searchOpen()       
        elif e.modifiers() == Qt.AltModifier: # Change between tabs with Alt-number
            self.tabbar.setCurrentIndex(e.key()-49)
        
        if e.key() == Qt.Key_Escape: # Exit the Search with Esc
            self.SearchBar.setHidden(True)
            self.setFocus()
        elif e.key() == Qt.Key_Return and self.SearchBar.lineedit.hasFocus(): # Search for something with Enter
            self.SearchAndDisplay()            
            self.setFocus()
        elif e.key() == Qt.Key_Return and any(self.views[i].hasFocus for i in self.views):
            global Editted_Items
            Account_Number = self.tabbar.tabText(self.tabbar.currentIndex()) #Find the account number
            for i in range(len(Editted_Items)):
                rowT,colI = Editted_Items[i][0], Editted_Items[i][1]
                col = colums[colI]
                if col == 'Category':
                    time = self.models[Account_Number]._data[rowT,4]
                    balance = self.models[Account_Number]._data[rowT,5]
                    same_day = dict_bank_data[Account_Number].loc[dict_bank_data[Account_Number]["Date"] == time]
                    same_item = same_day.loc[same_day['Balance'] == balance]
                    current_category = str(same_item['Category'].values[0])
                    editted_category = self.models[Account_Number]._data[rowT,colI]
                    if current_category != editted_category:
                        entry = str(self.models[Account_Number]._data[rowT,6])
                        for i in [0,5,2,3,4]:
                            entry = entry + ';' + str(self.models[Account_Number]._data[rowT,i])
                        entry = entry.lower()
                        if entry not in dr.exceptions[0]:
                            f = open('Settings/Exceptions.txt','a')
                            f.write(entry+'|'+editted_category+"\n")
                            f.close()
                            print("Changed the category from "+current_category+" to "+editted_category+" for "+str(self.models[Account_Number]._data[rowT,0]))
            Editted_Items = []
                            
# The search bar frame
class Search(QFrame):
    
    def __init__(self, parent):
        super(Search, self).__init__(parent)
        self.setStyleSheet(St.StyleSheets['Search'])
        self.datenum = 1
        self.date1 = dt.strptime("01/01/1970","%d/%m/%Y")
        self.date2 = dt.now()
        self.initUI()
    
    def initUI(self):
        self.Title = QLabel("Search Bar")
        self.Title.setAlignment(Qt.AlignCenter)
        self.Title.setFont(QFont(*St.Title_Font))
        
        self.lineedit = QLineEdit("Search...")
        self.lineedit.setFont(QFont(*St.Search_Bar_Font))
        self.lineedit.setStyleSheet(St.StyleSheets['Search'])
                
        self.CheckBoxes = CheckBoxes()
        
        self.view = QTableView()
        self.view.setStyleSheet(St.StyleSheets['Info Table'])
        self.model = self.createTable(self.parent().search_data, self.view)
        
        self.ButtonFrame = DateButtons()
        self.ButtonFrame.Date1Button.clicked.connect(self.onButtonClick1)
        self.ButtonFrame.Date2Button.clicked.connect(self.onButtonClick2)
        self.ButtonFrame.ResetDateButton.clicked.connect(self.DateReset)
        
        self.DateLabel = QLabel("")
        self.DateLabel.setFont(QFont(*St.Search_Info_Font))
        
        self.calender = QCalendarWidget(self)
        self.calender.setHidden(True)
        self.calender.clicked.connect(self.closeCalender)

        self.CatPlot = PlotCanvas([],[])
        xdata,ydata = stats.catFinder(dict_bank_data[act_nums[0]])
        self.CatPlot.plot(xdata, ydata)
        
        fncs.AllInOneLayout(self,[self.Title, self.lineedit, self.CheckBoxes, self.ButtonFrame, self.DateLabel, self.calender, self.view, self.CatPlot], VH='v', Stretches=[1,1,1,1,1,6,4,12], Align=Qt.AlignTop)

        self.show()
    
    def onButtonClick1(self):
        self.calender.setHidden(not self.calender.isHidden())
        self.datenum = 1
        
    def onButtonClick2(self):
        self.calender.setHidden(not self.calender.isHidden())       
        self.datenum = 2
    
    def DateReset(self):
        self.date1 = dt.strptime("01/01/1970","%d/%m/%Y")
        self.calbut1change(self.date1)
        self.date2 = dt.now()
        self.calbut2change(self.date2)
        self.parent().SearchAndDisplay()
    
    def calbut1change(self, date): 
        strdate1 = tc.date2str(date)
        self.ButtonFrame.Date1Button.setText(strdate1)
        
    def calbut2change(self, date):
        strdate2 = tc.date2str(date)
        self.ButtonFrame.Date2Button.setText(strdate2)
    
    def closeCalender(self):
        self.calender.setHidden(True)
        if self.datenum == 1:
            self.date1 = self.calender.selectedDate().toPyDate()
            self.calbut1change(self.date1)
        elif self.datenum == 2:
            self.date2 = self.calender.selectedDate().toPyDate()
            self.calbut2change(self.date2)
        self.parent().SearchAndDisplay()
            
    # This function creates the table using a TableView
    def createTable(self, data, view):
        model = InfoTable(data) # Create a model and fill it with data
        view.setModel(model)
        view.setShowGrid(St.Show_Table_Grid_Lines)
        headers = view.horizontalHeader()
        headers.setSectionResizeMode(0,QHeaderView.Stretch)  
        headers.setSectionResizeMode(1,QHeaderView.Stretch)  
        headers.setFont(QFont(*St.Search_Bar_Font))
        view.resizeColumnsToContents() # Resize the column widths to fit the contents
        view.show()
        return model
        
    

# A Frame to hold some buttons to control the date setting in the table
class DateButtons(QFrame):
    def __init__(self):
        super(DateButtons, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.Date1Button = QPushButton("Date 1")
        self.Date2Button = QPushButton("Date 2")
        self.ResetDateButton = QPushButton("Reset Date")
        
        self.Date1Button.setFont(QFont(*St.Search_Info_Font))
        self.Date2Button.setFont(QFont(*St.Search_Info_Font))
        self.ResetDateButton.setFont(QFont(*St.Search_Info_Font))
        
        self.Date1Button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.Date2Button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ResetDateButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.Date1Button.setStyleSheet(St.StyleSheets['Date Buttons'])
        self.Date2Button.setStyleSheet(St.StyleSheets['Date Buttons'])
        self.ResetDateButton.setStyleSheet(St.StyleSheets['Date Buttons'])

        fncs.AllInOneLayout(self, [self.Date1Button, self.Date2Button, self.ResetDateButton], VH='h')
        
        self.show()
        


# A frame to hold the CheckBoxes horizontally, these control the search behaviour
class CheckBoxes(QFrame):
    
    def __init__(self):
        super(CheckBoxes, self).__init__()
        self.initUI()
    
    def initUI(self):
        self.bxs = {}
        for name in dict_bank_data[act_nums[0]].columns:
            self.bxs[name] = QCheckBox(str(name), self)
            self.bxs[name].setChecked(True)
            self.bxs[name].setStyleSheet(St.StyleSheets['Check Boxes'])
        
        fncs.AllInOneLayout(self,list(self.bxs.values()),VH='h',Align=Qt.AlignTop)
        self.show()        
    
    
class PlotCanvas(FigureCanvas):
 
    def __init__(self,XData, YData, parent=None):
        self.parent = parent
        self.fig = self.make_figure()
        self.ax = self.fig.add_subplot(111)
        self.plot([],[])
        
    def plot(self, xlabels, ydata):
        error = False
        self.ax.cla()
        ind = arange(len(ydata))  # the x locations for the groups
        width = 0.05       # the width of the bars
        self.ax.bar(range(len(ydata)),ydata)
        self.ax.set_xticks(ind + width / 2)
        self.ax.set_xticklabels(xlabels, rotation='vertical')
        self.ax.grid(color='white')
        self.ax.tick_params(labelsize=7)
        self.ax.set_ylabel("Money Out / £", fontsize=7)
        self.ax.set_xlabel("Category", fontsize=7)
        
        self.draw()
        
        return error

            
    def make_figure(self):
        fig = Figure(facecolor='white')
        fig.subplots_adjust(0.13,0.25,0.95,0.98)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(self.parent)
 
        FigureCanvas.updateGeometry(self)
        return fig



# Will populate a TableView with the stats on the table data. This is has only been slightly modified from the above PandasModel
class InfoTable(QAbstractTableModel):
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
            if role == Qt.DisplayRole: # Displays the data
                return tc.tablePrep(self._data[index.row(),index.column()])
            
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter

            if role == Qt.TextColorRole:
                col = index.column()
                if col == 0:
                    return QVariant(QColor('#228B22'))
                if col == 1:
                    return QVariant(QColor('#65000B'))
        return None
    ###
    # This modifies the headerData, Qt.Horizontal will edit the horizontal headers, Vertical ones will be row headers.
    # p_int is the header index
    def headerData(self, p_int, orientation, role):
        headers = ['Total','Count','Avg Per Item','Daily Avg']
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._cols[p_int])
            elif orientation == Qt.Vertical:
                return headers[p_int]
        return None

    # This will modify the data in the table if it is changed in the table
    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole: 
            row = index.row()
            col = index.column()
            if type(value) == str:
                self._data[row,col] = tc.tablePrep(value) # Set the data to the newly typed value
                return True
            return False
        
    # A function to change the data displayed in the table.
    def updateData(self, dataIn, parent = QModelIndex()):
        self.beginRemoveRows(parent, 0, self.r-1) # Remove previous data
        self.endRemoveRows()
        #
        self._cols = dataIn.columns # update the table with the newly entered data.
        self.r, self.c = shape(dataIn) # Reset the vital stats of the table
        self.beginInsertRows(parent, 0, self.r-1) # insert the new data
        self._data = dataIn.values
        self.endInsertRows()
        
        return True
