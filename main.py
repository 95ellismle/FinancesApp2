from Data import Data as dr


bank_statement_folder_path = '/home/ellismle/Documents/Other/Finances-App(non git)/Stats/'
paypal_paths = '/home/ellismle/Documents/Other/Finances-App(non git)/Stats/'
dict_DATA, Plottable_cols = dr.Data_Read(bank_statement_folder_path)
 


from Gui import App
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App.App()
    sys.exit(app.exec_())
