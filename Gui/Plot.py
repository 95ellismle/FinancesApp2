# Imports from PyQt 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSizePolicy, QWidget, QPlainTextEdit, QFrame, QPushButton
from PyQt5.QtGui import QFont

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavBar
from matplotlib.figure import Figure
 
# Imports from other modules
from __main__ import dict_bank_data
from Data import Data as dr
from Gui.Funcs import AllInOneLayout
from Gui import StyleSheets as St

Plot_Mesg = """# This is how to control the plotting.\n
# Set the data displayed on the x or the y-axis via the XData and YData commands respectively.\n 
# A full rundown of the commands will be provided in the README.md file.\n
# Feel free to delete all these comments (marked with a hash).
\nYData:  Balance, Out;
XData: default;"""

class PlotPage(QWidget):
 
    def __init__(self):
        super().__init__()
        self.plot_params = {}
        self.Plot_Mesg = Plot_Mesg
        self.initUI()
    
    def initUI(self):       
        plot = PlotCanvas(XData=[1],YData=[1],parent=self)
        self.toolbar = NavBar(plot, self)
        text_frame = QFrame()
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
        
        AllInOneLayout(self,[plot, text_frame], Stretches=[4,1], VH='H')
        
        self.show()

    def Ok_Button_Click(self):
        self.plot_params = dr.dict_parser(self.control_box.toPlainText())
        self.Plot_Mesg = dr.dict2str(self.plot_params)
        self.control_box.setPlainText(self.Plot_Mesg)
        
class PlotCanvas(FigureCanvas):
 
    def __init__(self,XData, YData, parent=None):
        fig = Figure(facecolor='white')
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.updateGeometry(self)
        Data = dict_bank_data[27274868]
        dr.convert_col(Data,'Date','Date')
        Data = Data.groupby('Date').last()
        Xdata,Ydata = [Data.index,Data['Balance']]
        self.plot(Xdata,Ydata)
        fig.subplots_adjust(0.07,0.05,0.97,0.95)
 
    def plot(self,Xdata,Ydata):
        ax = self.figure.add_subplot(111)
        ax.plot(Xdata,Ydata, 'g-')
        ax.grid(color='#b0b0b0', lw=0.5)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(labelsize=15)        
        self.draw()
    
