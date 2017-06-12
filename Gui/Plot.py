# Imports from PyQt 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QWidget, QPlainTextEdit, QFrame, QPushButton
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
from __main__ import dict_bank_data
from Data import Data as dr
from Gui.Funcs import AllInOneLayout
from Gui import StyleSheets as St

Plot_Mesg = """# This is how to control the plotting.\n
# Set the data displayed on the x or the y-axis via the XData and YData commands respectively.\n 
# A full rundown of the commands will be provided in the README.md file.\n
# Feel free to delete all these comments (marked with a hash).
\nYData:  Balance;
XData: Date;"""

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
        self.plot_params = dr.dict_parser(self.control_box.toPlainText())
        self.Plot_Mesg = dr.dict2str(self.plot_params)
        self.control_box.setPlainText(self.Plot_Mesg)
        self.data_plot(self.plot_params)
    
    # Controls what gets plotted according to the control_box
    def data_plot(self, plt_prms):
        if 'Ydata' in plt_prms.keys() and 'Xdata' in plt_prms.keys():
            x = plt_prms['Xdata']
            y = plt_prms['Ydata']
            Data = dict_bank_data[27274868]
            XData = Data[x[0]]
            YData = Data[y[0]].apply(dr.str2float)
            self.Graph.plot(XData,YData)
    
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
        self.ax.cla()
        try:
            self.ax.plot(array(Xdata),array(Ydata), 'g.')
        except ValueError as e:
            print("Could Not Plot Data, Wrong Types were given")
            print("XData = \n",Xdata,"\nX-Type = ",type(Xdata[0]))
            print("YData = \n",Ydata,"\nY-Type = ",type(Ydata[0]))
        self.ax.grid(color='#b0b0b0', lw=0.5)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.tick_params(labelsize=15)        
        self.draw()

    
    def make_figure(self):
        fig = Figure(facecolor='white')
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(self.parent)
 
        FigureCanvas.updateGeometry(self)
        fig.subplots_adjust(0.07,0.05,0.97,0.95)
        return fig
    

    
