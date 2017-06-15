#!/usr/bin/python3

# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex, QVariant, QStringListModel
from PyQt5.QtWidgets import QAbstractScrollArea, QSizePolicy, QTableView, QWidget, QTabWidget, QHeaderView, QLineEdit, QFrame, QLabel, QCheckBox, QCalendarWidget, QPushButton, QCompleter
from PyQt5.QtGui import QFont, QColor

# Other Imports
from numpy import shape, column_stack, arange, around
from numpy.ma import masked_where, compressed
from datetime import datetime as dt

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Importing some required variables from the main code
from __main__ import dict_DATA as dict_bank_data
from Data import Data as dr
from Gui import Funcs
import Gui.StyleSheets as St


test_list = ['Bob','Aarav','Afia','Jane']
act_nums = list(dict_bank_data.keys())
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
            if role == Qt.EditRole: # Make the data editable
                return dr.TablePrep(self._data[index.row(),index.column()])
                
            if role == Qt.DisplayRole: # Displays the data
                return dr.TablePrep(self._data[index.row(),index.column()])
            
            if role == Qt.TextColorRole:
                colind = index.column()
                col = self._cols[colind]
                row = index.row()
                if col == 'Balance' and float(self._data[row,colind]) < 0:
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
                self._data[row,col] = dr.TablePrep(value) # Set the data to the newly typed value
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
        b_col = QColor(St.background_colour)
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
    
    # A function to search the data and display the required items
    def SearchAndDisplay(self):
        search_item = self.SearchBar.lineedit.text() #grab the search text
        Account_Number = int(self.tabbar.tabText(self.tabbar.currentIndex())) #Find the account number
        if search_item.lower() == '' or search_item.lower() == 'all' or search_item == "Search...":
            search_data = dict_bank_data[Account_Number] # reset the data if the above are typed in ^
            search_data = self.DateSplice(search_data,self.SearchBar.date1,self.SearchBar.date2)
        else:
            df = dict_bank_data[Account_Number] # find the data that corresponds to the tab currently selected
            df = self.DateSplice(df,self.SearchBar.date1,self.SearchBar.date2)
            check_boxes = self.SearchBar.CheckBoxes.bxs 
            cols = [check_boxes[i].text() for i in check_boxes if check_boxes[i].isChecked()] # find which columns to search according to the check boxes
            mask = column_stack([df[col].apply(str).apply(dr.lower).str.contains(search_item.lower(), na=False) for col in cols]) # The actual search. This constructs a Ndarray of booleans (a mask). True means the search condition has been met.
            search_data = df.loc[mask.any(axis=1)] # Applying the mask to the data.
        
        self.plotCategories(search_data) # Plots a little bar chart of the categorised data
        self.models[Account_Number].updateData(search_data)
        
        self.SearchBar.SearchCountLabel.setText("Total Spend = £%s\nSearch Count = %s\nAvg Per Item= £%s\nDaily Avg = £%s"%(self.statFinder(search_data)))
    
    # Finds averages and sums
    def statFinder(self, data):
        total_spend = data['Out'].apply(dr.str2float).sum()
        item_count  = len(data)
        if item_count > 0:
            item_avg   = format(total_spend/item_count,",.2f")
            first_date = min(data['Date'])
            second_date = max(data['Date'])
            time_delta = second_date-first_date
            daily_avg = format(total_spend/time_delta.days,",.2f")
        else:
            item_avg = '-'
            daily_avg = '-'
        total_spend = format(total_spend, ",.0f")
        return str(total_spend), format(item_count,',d'), str(item_avg), str(daily_avg)
    
    # Plot the categories in a bar chart
    def plotCategories(self, data):
        xdata,ydata = self.SearchBar.dataPrep(data)
        self.SearchBar.CatPlot.plot(xdata, ydata)
        
    #Will splice data between 2 given dates.
    def DateSplice(self, data, date1, date2):
        data = data.loc[data['Date'] < date2]
        data = data.loc[data['Date'] > date1]
        return data
    
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
               
        self.ButtonFrame = DateButtons()
        self.ButtonFrame.Date1Button.clicked.connect(self.onButtonClick1)
        self.ButtonFrame.Date2Button.clicked.connect(self.onButtonClick2)
        self.ButtonFrame.ResetDateButton.clicked.connect(self.DateReset)
        
        self.DateLabel = QLabel("")
        self.DateLabel.setFont(QFont(*St.Search_Info_Font))
        
        self.calender = QCalendarWidget(self)
        self.calender.setHidden(True)
        self.calender.clicked.connect(self.closeCalender)
        
        self.SearchCountLabel = QLabel("Total Spend = \nSearch Count = \nAverage Spend\nDaily Avg = ")  
        self.SearchCountLabel.setFont(QFont(*St.Search_Info_Font))

        self.CatPlot = PlotCanvas([],[])
        xdata,ydata = self.dataPrep(dict_bank_data[act_nums[0]])
        self.CatPlot.plot(xdata, ydata)
        
        Funcs.AllInOneLayout(self,[self.Title, self.lineedit, self.CheckBoxes, self.ButtonFrame, self.DateLabel, self.calender, self.SearchCountLabel, self.CatPlot], VH='v', Stretches=[1,1,1,1,1,1,10,12], Align=Qt.AlignTop)

        self.show()
    
    def onButtonClick1(self):
        self.calender.setHidden(False)
        self.datenum = 1
        
    def onButtonClick2(self):
        self.calender.setHidden(False)
        self.datenum = 2
    
    def DateReset(self):
        self.date1 = dt.strptime("01/01/1970","%d/%m/%Y")
        self.date2 = dt.now()
        self.parent().SearchAndDisplay()
    
    def closeCalender(self):
        self.calender.setHidden(True)
        if self.datenum == 1:
            self.date1 = self.calender.selectedDate().toPyDate()
            self.DateLabel.setText("%s -> %s"%(dr.date2str(self.date1),dr.date2str(self.date2)))
        elif self.datenum == 2:
            self.date2 = self.calender.selectedDate().toPyDate()
        self.parent().SearchAndDisplay()
            
        
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
            return (xdata,ydata)
        except KeyError:
            pass

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

        Funcs.AllInOneLayout(self, [self.Date1Button, self.Date2Button, self.ResetDateButton], VH='h')
        
        self.show()
        

# A frame to hold the CheckBoxes horizontally, these control the search behaviour
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
        
    def plot(self, xlabels, ydata):
        error = False
        self.ax.cla()
        ind = arange(len(ydata))  # the x locations for the groups
        width = 0.05       # the width of the bars
        self.ax.bar(range(len(ydata)),ydata)
        self.ax.set_xticks(ind + width / 2)
        self.ax.set_xticklabels(xlabels, rotation='vertical')
        self.draw()
        self.ax.tick_params(labelsize=7)
        self.ax.set_ylabel("Money Out / £", fontsize=7)
        self.ax.set_xlabel("Category", fontsize=7)
        
        return error

            
    def make_figure(self):
        fig = Figure(facecolor='white')
        fig.subplots_adjust(0.13,0.25,0.95,0.98)
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(self.parent)
 
        FigureCanvas.updateGeometry(self)
        return fig