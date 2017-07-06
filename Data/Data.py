#!/usr/bin/python3

import pandas as pd
import os
import string as osl

from Data import Type_Convert as tc
from Data import Strings as st

### Telling the code where everything is. This needs to be above the Data module import as these are used in that module.
categories_filename = '/home/ellismle/Documents/Other/Finances_app2/Settings/Categories.txt'
col_head_filepath = '/home/ellismle/Documents/Other/Finances_app2/Settings/Data_Headers.txt'


#error_messgs = [] # A list to store anything that goes wrong...

###

  

# Permanently removes the Sort-Code in the bank account data because it is not needed.
def data_clean(filepaths):
    if type(filepaths) != list: # the filepaths must be given in a list
        filepaths = [filepaths]    
    for file in filepaths:
        try:
            data = pd.read_csv(file,sep=',') #reads the data for each file
            for col_name in data.columns:
                col_name_up = col_name.upper()
                if 'INDEX' in col_name_up or 'UNNAMED' in col_name_up or 'SORT' in col_name_up or ' ' == col_name: # checks to see if some unwanted column headers are there
                    data = data.drop(col_name,1)
    
            data.to_csv(file,sep=',',index = None)#Saving the data without the sort code
        except UnicodeDecodeError as e:
            print("I couldn't read the files. They seem to be stored in the wrong format.\nPlease check that the statement data is in csv format.\n")
            print("Rogue file = ",file,"\nError = ",e)
    
 
    
# Checks if a substring is in a list of strings and if it is returns the list item
def list_check(search_item, LIST):
    for list_item in LIST:
        if list_item.lower() in search_item.lower() or search_item.lower() in list_item.lower():
            return (True,list_item)
    return False

          
        
# Checks to see whether a search parameter (value) is in the dictionary's values. Works for strings, numbers and lists.
def dict_value_search(value,dictionary):
    if type(value) == list or type(value) == set:
        new_vals = [i for i in value]
        for value_index in range(len(value)):
            for dict_values in dictionary.items():
                if list_check(value[value_index],dict_values[1]):
                    new_vals[value_index] = dict_values[0] 
                    break
        return new_vals
    
    elif type(value) == int or type(value) == float:
        value = str(value)
    
    elif type(value) == str:
        for dict_values in dictionary.items():
            if list_check(value,dict_values[1]):
                    return dict_values[0]
    else:
        return None


# Saves the data to a specified location.
def save(data,filepath):
    if type(data) == dict:
        for i in data:
            data[i].to_csv(filepath+str(i)+".csv")
    
    elif type(data) == pd.core.frame.DataFrame:
        data.to_csv(filepath)


