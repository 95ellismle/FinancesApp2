# Imports from PyQt 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QComboBox, QLabel, QSizePolicy, QWidget, QFrame, QStackedWidget, QTextEdit
from PyQt5.QtGui import QFont, QColor

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure

from itertools import compress
import numpy as np
import datetime as dt

# Imports from other modules
from Data import Data as dr
from Data import Type_Convert as tc
import Gui.Funcs as fncs
from Settings import StyleSheets as St
from __main__ import Plottable_cols, dict_DATA
act_nums = np.array(dr.new_act_names)
Plottable_cols = np.array(['Balance'] + [i for i in Plottable_cols  if 'ate' not in i.lower() and 'alan' not in i.lower()])

Plot_Mesg = """# This is how to control the plotting.\n
# Set the data displayed on the x or the y-axis via the XData and YData commands respectively.\n 
# For Help simply type press Cntrl-H (you may need to click this textbox).
\nYData:  Balance;
"""
default_plots = {'Balance':{'color':'#7FFF00','ls':'-', 'lw':1.5}, 'In':{'color':'#00ff5a', 'ls':'none', 'lw':2, 'marker':'o'}, 'Out':{'color':'#ff0000', 'ls':'none', 'lw':2, 'marker':'o'} }
    
# Just the code for contructing the main page
class App_Bit(QWidget):
    def __init__(self):
        super().__init__()
        self.bob = 'bob'
        self.FullStack = QStackedWidget(self)
        self.PlotPageStackItem = PlotPage()
        self.HelpPageStackItem = HelpPage()
        
        self.FullStack.addWidget(self.PlotPageStackItem)
        self.FullStack.addWidget(self.HelpPageStackItem)
                
        fncs.AllInOneLayout(self,self.FullStack)
        self.show()
    
    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_H:
                self.FullStack.setCurrentIndex(1)
        elif e.key():
            self.FullStack.setCurrentIndex(0)
           
            
            
           
# The code for building the page containing the graph
class PlotPage(QWidget):
 
    def __init__(self):
        super().__init__()
        self.plot_params = {}
        self.Plot_Mesg = Plot_Mesg    
        self.length_y = 1
        self.initUI()
    
    def initUI(self):    
        # The graph widgets
        self.Graph = PlotCanvas(False, False, parent=self)
        self.toolbar = NavBar(self.Graph, self)
        control_panel = ButtonPanel(self)
        
        fncs.AllInOneLayout(self, [self.Graph, control_panel], Stretches=[4,1], VH='h')
        self.show()
    
    # A function to connect the OK_Button on the bottom of the plotting page to retrieving the data and plotting it.
    def Ok_Button_Click(self):
        pass

    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_H:
                self.parent().parent().FullStack.setCurrentIndex(1)
            elif e.key() == Qt.Key_Return:
                self.Ok_Button_Click()


class ButtonPanel(QFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.account_buttons = 'bob'
        self.plot_params_buttons = 'bob'
        self.plotting_accounts = []
        self.yparams = []
        self.graph = self.parent().Graph
        self.initUI()
                
        ### Setting the Colour of the app background
        p = self.palette()
        b_col = QColor(St.plot_background_color)
        p.setColor(self.backgroundRole(), b_col)
        self.setPalette(p) 
        self.show()
    
    def initUI(self):
        
        account_label = QLabel("Account:")
        title_font = QFont(*St.Title_Font)
        account_label.setFont(title_font)
        account_label.setStyleSheet(St.StyleSheets['QLabel'])
        
        accounts_frame = QFrame(self);
        self.account_buttons = [QPushButton(i.replace('Account',''), self) for i in act_nums]
        [i.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) for i in self.account_buttons]
        [i.setCheckable(True) for i in self.account_buttons]
        [i.setStyleSheet(St.StyleSheets['Plot Buttons Account']) for i in self.account_buttons]
        [i.clicked.connect(self.onAccountClick) for i in self.account_buttons]
        fncs.AllInOneLayout(accounts_frame, self.account_buttons, VH='h', Align=Qt.AlignTop, Stretches=[1]+[1 for i in self.account_buttons])
        
        plot_params_frame = QFrame(self)
        self.plot_params_buttons = [QPushButton(i, self) for i in Plottable_cols]
        [i.setStyleSheet(St.StyleSheets['Plot Buttons Ydata']) for i in self.plot_params_buttons]
        [i.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) for i in self.plot_params_buttons]
        [i.setCheckable(True) for i in self.plot_params_buttons]
        [i.clicked.connect(self.onPlotParameterClick) for i in self.plot_params_buttons]
        fncs.AllInOneLayout(plot_params_frame, self.plot_params_buttons, VH='h', Align=Qt.AlignTop)
        
        ydata_label = QLabel("YData:")
        ydata_label.setFont(title_font)
        ydata_label.setStyleSheet(St.StyleSheets['QLabel'])
       
        groupby_frame = QFrame(self)
        groupby_label = QLabel("Resample:")
        groupby_label.setFont(title_font)
        groupby_combo_box = QComboBox(self)
        [groupby_combo_box.addItem(i) for i in ['None', 'Daily', 'Weekly', 'Monthly', 'Yearly']]
        groupby_combo_box.setStyleSheet(St.StyleSheets['Combo Box'])
        groupby_combo_box.activated[str].connect(self.onComboBox)
        
        fncs.AllInOneLayout(groupby_frame, [groupby_label, groupby_combo_box], VH='h')
        
        spacer = QLabel("")

        fncs.AllInOneLayout(self, [account_label, accounts_frame, ydata_label, plot_params_frame, spacer, groupby_frame, spacer], VH='V', Align=Qt.AlignTop, Stretches=[1,1,1,1,0.2,1,10])
    
    def onAccountClick(self):
        fil = [i.isChecked() for i in self.account_buttons]
        self.plotting_accounts = list(compress(act_nums,fil))
        self.graph.plotting(self.plotting_accounts, self.yparams)
        
    def onPlotParameterClick(self):
        fil = [i.isChecked() for i in self.plot_params_buttons]
        self.yparams = list(compress(Plottable_cols, fil))
        self.graph.plotting(self.plotting_accounts, self.yparams)
        
    def onComboBox(self, text):
        self.graph.resample_rate = text
        self.graph.plotting(self.plotting_accounts, self.yparams)

