#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 16:02:03 2017

@author: ellismle
"""

import pandas as pd
import datetime as dt
from Settings import StyleSheets as St


# Converts a dictionary to the format used in the settings files.
def dict2str(dictionary):
    string =''
    for i in dictionary:
        string += str(i) + ': ' + ', '.join(dictionary[i]) + ';\n'
    return string

# Converts to a string with no empty space at the end
def string(i):
    return str(i).rstrip()

# Converts string to either an int or a float.
def str2num(i):
    try:
        if float(i) == int(i):
            return int(i)
        else:
            return float(i)
    except:
        return i

# Converts from a pd.DataFrame column of strings to dates
def str2date(col):
    try:
        return col.apply(datetimeformat)
    except:
        try:
            return pd.to_datetime(col)
        except:
            return col

# Returns a lowercase string
def lower(i):
    try:
        return i.lower()
    except (TypeError, AttributeError):
        pass
        
# Converts a string to a date    
def datetimeformat(i):
    return dt.datetime.strptime(i,St.date_format)

# Converts from a date to a string
def date2str(dat):
    return dt.datetime.strftime(dat,St.date_format)

# Converts a string to an integer if possible and if it below a certain value
def str2int(string):
    try:
        return int(string)
    except:
        return string

# converts a string to a float
def str2float(i):
    try:
        return float(i)
    except:
        return None

# converts a float to a string
def float2str(i):
    try:
        return str(i)
    except:
        return None   
    
# Converts a datetime to a string for displaying the dataframe data
def tablePrep(item):
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
        
    