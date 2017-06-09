# PyQt related imports
from PyQt5.QtCore import QAbstractTableModel, Qt

from numpy import shape

# This is some code taken from https://stackoverflow.com/questions/31475965/fastest-way-to-populate-qtableview-from-pandas-data-frame
# I found the tableWidget was flagging in terms of performance for even smallish datasets (1,000+).
# This QAbstractTableModel seems to perform much better when populating a tableView with a pandas dataframe.

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data.values            # Returns a set of numpy arrays where each array contains a row from the dataframe in order.
        self._cols = data.columns           # Gets the dataframe columns
        self.r, self.c = shape(self._data)  # Finds the dimensions of the dataframe
     
    # rowCount, columnCount and data are all necessary functions to call when using the QAbstractTableModel.
    def rowCount(self, parent=None): 
        return self.r
    
    def columnCount(self, parent=None):
        return self.c

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return self._data[index.row(),index.column()]
        return None

    # Well behaved models also implement headerData (taken from http://pyqt.sourceforge.net/Docs/PyQt4/qabstracttablemodel.html)
    def headerData(self, p_int, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._cols[p_int])
            elif orientation == Qt.Vertical:
                return p_int
        return None