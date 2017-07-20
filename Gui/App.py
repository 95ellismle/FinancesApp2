# Importing Modules from PyQt5
from PyQt5.QtWidgets import QSizePolicy, QPushButton, QFrame, QWidget, QStackedWidget
from PyQt5.QtGui import QColor

# Importing Modules from the App
from Gui import Table, Plot, Funcs, Budget
from Settings import StyleSheets as St

def smallerNumber(number1, number2):
    if number1 < number2:
        return number1
    else:
        return number2

def fill_a_list(List, filler, length):
    List = List + [filler for i in range(length)]
    return List


class App(QWidget):
    # The Main Window... This Widget will be the main window.
    # Other widgets such as the TablePage and PlotPage will be called from here in a StackedWidget
    def __init__(self):
        super(App, self).__init__()
        self.setWindowTitle('Finances App 2')  # Set the title of the app
        self.setGeometry(500, 500, 1600, 880) # Set the Geometry of the Window   
        
        ### Setting the Colour of the app background
        p = self.palette()
        b_col = QColor(St.background_colour)
        p.setColor(self.backgroundRole(), b_col)
        self.setPalette(p)   
        
        self.initUI()
    
    def initUI(self):
        self.TableStackItem = Table.TablePage()
        self.PlotStackItem = Plot.App_Bit()
        self.BudgetStackItem = Budget.SettingsPage()
        
        sidebar_frame = self.sideBar()
        
        self.FullStack = QStackedWidget(self)
        
        self.FullStack.addWidget(self.TableStackItem)
        self.FullStack.addWidget(self.PlotStackItem)
        self.FullStack.addWidget(self.BudgetStackItem)
        
        self.onTabButton()
        
        Funcs.AllInOneLayout(self,[sidebar_frame,self.FullStack],Stretches=[1,10],VH="H")
        
        self.show()
    
    def sideBar(self):
        sidebar_frame = QFrame()
        sidebar_frame.setMinimumWidth(110)
        #sidebar_frame.setStyleSheet(St.StyleSheets['Sidebar'])
        
        button_titles = ['Data\nTables','Plotting','Budget']
        button_titles = fill_a_list(button_titles, '', St.number_of_buttons_on_sidebar-len(button_titles))
        self.buttons = []   
        but_funcs = [self.onTabButton, self.onPlotButton, self.onBudgetButton ]
        but_funcs = fill_a_list(but_funcs, self.emptyFunc, St.number_of_buttons_on_sidebar-len(but_funcs))
        for i in range(St.number_of_buttons_on_sidebar):
            button = QPushButton(button_titles[i])
            button.setStyleSheet(St.StyleSheets['Button%i'%i])
            button.clicked.connect(but_funcs[i])
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.setCheckable(True)
            self.buttons.append(button)
            
        Funcs.AllInOneLayout(sidebar_frame, self.buttons, VH='V')# add button and button2 to the sidebar_frame vertically, aligning them at the top.
                
        #frame_layout.setSizeLayout(QSizePolicy.Expanding, QSizePolicy.Expanding)        
        return sidebar_frame
    
    # These buttons change which widget we can see in the stacked widget
    def onTabButton(self):
        self.TableStackItem.setFocus()
        self.FullStack.setCurrentIndex(0)

    def onPlotButton(self):
        self.PlotStackItem.setFocus()
        self.FullStack.setCurrentIndex(1)
    
    def onBudgetButton(self):
        self.BudgetStackItem.setFocus()
        self.FullStack.setCurrentIndex(2)

    
    def emptyFunc(self):
        return 0