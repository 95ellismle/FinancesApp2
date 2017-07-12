#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 17:50:54 2017

@author: ellismle
"""

import string as osl


# Returns an uppercase string
def up(x):
    if type(x) == str:
        try:
            return x.upper()
        except AttributeError:
            return x
    else:
        return x

# Strips letters of a string
def letterStrip(string, letters='abcdefghijklmnopqrstuvwxyz'):
    for i in letters:
        string = string.replace(i,'')
    return string

# Removes any comments (Those with a hash) from some text
def comment_remove(string):
    x = [i for i in string.split('\n') if i]
    x = [i for i in x if i[0] != '#']
    x = [i[:i.find('#')] if i.find('#') != -1 else i for i in x ]
    string = '\n'.join(x)
    return string

# Detects the funny nonsense character strings that sometimes get put at the end of bank data
def nonsense_string(string):
         vowels = ['a','e','i','o','u','y']
         length = len(string)
         num_vowels = sum(x in vowels for x in string)
         ratio = num_vowels/length
         if ratio < 0.2 and length > 4:
             return False
         else:
             return True 

# Removes Certain Strings from the Description of the Transaction to make it more readable
def unclutter(string):
    string = string.upper()
    for i in ['1','2','3','4','5','6','7','8','9','0','(',')','CD', ':', '\\', '/', '%']:
        string = string.replace(i,'')
    string = capital(string)
    for i in ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec',',']:
        string = string.replace(i,'')
    st = ''
    for i in string.split(' '):
        if i:
            if nonsense_string(i):
                st += ' ' + i
    if st == '':
        return string
    return st

# Capatilises the first letter of each string
def capital(i):
    try:
        return osl.capwords(i) 
    except AttributeError:
        return None