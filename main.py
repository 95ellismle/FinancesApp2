### Standard Python Modules ####
import pandas as pd    # A module to carry out data analysis
import os              # A module for operating system operations

### Modules included in the repo ###
from Data import data_read as dr 



bank_statement_folder_path = '/home/ellismle/Documents/Other/Finances-App(non git)/Stats/'
poss_bank_files = os.listdir(bank_statement_folder_path)
poss_bank_files = [bank_statement_folder_path + i for i in poss_bank_files if '.csv' in i]      # removing any non csv files
paypal_filepaths = [i for i in poss_bank_files if 'payp' in i]     # finding the paypal files
bank_filepaths = [i for i in poss_bank_files if 'payp' not in i]   # finding the non-paypal and therefore bank files


dr.data_clean(poss_bank_files)                 # Permanently removes sensitive data from statements
bank_data = dr.data_read(bank_filepaths)       # Reads the statement files and collates them into 1 dataframe
paypal_data = dr.data_read(paypal_filepaths)   # Reads the paypal files and collates into 1 dataframe.

names = {'Acc Num':['account number'], 
         'Balance':['balance'], 
         'Incomings':['in','credit'], 
         'Outgoings':['out','debit'], 
         'Date':['date'],
         'Description':['descr','name'],
         'Type-Code':['type','code']}






for i in names:
    for j in range(len(names[i])):
        names[i][j] = names[i][j].lower()

cols = bank_data.columns
    
for col_i in range(len(cols)):
    for tupl in names.items():
        
        