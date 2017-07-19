#!/usr/bin/python3

import pandas as pd
import os
import string as osl
import datetime as dt

from Data import Type_Convert as tc
from Data import Strings as st
from Settings import StyleSheets as Ss

pd.options.mode.chained_assignment = None  # default='warn'
### Telling the code where everything is. This needs to be above the Data module import as these are used in that module.
categories_filename = '/home/ellismle/Documents/Other/Finances_app2/Settings/Categories.txt'
col_head_filepath = '/home/ellismle/Documents/Other/Finances_app2/Settings/Data_Headers.txt'


#error_messgs = [] # A list to store anything that goes wrong...

###


#Will splice data between 2 given dates.
def DateSplice(data, date1, date2):
    data = data.loc[data['Date'] < date2]
    data = data.loc[data['Date'] > date1]
    return data

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
    
# Searches for old keys and if it finds them changes them to new_keys
def dict_key_change(dictionary, old_keys, new_keys):
    for i in range(len(old_keys)):
        try:
            ydata_key = dict_key_get(dictionary, old_keys[i])
            dictionary[new_keys[i]] = dictionary.pop(ydata_key)
        except KeyError:
            pass
    return {i:dictionary[i] for i in dictionary if i in new_keys}

# Just tries to get the values associated with a dictionary, if the key isn't there it silently ignores it and returns None
def dict_value_get(dictionary, key1, acceptable_values=False):
    key = dict_key_get(dictionary, key1)
    try:
        value = dictionary[key]
        value = multi_list_check(value, acceptable_values)
        return value
    except (IndexError, KeyError):
        return None

# Finds a key close to the one asked for
def dict_key_get(dictionary, search):
        try:
            key = [i for i in dictionary.keys() if search.lower() in i.lower()][0]
            return key
        except:
            None
            
# Checks if a substring is in a list of strings and if it is returns the list item
def list_check(search_item, LIST):
    for list_item in LIST:
        if list_item.lower() in search_item.lower() or search_item.lower() in list_item.lower():
            return (True,list_item)
    return False

# Returns any items in list1 that are substrings of items in list2
def multi_list_check(list1, list2):
    if type(list1) == list and type(list2) == list:
        new_list1 = []
        for i in list1:
            val = list_check(i, list2)
            if val:
                new_list1.append(val[1])
        return new_list1
    else:
        return list1

# Fills a smaller list with a value specified by the filler
def list_fill(small_list, large_list, Type=1, filler='Account '):
         lenS, lenL = len(small_list), len(large_list)
         for i in range(lenS, lenL):
             if Type == 0:
                small_list.append(filler)
             if Type == 1:
                 small_list.append(str(i+1))
             if Type == 2:
                 small_list.append(small_list[int(i%lenS)])
             if Type == 3:
                 small_list.append(filler+str(i+1))
         return small_list         
        
