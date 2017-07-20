# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 22:23:37 2016

@author: ellismle
"""



categories_filename = 'Settings/Categories.txt'
save_filepath = 'Data/Demo_Data/'
#number_of_sample_data_files = 3
data_length = 2000



def remove_files_from_folder(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)
        for i in files:
            os.remove(folder+i)
    else: 
        print('\n\nSorry the directory in the settings document couldn\'t be found. Please double check this.\nCurrent folder path = \'%s\'\n'%str(folder))

        

import pandas as pd
import numpy as np
import datetime as dt
import random as rand
import os
from Data import Data as dr


from Data.Data import demo_data

cats = dr.dict_parser(categories_filename)
count = 0

def create_data(data_create_question):
    if 'y' in data_create_question.lower():
        num_accs = input("How many account's worth should I make?\t")
        make_data(num_accs)
        return 0
    elif 'n' in data_create_question.lower():
        print("OK, I'll just try and load the data that is already there.\n")
        return 0
    else:
        create_data(input("Sorry please type yes or no...\t"))

def make_data(num_accs):
    if "c" in num_accs.lower():
        return 0
    try:
        num_accs = int(num_accs)
        print("Okie doke, making "+str(num_accs)+" accounts worth of fake data.")
        for i in range(num_accs):
            datamaker(i,demo_data)
    except TypeError:
        make_data(input("Sorry that's not a number I recognise...\n\nPlease enter a number or type 'c' to cancel"))
        

def datamaker(i, save_filepath): 
    global count
    if count == 0:
        remove_files_from_folder(save_filepath)
    count += 1
    act_n = 'Account Number'
    date = 'Transaction Date'
    bal = 'Balance'
    out = 'Debit Amount'
    In = 'Credit Amount'
    descript = 'Transaction Description'

    column_headers = [act_n,date,bal,out,In,descript]
    
    date1 = dt.datetime(2016,1,1)
    orig_balance = abs(round(rand.gauss(0,1000),2))
    
    if os.path.isdir(save_filepath):
        save_filepath = save_filepath + str(i) + '.csv'
    else:
        return None
    data = pd.DataFrame({i:np.zeros(data_length) for i in column_headers})

    ## Acount Number
    account_number = rand.randint(10000000,99999999)
    data[act_n] = account_number

    ## Transaction Date
    data[date] = pd.date_range(date1,date1+dt.timedelta(data_length-1),freq = 'D')

    ## Debit Amount
    data[out] = [round(abs(rand.gauss(0,34)),2) if rand.randint(0,33) < 32 else 0 for i in range(data_length)]

    ## Credit Amount
    data[In] = data[out]
    def credit_amounter(x):
        if x == 0:
            return round(abs(rand.gauss(451,5)),2)
        else:
            return 0
    data[In] = data[In].apply(credit_amounter)

    ## Balance
    data[bal] = data[In]-data[out]
    f = open('balance','w+')
    f.write(str(orig_balance))
    f.close()

    def balancer(x):
        f = open('balance','r')
        balance = float(f.read())
        f.close()
        new_balance = balance + x
        f = open('balance','w')
        f.write(str(new_balance))
        f.close()
        return new_balance

    data[bal] = data[bal].apply(balancer)
    os.remove('balance')
    
    ## Type
    data['Type'] = 'DEB'

    ## Description
    data[descript] = data[out]
    def describer(x):
        if x > 0:
            lottery = rand.randint(0,100)
            if lottery < 25:
                return cats['Groceries'][rand.randint(0,len(cats['Groceries'])-1)]
            
            elif 24<lottery<30:
                return cats['Activities'][rand.randint(0,len(cats['Activities'])-1)]

            elif 29<lottery<31:
                return cats['Rent, Bills & Fines'][rand.randint(0,len(cats['Rent, Bills & Fines'])-1)]

            elif 30<lottery<45:
                return cats['Car'][rand.randint(0,len(cats['Car'])-1)]

            elif 44<lottery<55:
                return cats['Bars And Pubs'][rand.randint(0,len(cats['Bars And Pubs'])-1)]

            elif 54<lottery<58:
                return cats['Travel'][rand.randint(0,len(cats['Travel'])-1)]

            elif 57<lottery<64:
                return cats['Eating Out'][rand.randint(0,len(cats['Eating Out'])-1)]

            elif 63<lottery<88:
                return cats['Cash'][rand.randint(0,len(cats['Cash'])-1)]

            elif 87<lottery:
                return cats['Online Shopping'][rand.randint(0,len(cats['Online Shopping'])-1)]
        else:
            return 'Money In'

    data[descript] = data[descript].apply(describer)
    data.to_csv(save_filepath,index=False)