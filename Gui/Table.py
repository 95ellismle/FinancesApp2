# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt

from numpy import shape, array

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = array(data.values)
        self._cols = data.columns
        self.r, self.c = shape(self._data)
        
    def rowCount(self, parent=None):
        return self.r

    def columnCount(self, parent=None):
        return self.c

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return self._data[index.row(),index.column()]
        return None


    def headerData(self, p_int, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._cols[p_int]
            elif orientation == Qt.Vertical:
                return p_int
        return None