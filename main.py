### Standard Python Modules ####
import os              # A module for operating system operations
import pandas as pd

### Telling the code where everything is. This needs to be above the Data module import as these are used in that module.
bank_statement_folder_path = '/home/ellismle/Documents/Other/Finances-App(non git)/Stats/'
categories_filename = '/home/ellismle/Documents/Other/Finances_app2/Categories.txt'
col_head_filepath = '/home/ellismle/Documents/Other/Finances_app2/Data_Headers.txt'

### Modules included in the repo ###
from Data import Data as dr

error_messgs = [] # A list to store anything that goes wrong...

###

### Finding the Bank Statement Files and Paypal files
poss_bank_files = os.listdir(bank_statement_folder_path)
poss_bank_files = [bank_statement_folder_path + i for i in poss_bank_files if '.csv' in i]      # removing any non csv files
paypal_filepaths = [i for i in poss_bank_files if 'payp' in i]     # finding the paypal files
bank_filepaths = [i for i in poss_bank_files if 'payp' not in i]   # finding the non-paypal and therefore bank files
###

if len(bank_filepaths):
    dr.data_clean(poss_bank_files)                 # Permanently removes sensitive data from statements
    bank_data = dr.data_read(bank_filepaths)       # Reads the statement files and collates them into 1 dataframe
else:
    bank_data = dr.data_read('./')
if len(paypal_filepaths):
    paypal_data = dr.data_read(paypal_filepaths)   # Reads the paypal files and collates into 1 dataframe.

if len(bank_filepaths):
    names = dr.dict_parser(col_head_filepath)

    ### Changing the names of the statement columns
    cols = bank_data.columns
    new_cols = dr.dict_value_search(list(cols),names)
    bank_data.columns = new_cols
    ###

### Converting the type from string to something more useful
dr.convert_col(bank_data,'Date','date',error_messgs)
dr.convert_col(bank_data,'Balance',float,error_messgs)
dr.convert_col(bank_data,'In',float,error_messgs)
dr.convert_col(bank_data,'Out',float,error_messgs)
dr.convert_col(bank_data,'Acc Num',int,error_messgs)
###

if len(bank_filepaths):
    ### Sorting data from different bank accounts
    bank_data = bank_data.sort_values('Date',0)
    bank_data['Description'] = bank_data['Description'].apply(dr.up)
    bank_data = bank_data.fillna('')
    bank_data['Description'] = bank_data['Description'].apply(dr.unclutter)
    act_nums = list(set(list(bank_data['Acc Num']))) # Finding the unique account numbers
    dict_bank_data = {i:bank_data.loc[bank_data['Acc Num'] == i] for i in act_nums} # Storing each account as a separate dictionary entry
    for i in dict_bank_data: # Deleting the account numbers in the dataframes
        dict_bank_data[i] = dict_bank_data[i].drop([col for col in bank_data.columns if 'Acc' in col], axis=1)
    ###
    cols_ordered = ['Description','Category','In','Out','Date','Balance','Type']
    Plottable_cols = []
    for i in dict_bank_data:
        dict_bank_data[i] = dict_bank_data[i].drop_duplicates()
        dict_bank_data[i].loc[:,'Category'] = dict_bank_data[i].loc[:,'Type'].apply(str)+';'+ dict_bank_data[i].loc[:,'Description'].apply(str)+';'+dict_bank_data[i].loc[:,'Balance'].apply(str)+';'+dict_bank_data[i].loc[:,'In'].apply(str)+';'+dict_bank_data[i].loc[:,'Out'].apply(str)+';'+ dict_bank_data[i].loc[:,'Date'].apply(str)
        dict_bank_data[i].loc[:,'Category'] = dict_bank_data[i].loc[:,'Category'].apply(dr.categoriser)
        dict_bank_data[i] = dict_bank_data[i].sort_values(by='Date', ascending=False)
        dict_bank_data[i] = dict_bank_data[i][cols_ordered] # Re-Ordering the Columns
        dict_bank_data[i]['Description'] = dict_bank_data[i]['Description'].apply(dr.capital)
        dict_bank_data[i].index = range(len(dict_bank_data[i])) # Resorting the index

    
    for col in dict_bank_data[act_nums[0]].columns:
        if dict_bank_data[act_nums[0]][col].apply(dr.dataPrep).dtype != object:
            Plottable_cols.append(col)

   

from Gui import App
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App.App()
    sys.exit(app.exec_())
