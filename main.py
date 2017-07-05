from Data import Data as dr

settings = dr.dict_parser("Settings/Settings.txt",'l')
if settings['demo'][0] == 'on':
    bank_statement_folder_path = 'Demo_Data/'
    paypal_paths = 'Demo_Data/'  
else:
    bank_statement_folder_path = 'Stats/'
    paypal_paths = 'Stats/' 
        
dict_DATA, Plottable_cols = dr.Data_Read(bank_statement_folder_path)


from Gui import App
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App.App()
    sys.exit(app.exec_())


