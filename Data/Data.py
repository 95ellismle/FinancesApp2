import pandas as pd
import os
from __main__ import categories_filename
import datetime as dt
import string as string_lib
from Gui import StyleSheets as St

# Permanently removes the Sort-Code in the bank account data because it is not needed.
def data_clean(filepaths):
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
    
    
# Reads a group of data files and groups them into 1 dataframe.
def data_read(filepaths):
    if type(filepaths) == list:
        data = pd.concat([pd.read_csv(file) for file in filepaths]) #Concatenating the account data frames together.
    if type(filepaths) == str:
        files = [i for i in os.listdir(filepaths) if '.csv' in i]
        data = {int(i[:i.find('.csv')]):pd.read_csv('./'+i) for i in files}
    return data


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
    except TypeError:
        None
        
# Converts a datetime to a string for displaying the dataframe data
def TablePrep(item):
    try:
        return dt.datetime.strftime(item,St.date_format)
    except TypeError:
        try:
            return str(item)
        except:
            return None

# Converts a string to an integer if possible and if it below a certain value
def str2int(string):
    try:
        return int(string)
    except:
        return False

# Convert a string to a float and ignore exceptions
def dataPrep(i):
    try:
        return float(i)
    except ValueError:
        try:
            return pd.to_datetime(i,format=St.date_format)
        except ValueError:
            return None
    except TypeError:
        return i
    
# Converts the type of a column in a dataframe
def convert_col(df,col,Type,error_msgs=[]):
    col = col.lower()
    col = col[0].upper() + col[1:]
    try:
        if type(Type) == str:
            if 'date' in Type.lower() or 'time' in Type.lower():
                df[col] = pd.to_datetime(df[col],format=St.date_format)  
        else:
            df[col] = df[col].apply(Type)
    except KeyError as e:
         error_msgs.append('There is no '+col+' column in the bank_data')


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
        return 0


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

# Categorises the data
def categoriser(item):
    Type, Desc, Bal, In, Out, Date = item.lower().split(';')

    if Type == 'cpt':
        return 'Cash'
    elif Type == 'bgc':
        return 'Salary'
    elif Type == 'so':
        return 'Rent, Bills and Fines'
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

    if cat == 'High Street':
        if list_check(Desc,cats['Groceries']):
            return 'Groceries'
        elif list_check(Desc,cats['Online Shopping']):
            return 'Online Shopping'
        else:
            return 'High Street'
    
    if cat == 'Car':
        if list_check(Desc,cats['High Street']):
            return 'High Street'       
        elif list_check(Desc,cats['Online Shopping']):
            return 'Online Shopping'
        else:
            return 'Car'
    
    if cat == 'Bars and Pubs':
        if list_check(Desc,cats['Eating Out']):
            return 'Eating Out'
        else:
            return 'Bars and Pubs'
    else:
        return cat
