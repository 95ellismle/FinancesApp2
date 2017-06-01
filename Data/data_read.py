import pandas as pd

# Permanently removes the Sort-Code in the bank account data because it is not needed.
def data_clean(filepaths):
    for file in filepaths:
        try:
            data = pd.read_csv(file,sep=',')
            for col_name in data.columns:
                col_name_up = col_name.upper()
                if 'INDEX' in col_name_up or 'UNNAMED' in col_name_up or 'SORT' in col_name_up or ' ' == col_name:
                    data = data.drop(col_name,1)
    
            data.to_csv(file,sep=',',index = None)#Saving the data without the sort code
        except UnicodeDecodeError as e:
            print("I couldn't read the files. They seem to be stored in the wrong format.\nPlease check that the statement data is in csv format.\n")
            print("Rogue file = ",file,"\nError = ",e)


# Reads a group of data files and groups them into 1 dataframe.
def data_read(filepaths):
    data = pd.concat([pd.read_csv(file) for file in filepaths]) #Concatenating the account data frames together.
    return data
        