# Checks to see whether a search parameter (value) is in the dictionary's values. Works for strings, numbers and lists.
def dict_value_search(dictionary, value):
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
def dict_parser(filepath, LUC='c'):
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
        if LUC.lower() == 'u':
                    CATS = {i.split(':')[0]:[j for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.

    else:
        CATS = {i.split(':')[0]:[j for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
    ###
    return CATS

settings = dict_parser("Settings/Settings.txt",'u')
cats = dict_parser(categories_filename)
new_act_names = dict_value_get(settings, 'accountname')
bank_data_folder = dict_value_get(settings, 'statementfolderloc')[0]
demo_data = dict_value_get(settings, 'demodatafolder')[0]

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

# Reads a group of data files and groups them into 1 dataframe.
def data_read_and_concat(filepaths):
    if type(filepaths) == list:
        data = pd.concat([pd.read_csv(file) for file in filepaths]) #Concatenating the account data frames together.
    if type(filepaths) == str:
        files = [i for i in os.listdir(filepaths) if '.csv' in i]
        data = {int(i[:i.find('.csv')]):pd.read_csv('./'+i) for i in files}
    return data

def find_paypal_files(folderpath):
    ### Finding the Bank Statement Files and Paypal files
    poss_datafiles = os.listdir(folderpath)
    poss_datafiles = [folderpath + i for i in poss_datafiles if '.csv' in i]      # removing any non csv files
    datafilepaths = [i for i in poss_datafiles if 'payp' in i]   # finding the non-paypal and therefore bank files
    ###
    return datafilepaths

def paypal_data_read(folder):
    paypal_filepaths = find_paypal_files(folder)
    if len(paypal_filepaths):
        paypal_data = data_read_and_concat(paypal_filepaths)   # Reads the paypal files and collates into 1 dataframe.
        paypal_data['Date'] = pd.to_datetime(paypal_data['Date'], format=Ss.date_format)
        paypal_data = paypal_data.sort_values(by='Date', ascending=False)
        for col in paypal_data.columns:
            if any(j.lower() in col.lower() for j in ['receip', 'stat', 'rrency', 'time']):
                paypal_data = paypal_data.drop(col, axis=1)
        paypal_data[' Amount'] = paypal_data[' Amount'].apply(str)
        return paypal_data
    else:
        return None

paypal_data = paypal_data_read(bank_data_folder)

def dataframe_date_splice(data, date1, date2):
    data = data.loc[data['Date'] > date1]
    data = data.loc[data['Date'] < date2]
    return data


def find_files(folderpath):
    ### Finding the Bank Statement Files and Paypal files
    poss_datafiles = os.listdir(folderpath)
    poss_datafiles = [folderpath + i for i in poss_datafiles if '.csv' in i]      # removing any non csv files
    datafilepaths = [i for i in poss_datafiles if 'payp' not in i]   # finding the non-paypal and therefore bank files
    ###
    return datafilepaths

# Converts 1 large dataframe containing data from multiple accounts to a dictionary of dataframes with each key only containing 1 account's data.
def Initial_Prep(dataframe):
    dataframe = dataframe.drop_duplicates()
    dataframe = dataframe.fillna('')
    dataframe.loc[:,'Description'] = dataframe.loc[:,'Description'].apply(st.unclutter)
    dataframe = dataframe.sort_values('Date', 0, ascending=False)
    ### Sorting data from different bank accounts
    act_nums = dataframe.loc[:,'Acc Num'].unique() # Finding the account numbers
    global new_act_names 
    new_act_names = new_act_names[:len(act_nums)]
    list_fill(new_act_names, act_nums, Type=3)
    dict_DATA = {new_act_names[i]:dataframe.loc[dataframe['Acc Num'] == act_nums[i]] for i in range(len(act_nums))} # Storing each account as a separate dictionary entry
    for i in dict_DATA: # Deleting the account numbers in the dataframes
        dict_DATA[i] = dict_DATA[i].drop([col for col in dataframe.columns if 'Acc' in col], axis=1)
    return dict_DATA, new_act_names

def paypal_cross_ref(item, days_before):
    item = item.lower()
    Desc, Bal, In, Out, Date = item.split(';')
    Out = tc.str2float(Out)
    if 'payp' in Desc:
        date1 = tc.str2date(Date) - dt.timedelta(days_before)
        date2 = tc.str2date(Date) + dt.timedelta(1)
        possible_paypal_data = dataframe_date_splice(paypal_data, date1, date2)
        possible_paypal_data[' Amount'] = possible_paypal_data[' Amount'].apply(tc.str2float)
        if Out:
            possible_paypal_item = possible_paypal_data.loc[possible_paypal_data[' Amount'] == -tc.str2float(Out)]
            unique_entries = possible_paypal_item[' Name'].unique()
            if len(unique_entries) > 1:
                unique_entries = [i for i in unique_entries if all(j not in i.lower() for j in ['payp', 'credit card']) ]
                if len(unique_entries) > 1:
                    print("\n\nDescription = ", Desc, 
                          "\nDate = ", Date,
                          "\nIn = ", In,
                          "\nOut = ", Out, 
                          "\nPossible Paypal Item:\n", unique_entries)
                else:
                    if len(unique_entries):
                        return unique_entries[0] + ' (payp)'
            else:
                if len(unique_entries):
                    return unique_entries[0] + ' (payp)'
                else:
                    new_poss_paypal_item = possible_paypal_data.loc[possible_paypal_data[' Amount'] == Out]
                    if len(new_poss_paypal_item):
                        if new_poss_paypal_item[' Name'].values[0].replace(' ','').lower() == 'bankaccount':
                            balance = tc.str2float(new_poss_paypal_item[' Balance'].values[0])
                            possible_paypal_data[' Amount'] = possible_paypal_data[' Amount'].apply(tc.str2float)
                            possible_items = possible_paypal_data.loc[possible_paypal_data[' Amount'] == -balance][' Name'].unique()
                            if len(possible_items) == 1:
                                return possible_items[0]
                            else:
                                return paypal_cross_ref(item, 21)
                                print("\n\nDescription = ", Desc, 
                                      "\nDate = ", Date,
                                      "\nIn = ", In,
                                      "\nOut = ", Out,
                                      "\nPossible Paypal Data:\n", possible_paypal_data)
                                return "Non"
                    return Desc
        else:
            return "Paypal Transfer"
    else:
        return Desc

        

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
    elif Type == 'tfr' or 'transfer' in Desc:
        return 'Transfer'
    elif Type == 'dep':
        return 'Bank Deposit'
    if 'interest' in Desc:
        return 'Interest'
    if Desc == 'tan':
        return 'Salary'

    cat = dict_value_search(cats, Desc)

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

# Reads the data
def Data_Read(filepath, paypal=False):
    if os.path.isdir(filepath):
        if paypal == False:
            datafilepaths = find_files(filepath)
        else:
            datafilepaths = find_paypal_files(filepath)
        data_clean(datafilepaths)                 # Permanently removes sensitive/useless data from bank statements
        DATA = data_read_and_concat(datafilepaths)       # Reads the statement files and collates them into 1 dataframe
    else:
        DATA = data_read_and_concat('./')
        
    if len(DATA):
        names = dict_parser(col_head_filepath) #Grabbing the data headers
    
        ### Changing the names of the statement columns
        cols = DATA.columns
        new_cols = dict_value_search(names, list(cols))
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
            for col in ['Balance','In','Out','Date']:
                dict_DATA[i]['Description'] = dict_DATA[i]['Description'] + ';' + dict_DATA[i][col].apply(tc.string)
            dict_DATA[i]['Description'] = dict_DATA[i]['Description'].apply(paypal_cross_ref, args=(7,))        
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