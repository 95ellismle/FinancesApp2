import pandas as pd


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
    data = pd.concat([pd.read_csv(file) for file in filepaths]) #Concatenating the account data frames together.
    return data


# Checks if a substring is in a list of strings and if it is returns the list item
def list_check(search_item, LIST):
    for list_item in LIST:
        if list_item.lower() in search_item.lower() or search_item.lower() in list_item.lower():
            return (True,list_item)
    return False

# Converts the type of a column in a dataframe
def convert_col(df,col,Type,error_msgs):
    col = col.lower()
    col = col[0].upper() + col[1:]
    try:
        if type(Type) == str:
            if 'date' in Type.lower() or 'time' in Type.lower():
                df[col] = pd.to_datetime(df[col])  
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
                if list_check(value[value_index].lower(),dict_values[1]):
                    new_vals[value_index] = dict_values[0]
                    break
        return new_vals
    elif type(value) == int or type(value) == float:
        value = str(value)
    
    elif type(value) == str:
        for dict_values in dictionary.items():
            if list_check(value.lower(),dict_values[1]):
                    return dict_values[0]
    else:
        return 0