import pandas as pd
from scipy.optimize import curve_fit
import numpy as np
import sys
import datetime as dt
import matplotlib.pyplot as plt


sys.path.append("/home/ellismle/Documents/Other/Finances_app2/")
from Data import Data as dr

bank_statement_folder_path = '/home/ellismle/Documents/Other/Finances-App(non git)/Stats/'

dict_bank_data = dr.Data_Read(bank_statement_folder_path)[0]
data = dict_bank_data[list(dict_bank_data.keys())[0]]

secs_in_a_day = dt.timedelta(1).total_seconds()
# A function to check whether a date is near another date within a tolerance
def near_date( date1, date2, tolerance=dt.timedelta(1) ):
    return np.abs(date1-date2) > tolerance
    
'''
# A function to take the time derivatives of the data.
def time_deriv(dates, dataIn):
    derivatives = []
    new_data = []
    new_dates = []
    for i in range(len(dates)-1):
        time_diff = (dates[i+1] - dates[i]).total_seconds()/secs_in_a_day
        data_diff = dataIn[i+1] - dataIn[i]
        if time_diff != 0:
            derivatives.append(data_diff/time_diff)
            new_data.append(dataIn[i])
            new_dates.append(dates[i])
    return (new_dates, derivatives, new_data)
'''

# A function to create a mask for finding outliers in an array
def outliers_mask(array, array_tol, std_tol=2, diff = False, outliers = False):
    mean = np.mean(array_tol)
    std_dev = np.std(array_tol)
    if not diff:
        diff = mean + (std_tol*std_dev)
    if outliers:
        mask = np.ma.masked_where(np.abs(array_tol) >= diff, array)
    else:
        mask = np.ma.masked_where(np.abs(array_tol) <= diff, array)
    return mask

def str2float(i):
    try:
        return float(i)
    except:
        return False

Dates = data['Date']
Balance = data['Balance']

#x, y, diff_bal = time_deriv(Dates, Balance)



fig = plt.figure()
ax = fig.add_subplot(111)
twin = plt.twinx(ax)

dates_mask = outliers_mask(Dates, data['In'].apply(str2float), std_tol=2.5)
change_dates = []
dates_inds = []
for i in range(len(dates_mask)):
    if dates_mask[i] and dates_mask[i] not in change_dates:
        dates_inds.append(i)
        change_dates.append(dates_mask[i])

tol_dates = []
for i in range(len(change_dates)-1):
    if near_date(change_dates[i], change_dates[i+1], np.timedelta64(24*60,'h')):
       tol_dates.append(change_dates[i])
       tol_dates.append(change_dates[i+1])

ax.plot(x, y, 'g.')


#ax.plot(x, y, 'k.')
for i in change_dates:
    ax.axvline(i,color='g')
    #ax.axvline(tol_dates[i+1],color='r')
plt.show()



'''

'''