from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class SettingsPage(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        l1 = QLabel("Peek-A-Boo!")
        font = QFont("Comic Sans", 25)
        l1.setFont(font)
        self.AllInOneLayout(self,[l1],Align=Qt.AlignCenter)
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
