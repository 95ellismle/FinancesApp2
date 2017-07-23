from Data import Data as dr
from Data import Random_Data_Creator as rdc

if dr.settings['Demo'][0].lower() == 'on':
    data_create_question = input("Should I create some random data? [y/n]\t")
    rdc.create_data(data_create_question)
    
    bank_statement_folder_path = dr.demo_data
    paypal_paths = dr.demo_data  
else:
    bank_statement_folder_path = dr.bank_data_folder
    paypal_paths = dr.bank_data_folder

dict_DATA, Plottable_cols = dr.Data_Read(bank_statement_folder_path)

#print(data)

 
from Gui import App
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App.App()
    sys.exit(app.exec_())
