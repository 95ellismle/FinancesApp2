from Data import Data as dr

bank_data_folder = dr.dict_value_get(dr.settings, 'statementfolderloc')[0]
demo_data = dr.dict_value_get(dr.settings, 'demodatafolder')[0]
from Data import Random_Data_Creator


def create_data(data_create_question):
    if 'y' in data_create_question.lower():
        num_accs = input("How many account's worth should I make?\t")
        Random_Data_Creator.make_data(num_accs)
        return 0
    elif 'n' in data_create_question.lower():
        print("OK, I'll just try and load the data that is already there.\n")
        return 0
    else:
        create_data(input("Sorry please type yes or no...\t"))

if dr.settings['Demo'][0].lower() == 'on':
    data_create_question = input("Should I create some random data? [y/n]\t")
    create_data(data_create_question)
    
    bank_statement_folder_path = demo_data
    paypal_paths = demo_data  
else:
    bank_statement_folder_path = bank_data_folder
    paypal_paths = bank_data_folder
        
dict_DATA, Plottable_cols = dr.Data_Read(bank_statement_folder_path)



from Gui import App
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App.App()
    sys.exit(app.exec_())
    
    