# Parses the dictionary data from a txt file into a dictionary.
# filepath is the filepath of the text file or can be a string that needs parsing. LUC refers to whether the text should be lower or uppercase or capitilised first word.
def dict_parser(filepath,LUC='c'):
    try:
        ### Reading the file containing info on categorising the data
        categories_file = open(filepath,'r')
        categories_txt = st.comment_remove(categories_file.read())
        categories_file.close()
    except OSError:
        categories_txt = filepath
    last_sc = categories_txt.rfind(';')
    if last_sc == -1:
        last_sc = None
    categories_txt = st.comment_remove(categories_txt[:last_sc])
    # Parsing the category file data
    x = [i.replace('\n','').replace('\t','').replace(' ','').replace('\_',' ') for i in categories_txt.split(';')]
    x = [i for i in x if i] # Removes any empty strings and the like...
    if LUC:
        if LUC.lower() == 'l':
            CATS = {i.lower().split(':')[0]:[j.lower() for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
        if LUC.lower() == 'u':
                    CATS = {i.upper().split(':')[0]:[j.upper() for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
        if LUC.lower() == 'c':
                    CATS = {osl.capwords(i).split(':')[0]:[osl.capwords(j) for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.

    else:
        CATS = {i.split(':')[0]:[j for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
    ###
    return CATS

settings = dict_parser("Settings/Settings.txt",'c')
cats = dict_parser(categories_filename)




# Parses the category exceptions into a list
def exceptionparser(filepath):
    try:
        f = open(filepath)
        txt = f.read()
        f.close()
    except FileNotFoundError:
        return None
    LIST = [st.comment_remove(i) for i in txt.split('\n') if st.comment_remove(i)]
    LIST = [i.split('|') for i in LIST]
    exceptions = [i[0].replace(" ","") for i in LIST]
    new_cat = [i[1] for i in LIST]
    return exceptions,new_cat
    

exceptions = exceptionparser('Settings/Exceptions.txt')
# Categorises the data
def categoriser(item):
    item = item.lower()
    if item.replace(" ","") in exceptions[0]:
        ind = exceptions[0].index(item.replace(" ",""))
        return exceptions[1][ind]
    Type, Desc, Bal, In, Out, Date = item.split(';')

    if Type == 'cpt':
        return 'Cash'
    elif Type == 'bgc':
        return 'Salary'
    elif Type == 'so':
        return 'Rent, Bills & Fines'
    elif Type == 'tfr':
        return 'Transfer'
    elif Type == 'dep':
        return 'Bank Deposit'
    if 'interest' in Desc:
        return 'Interest'
    if Desc == 'tan':
        return 'Salary'

    cat = dict_value_search(Desc,cats)

    if cat == 'Groceries':
        if list_check(Desc,cats['Car']):
            return 'Car'
        elif list_check(Desc,cats['Online Shopping']):
            return 'Online Shopping'
        else:
            return'Groceries'

    elif cat == 'High Street':
        if list_check(Desc,cats['Groceries']):
            return 'Groceries'
        elif list_check(Desc,cats['Online Shopping']):
            return 'Online Shopping'
        else:
            return 'High Street'
    
    elif cat == 'Car':
        if list_check(Desc,cats['High Street']):
            return 'High Street'       
        elif list_check(Desc,cats['Online Shopping']):
            return 'Online Shopping'
        else:
            return 'Car'
    
    elif cat == 'Bars and Pubs':
        if list_check(Desc,cats['Eating Out']):
            return 'Eating Out'
        else:
            return 'Bars and Pubs'
    else:
        return cat
    
# Fills a smaller list with a value specified by the filler
def list_fill(small_list, large_list, filler='1', Type=0):
         lenS, lenL = len(small_list), len(large_list)
         for i in range(lenS, lenL):
             if Type == 0:
                small_list.append(filler)
             if Type == 1:
                 small_list.append(i+1)
             if Type == 2:
                 small_list.append(small_list[int(i%lenS)])
         return small_list

# Reads a group of data files and groups them into 1 dataframe.
def data_read(filepaths):
    if type(filepaths) == list:
        data = pd.concat([pd.read_csv(file) for file in filepaths]) #Concatenating the account data frames together.
    if type(filepaths) == str:
        files = [i for i in os.listdir(filepaths) if '.csv' in i]
        data = {int(i[:i.find('.csv')]):pd.read_csv('./'+i) for i in files}
    return data

def Paypal_Integration(paypal_filepaths):
    if len(paypal_filepaths):
        paypal_data = data_read(paypal_filepaths)   # Reads the paypal files and collates into 1 dataframe.
        
    return paypal_data

def find_files(folderpath):
    ### Finding the Bank Statement Files and Paypal files
    poss_datafiles = os.listdir(folderpath)
    poss_datafiles = [folderpath + i for i in poss_datafiles if '.csv' in i]      # removing any non csv files
    datafilepaths = [i for i in poss_datafiles if 'payp' not in i]   # finding the non-paypal and therefore bank files
    ###
    return datafilepaths

def find_paypal_files(folderpath):
    ### Finding the Bank Statement Files and Paypal files
    poss_datafiles = os.listdir(folderpath)
    poss_datafiles = [folderpath + i for i in poss_datafiles if '.csv' in i]      # removing any non csv files
    datafilepaths = [i for i in poss_datafiles if 'payp' in i]   # finding the non-paypal and therefore bank files
    ###
    return datafilepaths

# Converts 1 large dataframe containing data from multiple accounts to a dictionary of dataframes with each key only containing 1 account's data.
def Initial_Prep(dataframe):
    dataframe = dataframe.drop_duplicates()
    dataframe['Description'] = dataframe['Description'].apply(st.up)
    dataframe = dataframe.fillna('')
    dataframe['Description'] = dataframe['Description'].apply(st.unclutter)
    dataframe = dataframe.sort_values('Date', 0, ascending=False)
    ### Sorting data from different bank accounts
    act_nums = dataframe['Acc Num'].unique() # Finding the account numbers
    new_act_names = settings['Account_names']
    list_fill(new_act_names, act_nums, Type=1)
    [new_act_names[i] for i in range(len(new_act_names))] # This piece of code for some reason stops preserves the order of the dictionary? 
    dict_DATA = {new_act_names[i]:dataframe.loc[dataframe['Acc Num'] == act_nums[i]] for i in range(len(act_nums))} # Storing each account as a separate dictionary entry
    for i in dict_DATA: # Deleting the account numbers in the dataframes
        dict_DATA[i] = dict_DATA[i].drop([col for col in dataframe.columns if 'Acc' in col], axis=1)
    return dict_DATA, new_act_names

# Reads the data
def Data_Read(filepath, paypal=False):
    if os.path.isdir(filepath):
        if paypal == False:
            datafilepaths = find_files(filepath)
        else:
            datafilepaths = find_paypal_files(filepath)
        data_clean(datafilepaths)                 # Permanently removes sensitive/useless data from bank statements
        DATA = data_read(datafilepaths)       # Reads the statement files and collates them into 1 dataframe
    else:
        DATA = data_read('./')
        
    if len(DATA):
        names = dict_parser(col_head_filepath) #Grabbing the data headers
    
        ### Changing the names of the statement columns
        cols = DATA.columns
        new_cols = dict_value_search(list(cols),names)
        DATA.columns = new_cols
        ###
    else:
        print("\n\n\nSorry there are no '.csv' files could be found in the directory '"+filepath+"'\nAre you sure this is where you want me to look?\n\n\n\n")
        raise OSError(' '.join(["No files found in ", filepath]))
        
    ### Converting the type from string to something more useful
    for i in DATA.columns:
        DATA[i] = DATA[i].apply(tc.str2num)
        if DATA[i].dtype == object:
            DATA[i] = tc.str2date(DATA[i])   
    ###
    
    if len(datafilepaths):
        dict_DATA, act_nums = Initial_Prep(DATA)
        ###
        cols_ordered = ['Description','Category','In','Out','Date','Balance','Type']
        Plottable_cols = []
        for i in dict_DATA:
            dict_DATA[i]['Category'] = dict_DATA[i]['Type']
            for col in ['Description','Balance','In','Out','Date']:
                dict_DATA[i]['Category'] = dict_DATA[i]['Category'] + ';' + dict_DATA[i][col].apply(tc.string)
            dict_DATA[i].index = range(len(dict_DATA[i])) # Resorting the index
            dict_DATA[i]['Category'] = dict_DATA[i]['Category'].apply(categoriser)
            dict_DATA[i] = dict_DATA[i].sort_values(by='Date', ascending=False)
            dict_DATA[i] = dict_DATA[i][cols_ordered] # Re-Ordering the Columns
            dict_DATA[i]['Description'] = dict_DATA[i]['Description'].apply(st.capital)
    
        
        for col in dict_DATA[act_nums[0]].columns:
            if dict_DATA[act_nums[0]][col].apply(tc.dataPrep).dtype != object:
                Plottable_cols.append(col)    
    
    return dict_DATA, Plottable_cols