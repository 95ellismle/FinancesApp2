from PyQt5.QtWidgets import QLabel, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from Gui import Funcs as fncs


class SettingsPage(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        l1 = QLabel("Peek-A-Boo!")
        font = QFont("Comic Sans", 25)
        l1.setFont(font)
        fncs.AllInOneLayout(self,[l1],Align=Qt.AlignCenter)
        self.show()
