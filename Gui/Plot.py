# Imports from PyQt 
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

# Matplotlib imports
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Other Imports
import pandas as pd
 
# Imports from other modules
from __main__ import dict_bank_data
 
class PlotPage(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
 
        plot = PlotCanvas(XData=[1],YData=[1],parent=self)

        self.AllInOneLayout(self,[plot])
        
        self.show()

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
 
class PlotCanvas(FigureCanvas):
 
    def __init__(self,XData, YData, parent=None):
        fig = Figure(facecolor='white')
        self.axes = fig.add_subplot(111)
 
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.updateGeometry(self)
        Data = dict_bank_data[27274868]
        Data['Date'] = pd.to_datetime(Data['Date'])
        Data = Data.groupby('Date').first()
        Xdata,Ydata = [Data.index,Data['Balance']]
        self.plot(Xdata,Ydata)
 
 
    def plot(self,Xdata,Ydata):
        ax = self.figure.add_subplot(111)
        ax.plot(Xdata,Ydata, 'g-')
        self.draw()
    
