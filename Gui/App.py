# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtWidgets import QAbstractScrollArea, QTableView, QWidget, QVBoxLayout, QTabWidget, QHeaderView
from PyQt5.QtGui import QFont, QColor


# Importing some required variables from the main code
from __main__ import dict_bank_data, act_nums
from Data import Data as dr
from Gui.StyleSheets import StyleSheets, background_colour
from Gui.Table import PandasModel
    

class Main(QWidget): # Create a class inheriting from the QMainWindow
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setWindowTitle('Finances App 2')  # Set the title of the app
        self.setGeometry(500, 500, 900, 800) # Set the Geometry of the Window   
        
        ### Setting the Colour of the app background
        p = self.palette()
        b_col = QColor(background_colour[0],background_colour[1],background_colour[2],background_colour[3])
        p.setColor(self.backgroundRole(), b_col)
        self.setPalette(p)   
        ###
        self.initUI() # Call the initUI function to initialise things
        
    def initUI(self):      
        ### Dealing with the Tabs         
        self.myTabs = QTabWidget() # Creates the tab widget to hold the tabs
        self.myTabs.setStyleSheet(StyleSheets['tab'])
        for name in act_nums:
            tabWidget =  QWidget() # Creating a widget to hold a single tab
            self.view = QTableView(self) # Creating a table view to eventually put a pandas dataframe in
            self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            ### Change the header fonts
            font = QFont()
            font.setPointSize(14)
            self.headers = self.view.horizontalHeader()
            self.headers.setFont(font)
            ###
            tabLayout = QVBoxLayout() #Creating a layout for the tabs
            tabLayout.addWidget(self.view) # Adding the view to the tab
            tabWidget.setLayout(tabLayout) # fixing the layout of the tabs with the created one above.
            font.setPointSize(13)
            self.myTabs.setFont(font)
            self.view.setAlternatingRowColors(True);
            self.myTabs.addTab(tabWidget, str(name)) # Add this tab to myTabs
            self.createTable(dict_bank_data[name]) # Call the create table function to create a table
        ###
        
        ### Sorting out the Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.myTabs)
        self.setLayout(mainLayout)
        ###
        
        self.show() # show the entire app

    # This function creates the table using a TableView
    def createTable(self, data):
        self.Display_Data = data # Making a new dataframe to hold the data for display
        self.Display_Data['Date'] = self.Display_Data['Date'].apply(dr.date2str) # Making the datetime more readable
        self.model = PandasModel(self.Display_Data) # Create a model and fill it with data
        self.view.setModel(self.model)
        self.view.setShowGrid(False)
        for i in range(1,len(dict_bank_data[act_nums[0]].columns)):
                self.headers.setSectionResizeMode(int(i),QHeaderView.Stretch)  
        self.view.setStyleSheet(StyleSheets['Table'])
        self.view.resizeColumnsToContents() # Resize the column widths to fit the contents
        
        self.view.show()
    
    