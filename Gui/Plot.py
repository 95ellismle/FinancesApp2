# Imports from PyQt 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QWidget, QPlainTextEdit, QFrame, QPushButton, QStackedWidget, QTextEdit
from PyQt5.QtGui import QFont

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
 
# Other Imports
from numpy import array, gradient
from pandas.tslib import Timestamp as timstmp
from pandas import to_datetime

# Imports from other modules
from __main__ import dict_bank_data, act_nums
from Data import Data as dr
from Gui.Funcs import AllInOneLayout, abs_remove
from Gui import StyleSheets as St

Plot_Mesg = """# This is how to control the plotting.\n
# Set the data displayed on the x or the y-axis via the XData and YData commands respectively.\n 
# A full rundown of the commands will be provided in the README.md file.\n
# Feel free to delete all these comments (marked with a hash).
~For Help simply type 'help' anywhere in this box~
\nYData:  Balance;
"""

Help_Mesg = "#Feature Coming Soon"

class App_Bit(QWidget):
    def __init__(self):
        super().__init__()
        self.bob = 'bob'
        self.FullStack = QStackedWidget(self)
        self.PlotPageStackItem = PlotPage()
        self.HelpPageStackItem = HelpPage()
        
        self.FullStack.addWidget(self.PlotPageStackItem)
        self.FullStack.addWidget(self.HelpPageStackItem)
                
        AllInOneLayout(self,self.FullStack)
        self.show()
           
        
class PlotPage(QWidget):
 
    def __init__(self):
        super().__init__()
        self.plot_params = {}
        self.Plot_Mesg = Plot_Mesg        
        self.initUI()
    
    def initUI(self):    
        # The graph widgets
        self.Graph = PlotCanvas(XData=[1],YData=[1],parent=self)
        self.toolbar = NavBar(self.Graph, self)
        
        text_frame = QFrame() # A frame to put the textbox and the button in
        text_frame.setStyleSheet(St.StyleSheets['Text Frame'])
        
        self.control_box = QPlainTextEdit(self.Plot_Mesg)
        CFont = QFont(*St.Header_Font)
        self.control_box.setFont(CFont)
        self.control_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        OK_Button = QPushButton("Ok")
        OK_Button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        OK_Button.clicked.connect(self.Ok_Button_Click)
        OK_Button.setStyleSheet(St.StyleSheets['Ok Button'])
        AllInOneLayout(text_frame, [self.control_box, OK_Button],Stretches=[10,1], Align=Qt.AlignRight)
        
        AllInOneLayout(self,[self.Graph, text_frame], Stretches=[4,1], VH='H')
        
        self.show()
        
    # A function to connect the OK_Button on the bottom of the plotting page to retrieving the data and plotting it.
    def Ok_Button_Click(self):
        control_text = self.control_box.toPlainText()
        control_text = abs_remove(control_text)
        if 'help' in control_text.lower():
            self.parent().parent().FullStack.setCurrentIndex(1)
        else:
            self.plot_params = dr.dict_parser(control_text)
            self.Plot_Mesg = dr.dict2str(self.plot_params)
            self.control_box.setPlainText(self.Plot_Mesg)
            self.data_plot(self.plot_params)
    
    # Controls what gets plotted according to the control_box
    def data_plot(self, plt_prms):
        if 'Ydata' in plt_prms.keys():
            try:
                # Parse the parameters from the text
                y = self.dict_value_get(plt_prms, 'Ydata')
                x = self.dict_value_get(plt_prms, 'Xdata')
                act = self.dict_value_get(plt_prms, 'Act')
                act = self.act_num_handler(act,len(y))
                # Checking whether the parameters have been stated and if not set them to defaults
                x = self.not_var(x,'Date',len(y))
                
                Data = dict_bank_data[act[0]]
                XData = Data[x[0]].apply(dr.dataPrep)
                YData = Data[y[0]].apply(dr.dataPrep)
                e = self.Graph.plot(XData,YData)
                if e:
                    self.control_box.setPlainText("#Sorry there is something wrong with the format of the data that you want plotting\n")
                    self.control_box.appendPlainText("#Are you sure this is numeric data?\n")
                    self.control_box.appendPlainText("\n#Error = " + str(e))
                    self.control_box.appendPlainText("\n"+"#"*int(self.control_box.width()/15)+"\n\nYData: Balance;\nXData: Date;")
            except KeyError as e:

                self.control_box.setPlainText("#Sorry I can't find any data named '"+str(e)+"'.\n\n#The full list of data categories you can use are:")
                for i in dict_bank_data[act_nums[0]]:
                    self.control_box.appendPlainText("\t#"+str(i))
                self.control_box.appendPlainText("\n#Some of these may not be numeric and unavailable for plotting")
                self.control_box.appendPlainText("\n"+"#"*int(self.control_box.width()/15)+"\n\nYData: Balance;")
        else:
            self.control_box.setPlainText("# You at least need the Ydata Parameter, like below:")
            self.control_box.appendPlainText("\n\nYData: Balance;")
            
    # Just tries to get the values associated with a dictionary, if the key isn't there it silently throws an error    
    def dict_value_get(self,dictionary,value):
        value = [i for i in dictionary.keys() if value in i]
        try:
            return dictionary[value[0]]
        except IndexError:
            return False
    
    # Handles the parsing of the ydata and xdata parameters
    def dataParser(self,x,length_y):
        x = self.not_var(x,'Date',length_y)
        return x
    
    # Deals with the account number parameter
    def act_num_handler(self,act,length_of_y):
        ### If the account number parameters have been set convert them to ints
        if type(act) == list:
            act = [dr.str2int(i) for i in act] 
        ###
        act = self.not_var(act,act_nums[0],length_of_y) #If they haven't been set use default settings
        try:
            act = [act_nums[i-1] if i < 1000 else i for i in act] # If the chosen number is less than 1000, assume it is an index of the accounts rather than an account number
        except IndexError:
            pass  
        ### If the number doesn't exist in the known accounts then let the user know and use the default account
        for i in range(len(act)):
            if act[i] not in act_nums:
                self.control_box.appendPlainText("# Account number '%s' was not recognised using the default (first) account instead"%str(act[i]))
                act[i] = act_nums[0]
        ###
        return act
    
    # A very simple repeated function checking whether a function has any data
    def not_var(self,var,replace,repeat):
        try:
            if len(var) < repeat:
                var = var+[replace]*(repeat-len(var))
                return var
        except:
            pass
        if not var:
            var = [replace]*repeat
        return var
            
    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_Return:
                self.Ok_Button_Click()
            
