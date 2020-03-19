# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 22:15:08 2020

@author: Beaver
"""

import numpy as np
import pandas as pd

#Reading data from csv-file.
data = pd.read_csv('cable1.csv', header=None, encoding='cp1251')

#Defining function for splitting the cable designation.
def split_num(line):
    return line.split('-')[-1]

#Creating new column of cable numbers (last portion of cable designation),
#Changing its format from string to integer and sorting by this column.
data[1] = data[0].apply(split_num)
data[1] = pd.to_numeric(data[1])
data.sort_values(by=data.columns[1], inplace=True)

#Finding duplicates and number of empty slots required for their placement.
#Cutting duplicates from the initial dataframe (to a separate dataframe).
#Dropping cut duplicates from the initial dataframe.
df = data[data[1].duplicated()]
empty_slots_required = len(df)
data.drop_duplicates(subset = data.columns[1], inplace = True)

#Function for finding missed numbers in a natural number sequence.
def missed_numbers(n_seq, k):
    missed = []
    i, j, l = 0, 0, 0
    while(l<k):
        if i+1 == n_seq[j]:
            i += 1
            j += 1
        else:
            missed.append(i+1)
            l += 1
            i += 1
    return missed

#Setting the array of numbers for duplicates.
n_for_d = np.asarray(missed_numbers(data[1].values, empty_slots_required), dtype=np.int64)

#Adding the columns with new cable name and number to the dataframe.
#So it could be seen was that cable name a duplicate or not after merging the
#dataframe with duplicates removed and the dataframe containing duplicates.
data.loc[:, 'new_number'] = pd.Series(data[1].values, index=data.index)
data.loc[:, 'new_name'] = pd.Series(data[0].values, index=data.index)

#Adding the column with new numbers to the dataframe containing duplicates.
df.loc[:, 'new_number'] = pd.Series(n_for_d, index=df.index)

#Function for creating array of new names from column of old names 
#and column of new numbers. Obviously the columns must be of equal length.
def replace_third(old_names, new_numbers):
    l = len(old_names)
    new_names = []
    for i in range(l):
        name = old_names[i].split('-')
        new_names.append(name[0] + '-' + name[1] + '-' + str(new_numbers[i]))
    return new_names

#Creating array of new names with the use of 'replace_third' function
new_name = replace_third(df[0].values, df['new_number'].values)

#Adding the column with new names to the dataframe containing duplicates.
#Now both dataframes have the same set of column names.
df.loc[:, 'new_name'] = pd.Series(new_name, index=df.index)

#Combining the dataframe with duplicates removed and the dataframe containing duplicates.
#So the combined dataframe will represent the transformed initial dataframe with 
#information about initial names and numbers and the same after duplicates removal.
#Indices of the dataframe will be saved in excel-file for making it possible to find
#the cables in the initial cable list.
data_result = data.append(df, verify_integrity = True)

#Sorting the combined dataframe.
data_result = data_result.sort_values(by=['new_number'])

#Writing both dataframes to excel files to have a representation of changes made
#on the initial dataframe and representation of found duplicates with numbers and names
#before and after the change.

#Setting widths for columns of the dataframes in excel file for better viewing.
#The dataframe with duplicates is contained in the combined dataframe, so the last
#is used to calculate these widths.
w1 = data_result[0].map(len).max() + 2
w3 = len('new_number') + 2
w4 = data_result['new_name'].map(len).max() + 2

#Writing the dataframe with duplicates.
writer = pd.ExcelWriter('dublicates.xlsx', engine = 'xlsxwriter')
df.to_excel(writer)
worksheet = writer.sheets['Sheet1']
worksheet.set_column(1, 1, w1)
worksheet.set_column(3, 3, w3)
worksheet.set_column(4, 4, w4)
writer.save()

#Writing the combined dataframe.
writer = pd.ExcelWriter('new_cables.xlsx', engine = 'xlsxwriter')
data_result.to_excel(writer)
worksheet = writer.sheets['Sheet1']
worksheet.set_column(1, 1, w1)
worksheet.set_column(3, 3, w3)
worksheet.set_column(4, 4, w4)
writer.save()