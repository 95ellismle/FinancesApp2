#!/usr/bin/python3

import pandas as pd
import os
import datetime as dt
import string as string_lib

from Gui import StyleSheets as St

### Telling the code where everything is. This needs to be above the Data module import as these are used in that module.
categories_filename = '/home/ellismle/Documents/Other/Finances_app2/Settings/Categories.txt'
col_head_filepath = '/home/ellismle/Documents/Other/Finances_app2/Settings/Data_Headers.txt'


error_messgs = [] # A list to store anything that goes wrong...

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
    
    
# Returns an uppercase string
def up(x):
    if type(x) == str:
        try:
            return x.upper()
        except AttributeError:
            return x
    else:
        return x
    
    
# Checks if a substring is in a list of strings and if it is returns the list item
def list_check(search_item, LIST):
    for list_item in LIST:
        if list_item.lower() in search_item.lower() or search_item.lower() in list_item.lower():
            return (True,list_item)
    return False

# Returns a lowercase string
def lower(i):
    try:
        return i.lower()
    except (TypeError, AttributeError):
        pass
        
# Converts a datetime to a string for displaying the dataframe data
def TablePrep(item):
    try:
        return dt.datetime.strftime(item,St.date_format)
    except TypeError:
        try:
            return "%.2f"% round(item,2)
        except:
            try:
                return str(item)
            except:
                return "None"

# Converts a string to an integer if possible and if it below a certain value
def str2int(string):
    try:
        return int(string)
    except:
        return False

# converts a string to a float
def str2float(i):
    try:
        return float(i)
    except:
        return None

# Convert a string to a float and ignore exceptions
def dataPrep(i):
    try:
        return round(float(i),2)
    except ValueError:
        try:
            return pd.to_datetime(i,format=St.date_format)
        except ValueError:
            return None
    except TypeError:
        return i
    
def datetimeformat(i):
    return dt.datetime.strptime(i,St.date_format)

def str2date(col):
    try:
        return col.apply(datetimeformat)
    except:
        try:
            return pd.to_datetime(col)
        except:
            return col

def date2str(dat):
    return dt.datetime.strftime(dat,St.date_format)

        

def str2num(i):
    try:
        if float(i) == int(i):
            return int(i)
        else:
            return float(i)
    except:
        return i

            
        
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

# Removes any comments (Those with a hash) from some text
def comment_remove(string):
    x = [i for i in string.split('\n') if i]
    x = [i for i in x if i[0] != '#']
    x = [i[:i.find('#')] if i.find('#') != -1 else i for i in x ]
    string = '\n'.join(x)
    return string

# Parses the dictionary data from a txt file into a dictionary.
# filepath is the filepath of the text file or can be a string that needs parsing. LUC refers to whether the text should be lower or uppercase or capitilised first word.
def dict_parser(filepath,LUC='c'):
    try:
        ### Reading the file containing info on categorising the data
        categories_file = open(filepath,'r')
        categories_txt = comment_remove(categories_file.read())
        categories_file.close()
    except OSError:
        categories_txt = filepath
    last_sc = categories_txt.rfind(';')
    if last_sc == -1:
        last_sc = None
    categories_txt = comment_remove(categories_txt[:last_sc])
    # Parsing the category file data
    x = [i.replace('\n','').replace('\t','').replace(' ','').replace('\_',' ') for i in categories_txt.split(';')]
    x = [i for i in x if i] # Removes any empty strings and the like...
    if LUC:
        if LUC.lower() == 'l':
            CATS = {i.lower().split(':')[0]:[j.lower() for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
        if LUC.lower() == 'u':
                    CATS = {i.upper().split(':')[0]:[j.upper() for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
        if LUC.lower() == 'c':
                    CATS = {string_lib.capwords(i).split(':')[0]:[string_lib.capwords(j) for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.

    else:
        CATS = {i.split(':')[0]:[j for j in filter(None,i.split(':')[1].split(','))] for i in x} # This maybe is a bit too condensed, it uses a dictionary comphrension to loop through data in categories and extract the key names and the values. It also removes any empty strings from the lists.
    ###
    return CATS

cats = dict_parser(categories_filename)

# Returns a string from a dictionary
def dict2str(dictionary):
    string =''
    for i in dictionary:
        string += str(i) + ': ' + ', '.join(dictionary[i]) + ';\n'
    return string

# Removes Certain Strings from the Description of the Transaction to make it more readable
def unclutter(string):
    for i in ['1','2','3','4','5','6','7','8','9','0','(',')','CD']:
        string = string.replace(i,'')
    return string

# Capatilises the first letter of each string
def capital(i):
    return string_lib.capwords(i)

# Parses the category exceptions into a list
def exceptionparser(filepath):
    try:
        f = open(filepath)
        txt = f.read()
        f.close()
    except FileNotFoundError:
        return None
    LIST = [comment_remove(i) for i in txt.split('\n') if comment_remove(i)]
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

def string(i):
    return str(i).rstrip()

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
        
    if len(datafilepaths):
        names = dict_parser(col_head_filepath) #Grabbing the data headers
    
        ### Changing the names of the statement columns
        cols = DATA.columns
        new_cols = dict_value_search(list(cols),names)
        DATA.columns = new_cols
        ###
        
    ### Converting the type from string to something more useful
    for i in DATA.columns:
        DATA[i] = DATA[i].apply(str2num)
        if DATA[i].dtype == object:
            DATA[i] = str2date(DATA[i])   
    ###
    
    if len(datafilepaths):
        ### Sorting data from different bank accounts
        DATA = DATA.drop_duplicates()
        DATA['Description'] = DATA['Description'].apply(up)
        DATA = DATA.fillna('')
        DATA['Description'] = DATA['Description'].apply(unclutter)
        DATA = DATA.sort_values('Date', 0, ascending=False)
        act_nums = DATA['Acc Num'].unique() # Finding the account numbers
        dict_DATA = {i:DATA.loc[DATA['Acc Num'] == act_nums[i]] for i in range(len(act_nums))} # Storing each account as a separate dictionary entry
        act_nums = range(len(act_nums))
        for i in dict_DATA: # Deleting the account numbers in the dataframes
            dict_DATA[i] = dict_DATA[i].drop([col for col in DATA.columns if 'Acc' in col], axis=1)
        ###
        cols_ordered = ['Description','Category','In','Out','Date','Balance','Type']
        Plottable_cols = []
        for i in dict_DATA:
            dict_DATA[i]['Category'] = dict_DATA[i]['Type']
            for col in ['Description','Balance','In','Out','Date']:
                dict_DATA[i]['Category'] = dict_DATA[i]['Category'] + ';' + dict_DATA[i][col].apply(string)
            dict_DATA[i].index = range(len(dict_DATA[i])) # Resorting the index
            dict_DATA[i]['Category'] = dict_DATA[i]['Category'].apply(categoriser)
            dict_DATA[i] = dict_DATA[i].sort_values(by='Date', ascending=False)
            dict_DATA[i] = dict_DATA[i][cols_ordered] # Re-Ordering the Columns
            dict_DATA[i]['Description'] = dict_DATA[i]['Description'].apply(capital)
    
        
        for col in dict_DATA[act_nums[0]].columns:
            if dict_DATA[act_nums[0]][col].apply(dataPrep).dtype != object:
                Plottable_cols.append(col)    
    
    return dict_DATA, Plottable_cols