class PlotCanvas(FigureCanvas):
 
    def __init__(self,XData, YData, parent=None):
        self.parent = parent
        Data = dict_bank_data[27274868]
        dr.convert_col(Data,'Date','Date')
        Data = Data.groupby('Date').last()
        Xdata,Ydata = [Data.index,Data['Balance']]
        self.count = 0
        self.fig = self.make_figure()
        self.ax = self.fig.add_subplot(111)
        self.plot(Xdata,Ydata)
        
    def plot(self,Xdata,Ydata,Ls='-',Color='g'):
        error = False
        self.ax.cla()
        try:
            if type(Xdata) == list and type(Ydata) == list:
                for i in range(len(Xdata)):
                    self.ax.plot(array(Xdata[i]),array(Ydata),'g.')
            else:
                self.ax.plot(array(Xdata),array(Ydata), 'g.')
        except ValueError as e:
            error = e
            print("Could Not Plot Data, Wrong Types were given")
            print("XData = \n",Xdata,"\nX-Type = ",type(Xdata[0]))
            print("YData = \n",Ydata,"\nY-Type = ",type(Ydata[0]))
        self.ax.grid(color='#b0b0b0', lw=0.5)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.tick_params(labelsize=15)
        try:        
            self.draw()
        except ValueError as e:
            error = e
        return error

    
    def make_figure(self):
        fig = Figure(facecolor='white')
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(self.parent)
 
        FigureCanvas.updateGeometry(self)
        fig.subplots_adjust(0.07,0.05,0.97,0.95)
        return fig
    

class HelpPage(QWidget):
 
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):    
        # The graph widgets
        f = open('./Gui/Help Page/Help_Page.html','r')
        help_page_html = f.read()
        f.close()
        self.Help_Box = QTextEdit()
        self.Help_Box.setHtml(help_page_html)
        self.Help_Box.setReadOnly(True)
        CFont = QFont(*St.Header_Font)
        self.Help_Box.setFont(CFont)
        self.Help_Box.setStyleSheet(St.StyleSheets['Text Frame'])
        self.Help_Box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
        AllInOneLayout(self,self.Help_Box)
    
    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.key():
            self.parent().parent().FullStack.setCurrentIndex(0)