# The code that holds the plotting figure and does all the plotting.    
class PlotCanvas(FigureCanvas):
 
    def __init__(self, Accounts, YParams, parent=None):
        self.parent = parent
        self.fig = self.make_figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.resample_rate = 'None'
        self.plotting(Accounts, YParams)
        
    def plotting(self, Accounts, YParams):
        self.axis_prep()
        if Accounts and YParams:
            for acc in Accounts:
                data = dict_DATA[acc].ix[:, list(Plottable_cols)+['Date']]
                data.index = data['Date']
                for col in Plottable_cols:
                    data[col] = data[col].apply(tc.dataPrep)
                for yparam in YParams:
                    col, ls, lw, marker =self.whichPlot(yparam, Accounts, acc)
                    ydat = self.resample(data, yparam)
                    self.ax.grid('on')
                    #self.get_mid_coords(ydat.index, ydat)
                    self.ax.plot(ydat, color=col, ls=ls, lw=lw, marker=marker)
        self.draw()
        
    def axis_prep(self):
        self.ax.cla()
        self.fig.subplots_adjust(left=0.08,right=0.97,
                            bottom=0.08,top=0.97,
                            hspace=0.2,wspace=0.2)
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Money / £')
        
    def whichPlot(self, YParams, Accounts, acc):
        col = dr.dict_value_get(default_plots[YParams],'color')
        col =  fncs.colorChange(col, 1-0.2*Accounts.index(acc), [0,1,2], Type='scale', output='hex')
        ls = dr.dict_value_get(default_plots[YParams],'ls')
        lw = dr.dict_value_get(default_plots[YParams],'lw')+Accounts.index(acc)*0.25
        marker = dr.dict_value_get(default_plots[YParams],'marker')
        return col,ls,lw, marker
    
    def get_mid_coords(self, xdata, ydata):
        xdata.index = range(len(xdata))
        ydata.index = range(len(ydata))
        max_index = ydata.idxmax()
        xmid, ymid1 = xdata[max_index], ydata.loc[max_index]
        return (xmid, ymid1), (xmid+dt.timedelta(24), ymid1+150)
    
    def draw_on_plot(self, axes, coords, annotation, yparam):
        if yparam.lower() == 'balance':
            axes.annotate(annotation, xy=coords[0], xytext = coords[1], 
                          arrowprops=dict(arrowstyle='->', color='red'), fontsize=16)
    
    def resample_rate_translate(self):
        if self.resample_rate == 'Weekly':
            self.resample_rate = 'W'
        elif self.resample_rate == 'Monthly':
            self.resample_rate = 'M'
        elif self.resample_rate == 'Daily':
            self.resample_rate = 'D'
        elif self.resample_rate == 'Yearly':
            self.resample_rate = dt.timedelta(365.25)
        
                    
    
    def resample(self, data, yparam):
        self.resample_rate_translate()
        if self.resample_rate == 'None':
            return data[yparam].astype(float)
        if yparam == 'Balance':
            data = data.groupby(data.index).max()[yparam]
            data = data.resample(self.resample_rate).max()
        elif yparam == 'In' or yparam == 'Out':
            data = data.groupby(data.index).sum()[yparam]
            data = data.resample(self.resample_rate).sum()
        data = data.dropna()
        return data
    
    def make_figure(self):
        fig = Figure(facecolor='white')
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(self.parent)
 
        FigureCanvas.updateGeometry(self)
        fig.subplots_adjust(0.07,0.05,0.97,0.95)
        return fig

    # Binds Cntrl+H to the switching to the help page
    def keyPressEvent(self, e):
        if e.modifiers() == Qt.ControlModifier:
            if e.key() == Qt.Key_H:
                self.parent().parent().parent().FullStack.setCurrentIndex(1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# The help page (simply displays some HTML)
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
                
        fncs.AllInOneLayout(self,self.Help_Box)
    
    # Binds Cntrl+Enter to the Ok_Button
    def keyPressEvent(self, e):
        if e.key():
            self.parent().parent().FullStack.setCurrentIndex(0)
            
            
    
'''
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
fncs.AllInOneLayout(text_frame, [self.control_box, OK_Button],Stretches=[10,1], Align=Qt.AlignRight)

fncs.AllInOneLayout(self,[self.Graph, text_frame], Stretches=[4,1], VH='H')
'''