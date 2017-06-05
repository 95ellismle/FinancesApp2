### Standard Python Modules ####
import os              # A module for operating system operations
import pandas as pd

### Modules included in the repo ###
cats = {}
from Data import Data as dr

error_messgs = [] # A list to store anything that goes wrong...

# Removes any comments (Those with a hash) from some text
def comment_remove(string):
    hash_ind = string.find('#')
    if hash_ind != -1:
        carriage_ind = string[hash_ind:].find('\n') + 1
        string = string[carriage_ind:]
        return comment_remove(string)
    else:
        return string

# Parses the dictionary data from a txt file into a dictionary
def cat_parser(filepath):
    ### Reading the file containing info on categorising the data
    categories_file = open(filepath,'r')
    categories_txt = comment_remove(categories_file.read())
    categories_file.close()
    # Parsing the category file data.
    x = [i.replace('\n','').replace(' ','').replace('\_',' ') for i in categories_txt.split(';')]
    cats = {i.split(':\t')[0]:[j.upper() for j in filter(None,i.split(':\t')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
    ###
    return cats

### Telling the code where everything is
bank_statement_folder_path = '/home/ellismle/Documents/Other/Finances-App(non git)/Stats/'
categories_filename = '/home/ellismle/Documents/Other/Finances_app2/Categories.txt'
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
    names = {'Acc Num':['account number'], 
             'Balance':['balance'], 
             'In':['in','credit'], 
             'Out':['out','debit'], 
             'Date':['date'],
             'Description':['descr','name'],
             'Type':['type','code'],
             'Time':['tim']}
    
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

cats = cat_parser(categories_filename) # Parsing the categories information into a dictionary named cats

if len(bank_filepaths):
    ### Sorting data from different bank accounts
    bank_data = bank_data.sort_values('Date',0)
    bank_data['Description'] = bank_data['Description'].apply(dr.up)
    act_nums = set(list(bank_data['Acc Num'])) # Finding the unique account numbers
    dict_bank_data = {i:bank_data.loc[bank_data['Acc Num'] == i] for i in act_nums}
    ###


    for i in dict_bank_data:
        dict_bank_data[i].index = range(len(dict_bank_data[i]))
        dict_bank_data[i]['Categories'] = dict_bank_data[i]['Type'].apply(str)+';'+ dict_bank_data[i]['Description'].apply(str)+';'+dict_bank_data[i]['Acc Num'].apply(str)+';'+dict_bank_data[i]['Balance'].apply(str)+';'+dict_bank_data[i]['In'].apply(str)+';'+dict_bank_data[i]['Out'].apply(str)+';'+ dict_bank_data[i]['Date'].apply(str)
        dict_bank_data[i]['Categories'] = dict_bank_data[i]['Categories'].apply(dr.categoriser)
    #dr.save(dict_bank_data,'./')




