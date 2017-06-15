# Imports from PyQt 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QWidget, QPlainTextEdit, QFrame, QPushButton, QStackedWidget, QTextEdit
from PyQt5.QtGui import QFont

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
#import matplotlib.pyplot as plt
 
# Other Imports
from numpy import array

# Imports from other modules
from __main__ import dict_DATA as dict_bank_data
from __main__ import Plottable_cols
from Data import Data as dr
from Gui.Funcs import AllInOneLayout, dict_value_get
from Gui import StyleSheets as St
act_nums = list(dict_bank_data.keys())
Plot_Mesg = """# This is how to control the plotting.\n
# Set the data displayed on the x or the y-axis via the XData and YData commands respectively.\n 
# For Help simply type press Cntrl-H (you may need to click this textbox).
\nYData:  Balance;
"""

default_plots = {'balance':{'color':'#568203','ls':'-','type':'scatter'},'in':{'color':'#00ff5a','width':3,'type':'bar','edgecolor':None},'out':{'color':'r','width':1.4,'type':'bar','edgecolor':'r'}}

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
    
    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_H:
                self.FullStack.setCurrentIndex(1)
        elif e.key():
            self.FullStack.setCurrentIndex(0)
           
        
class PlotPage(QWidget):
 
    def __init__(self):
        super().__init__()
        self.plot_params = {}
        self.Plot_Mesg = Plot_Mesg    
        self.length_y = 1
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
        self.plot_params = dr.dict_parser(control_text)
        self.Plot_Mesg = dr.dict2str(self.plot_params)
        self.control_box.setPlainText(self.Plot_Mesg)
        self.data_plot(self.plot_params)

    # Controls what gets plotted according to the control_box
    def data_plot(self, plt_prms):
        if 'Ydata' in plt_prms.keys():
            try:
                # Parse the parameters from the text
                y = dict_value_get(plt_prms, 'Ydata')
                self.length_y  = len(y)
                x = dict_value_get(plt_prms, 'Xdata')
                act = dict_value_get(plt_prms, 'Act')
                act = self.act_num_handler(act)
                # Checking whether the parameters have been stated and if not set them to defaults
                x = self.not_var(x,'Date')
                
                e = self.Graph.plot(x,y,act)
                if e:
                    self.control_box.setPlainText("#Sorry there is something wrong with the format of the data that you want plotting\n")
                    self.control_box.appendPlainText("#Are you sure this is numeric data?\n")
                    self.control_box.appendPlainText("\n#Error = " + str(e))
                    self.control_box.appendPlainText("\n"+"#"*int(self.control_box.width()/15))
                    self.control_box.appendPlainText(dr.dict2str(self.plot_params))
            except KeyError as e:
                self.control_box.setPlainText("#Sorry I can't find any data named '"+str(e)+"'.\n\n#The full list of data categories you can use are:")
                for i in Plottable_cols:
                    self.control_box.appendPlainText("\t#"+str(i))
                self.control_box.appendPlainText("\n"+"#"*int(self.control_box.width()/15))
                self.control_box.appendPlainText(dr.dict2str(self.plot_params))
        else:
            self.control_box.setPlainText("# You at least need the Ydata Parameter, like below:")
            self.control_box.appendPlainText("YData: Balance;\nAct_N:1;")
                    
    # Deals with the account number parameter
    def act_num_handler(self,act):
        ### If the account number parameters have been set convert them to ints
        if type(act) == list:
            act = [dr.str2int(i) for i in act] 
        ###
        act = self.not_var(act,act_nums[0]) #If they haven't been set use default settings
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
    def not_var(self,var,replace):
        try:
            if len(var) < self.length_y:
                var = var+var*(self.length_y-len(var))
                return var
        except:
            pass
        if not var:
            var = [replace]*self.length_y
        return var
            
    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_H:
                self.parent().parent().FullStack.setCurrentIndex(1)
            elif e.key() == Qt.Key_Return:
                self.Ok_Button_Click()
            
class PlotCanvas(FigureCanvas):
 
    def __init__(self,XData, YData, parent=None):
        self.parent = parent
        self.fig = self.make_figure()
        self.ax = self.fig.add_subplot(111)
        self.plot(['Date'],['Balance'],[act_nums[0]])
        
    def plot(self,Xvar, Yvar, Account_numbers, Ls='-', Color='g'):
        error = False
        self.ax.cla()
        try:
            for i in range(len(Yvar)):
                Data = dict_bank_data[Account_numbers[i]]
                XData = [Data.loc[:,Xvar[i]].apply(dr.dataPrep) for i in range(self.parent.length_y)]
                YData = [Data.loc[:,Yvar[i]].apply(dr.dataPrep) for i in range(self.parent.length_y)]
                self.whichPlot(array(XData[i]),array(YData[i]),self.ax,default_plots[Yvar[i].lower()])
        except ValueError as e:
            error = e
            print("Could Not Plot Data, Wrong Types were given")
            print("XData = \n",XData,"\nX-Type = ",type(XData[0]))
            print("YData = \n",YData,"\nY-Type = ",type(YData[0]))
        self.ax.grid(color='#b0b0b0', lw=0.5)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.tick_params(labelsize=15)
        try:        
            self.draw()
        except ValueError as e:
            error = e
        return error

    def whichPlot(self,xdata,ydata,axis,plt_prms=False):
        if plt_prms:
            Type = dict_value_get(plt_prms, 'type')
            color = dict_value_get(plt_prms, 'color')
            if Type.lower() == 'scatter':
                ls = dict_value_get(plt_prms, 'ls')
                axis.plot(xdata,ydata,color=color,ls=ls)
            elif Type.lower() == 'bar':
                edgecolor = dict_value_get(plt_prms, 'edgec')
                width = dict_value_get(plt_prms, 'width')
                axis.bar(xdata,ydata,color=color,edgecolor=edgecolor,width=width)
            else:
                return "# Plot Type, %s, Not Recognised"%str(Type)
        else:
            axis.plot(xdata,ydata,'k.')
            
    def make_figure(self):
        fig = Figure(facecolor='white')
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(self.parent)
 
        FigureCanvas.updateGeometry(self)
        fig.subplots_adjust(0.07,0.05,0.97,0.95)
        return fig

    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_H:
                self.parent().parent().parent().FullStack.setCurrentIndex(1)
    

class HelpPage(QWidget):
 
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):    
        # The graph widgets
        f = open('./Gui/html/Help_Page.html','r')
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