# Importing Modules from PyQt5
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QWidget, QStackedWidget
from PyQt5.QtGui import QColor

# Importing Modules from the App
from Gui.Table import TablePage
import Gui.StyleSheets as St


# The Main Window... This Widget will be the main window.
# Other widgets such as the TablePage and PlotPage will be called from here in a StackedWidget
class App(QWidget):
    
    def __init__(self):
        super(App, self).__init__()
        self.setWindowTitle('Finances App 2')  # Set the title of the app
        self.setGeometry(500, 500, 1600, 880) # Set the Geometry of the Window   
        
        ### Setting the Colour of the app background
        p = self.palette()
        b_col = QColor(*St.table_background_colour)
        p.setColor(self.backgroundRole(), b_col)
        self.setPalette(p)   
        
        self.initUI()
    
    def initUI(self):
        new_widget = TablePage()
        sidebar_frame = self.sideBar()
        self.AllInOneLayout(self,[sidebar_frame,new_widget],VH="H")
        
        self.show()
    
    def sideBar(self):
        sidebar_frame = QFrame()
        sidebar_frame.setMinimumWidth(110)
        sidebar_frame.setStyleSheet(St.StyleSheets['Sidebar'])
        
        button_titles = ['Data\nTables','Plotting']
        button_titles = button_titles + ['' for i in range(St.number_of_buttons_on_sidebar-len(button_titles))]
        buttons = []    
        for i in range(St.number_of_buttons_on_sidebar):
            button = QPushButton(button_titles[i])
            button.setMinimumSize(110,self.height()/St.number_of_buttons_on_sidebar)
            button.setStyleSheet(St.StyleSheets['Button%i'%i])
            buttons.append(button)
        self.AllInOneLayout(sidebar_frame,buttons,VH='V')#,Align=Qt.AlignTop) # add button and button2 to the sidebar_frame vertically, aligning them at the top.
        return sidebar_frame
    
    # A function to place objects in a layout.
    def AllInOneLayout(self,object,widgets,VH='V',Align=False):
        if VH == "V":
            layout = QVBoxLayout()
        elif VH == "H":
            layout = QHBoxLayout()
        
        if Align:
            layout.setAlignment(Align)
        
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for widg in widgets:
            layout.addWidget(widg)
        
        if object:
            object.setLayout(layout)
        return layout