# Other people's modules
from PyQt5.QtWidgets import  QMainWindow

# Own Modules
from Gui import Table as t



class App(QMainWindow):
    def __init__(self,data):
        QMainWindow.__init__(self)
        
        self.initUI()
        self.create_table(data)
    
    def initUI(self):
        self.resize(500,500)
        self.show()

    def create_table(self, data):
        t.Table(data)
