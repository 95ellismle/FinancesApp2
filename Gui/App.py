# PyQt related imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QFrame, QAbstractScrollArea, QTableView, QWidget, QHBoxLayout, QVBoxLayout, QTabWidget, QHeaderView, QPushButton
from PyQt5.QtGui import QFont, QColor


# Importing some required variables from the main code
from __main__ import dict_bank_data, act_nums
from Data import Data as dr
from Gui.StyleSheets import StyleSheets, table_background_colour
from Gui.Table import PandasModel


class Main(QWidget): # Create a class inheriting from the QMainWindow
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setWindowTitle('Finances App 2')  # Set the title of the app
        self.setGeometry(500, 500, 1000, 800) # Set the Geometry of the Window   
        
        ### Setting the Colour of the app background
        p = self.palette()
        b_col = QColor(table_background_colour[0],table_background_colour[1],table_background_colour[2],table_background_colour[3])
        p.setColor(self.backgroundRole(), b_col)
        self.setPalette(p)   
        ###
        self.initUI() # Call the initUI function to initialise things
        
    def initUI(self):      
        sidebar_frame = QFrame()
        sidebar_frame.setMinimumWidth(110)
        sidebar_frame.setStyleSheet(StyleSheets['sidebar'])
        
        sidebar_layout = QVBoxLayout()
        
        button = QPushButton("Button 1")
        button.setMinimumSize(110,100)
        button.setStyleSheet(StyleSheets['button1'])
        button.clicked.connect(self.on_click)
    
        button2 = QPushButton("Button 2")
        button2.setMinimumSize(110,100)
        button2.setStyleSheet(StyleSheets['button2'])
        button2.clicked.connect(self.on_click)
        
        sidebar_frame.setLayout(sidebar_layout)
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(0,0,0,0)
        sidebar_layout.addWidget(button,1)
        sidebar_layout.addWidget(button2,1)
        
        ### Dealing with the Tabs         
        self.myTabs = QTabWidget(self) # Creates the tab widget to hold the tabs
        self.myTabs.setMinimumHeight(100)
        self.myTabs.setStyleSheet(StyleSheets['tab'])
        for name in act_nums:
            self.tabWidget =  QWidget() # Creating a widget to hold a single tab
            self.view = QTableView(self) # Creating a table view to eventually put a pandas dataframe in
            self.view.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            self.tabWidget.setStyleSheet(StyleSheets['tab'])
            ### Change the header fonts
            font = QFont()
            font.setPointSize(15)
            self.headers = self.view.horizontalHeader()
            self.headers.setDefaultAlignment(Qt.AlignLeft|Qt.AlignVCenter)
            self.headers.setFont(font)
            ###
            tabLayout = QVBoxLayout() #Creating a layout for the tabs
            tabLayout.setContentsMargins(0,0,0,0)
            tabLayout.addWidget(self.view) # Adding the view to the tab
            self.tabWidget.setLayout(tabLayout) # fixing the layout of the tabs with the created one above.
            font.setPointSize(13)
            self.myTabs.setFont(font)
            self.view.setAlternatingRowColors(True);
            self.myTabs.addTab(self.tabWidget, str(name)) # Add this tab to myTabs
            self.createTable(dict_bank_data[name]) # Call the create table function to create a table
        ###
        
        ### Sorting out the Layout
        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0,0,0,0)
        mainLayout.addWidget(sidebar_frame)
        mainLayout.addWidget(self.myTabs)
        self.setLayout(mainLayout)
        ###
        
        self.show() # show the entire app
        
    def on_click(self):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)
    
       msg.setText("Hello, this is a test of the button")
       msg.setWindowTitle("Tennis?")
       msg.setStandardButtons(QMessageBox.Ok)
       msg.buttonClicked.connect(self.msgbtn)
    	
       retval = msg.exec_()
       print("value of pressed message box button:", retval)
    	
    def msgbtn(self,i):
       print("Button pressed is:",i.text())

    # This function creates the table using a TableView
    def createTable(self, data):
        self.Display_Data = data # Making a new dataframe to hold the data for display
        self.Display_Data['Date'] = self.Display_Data['Date'].apply(dr.date2str) # Making the datetime more readable
        self.model = PandasModel(self.Display_Data) # Create a model and fill it with data
        self.view.setModel(self.model)
        self.view.setShowGrid(False)
        for i in range(1,len(dict_bank_data[act_nums[0]].columns)):
                self.headers.setSectionResizeMode(int(i),QHeaderView.Stretch)  
        self.view.setStyleSheet(StyleSheets['table'])
        self.view.resizeColumnsToContents() # Resize the column widths to fit the contents
        
        self.view.show()
    
    