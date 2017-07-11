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

# Removes Certain Strings from the Description of the Transaction to make it more readable
def unclutter(string):
    for i in ['1','2','3','4','5','6','7','8','9','0','(',')','CD', '\\', '/']:
        string = string.replace(i,'')
    return string

# Capatilises the first letter of each string
def capital(i):
    return osl.capwords(i) 