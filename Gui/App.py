# PyQt related imports
from PyQt5.QtWidgets import QAbstractScrollArea, QTableView, QWidget, QVBoxLayout, QTabWidget, QHeaderView
from PyQt5.QtGui import QFont, QColor


# Importing some required variables from the main code
from __main__ import dict_bank_data, act_nums
from Data import Data as dr
from Gui.StyleSheets import StyleSheets
from Gui.Table import PandasModel
    

class Main(QWidget): # Create a class inheriting from the QMainWindow
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setWindowTitle('Finances App 2')  # Set the title of the app
        self.setGeometry(500, 500, 900, 800) # Set the Geometry of the Window   
        
        ### Setting the Colour of the app background
        p = self.palette()
        background_colour = QColor(230,240,240,255)
        p.setColor(self.backgroundRole(), background_colour)
        self.setPalette(p)        
        ###
        self.initUI() # Call the initUI function to initialise things
        
    def initUI(self):      
        ### Dealing with the Tabs         
        self.myTabs = QTabWidget() # Creates the tab widget to hold the tabs
        for name in act_nums:
            tabWidget =  QWidget() # Creating a widget to hold a single tab
            self.view = QTableView(self) # Creating a table view to eventually put a pandas dataframe in
            self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            
            tabLayout = QVBoxLayout() #Creating a layout for the tabs
            tabLayout.addWidget(self.view) # Adding the view to the tab
            tabWidget.setLayout(tabLayout) # fixing the layout of the tabs with the created one above.
            
            self.myTabs.addTab(tabWidget, str(name)) # Add this tab to myTabs
            
            #self.setCentralWidget(self.view) # Changes the layout of the table view
    
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
        self.Display_Data['Date'] = self.Display_Data['Date'].apply(dr.date2time) # Making the datetime more readable
        self.model = PandasModel(self.Display_Data) # Create a model and fill it with data
        self.view.setModel(self.model)
        
        ### Change the header fonts
        font = QFont()
        font.setPointSize(14)
        headers = self.view.horizontalHeader()
        for i in range(len(data.columns)-3):
            headers.setSectionResizeMode(i,QHeaderView.Stretch)

        
        headers.setFont(font)
        ###
        self.view.setStyleSheet(StyleSheets['Table'])
        self.view.resizeColumnsToContents() # Resize the column widths to fit the contents
        self.view.setColumnWidth(0,300) # The description column is a bit large so make this a sensible size
        
        self.view.show()
    
    