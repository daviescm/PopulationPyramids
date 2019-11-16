# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 09:56:59 2019

@author: daviescm
"""

import pandas as pd
import numpy as np

import os

import matplotlib.pyplot as plt
import seaborn as sns

#%% Import data

cwd = os.getcwd()

df = pd.read_csv(cwd+'jeffcoky.csv')

#%% Recode values and clean data

df = df.applymap(lambda x: x.strip() if type(x)==str else x)
df['Sex'] = df['Sex'].replace('Females', 'Female')

df = pd.melt(df, id_vars=['Year', 'Sex'], value_vars=['0to4YearOlds', '5to9YearOlds',
            '10to14YearOlds', '15to19YearOlds', '20to24YearOlds', '25to29YearOlds',
            '30to34YearOlds', '35to39YearOlds', '40to44YearOlds', '45to49YearOlds',
            '50to54YearOlds', '55to59YearOlds', '60to64YearOlds', '65to69YearOlds',
            '70to74YearOlds', '75to79YearOlds', '80to84YearOlds', '85YearsAndOlder',
            'TotalPopulation', 'MedianAge'], var_name='AgeRange', value_name='Value')

#%%

years = df['Year'].sort_values().unique().tolist()
df_list = list()
for i in years:
    # Create empty dataframe with every possible category
    blank_df = pd.DataFrame({'AgeRange': ['0to4YearOlds', '5to9YearOlds', '10to14YearOlds',
                                          '15to19YearOlds', '20to24YearOlds', '25to29YearOlds',
                                          '30to34YearOlds', '35to39YearOlds', '40to44YearOlds',
                                          '45to49YearOlds', '50to54YearOlds', '55to59YearOlds',
                                          '60to64YearOlds', '65to69YearOlds', '70to74YearOlds',
                                          '75to79YearOlds', '80to84YearOlds', '85YearsAndOlder',
                                          '0to4YearOlds', '5to9YearOlds', '10to14YearOlds',
                                          '15to19YearOlds', '20to24YearOlds', '25to29YearOlds',
                                          '30to34YearOlds', '35to39YearOlds', '40to44YearOlds',
                                          '45to49YearOlds', '50to54YearOlds', '55to59YearOlds',
                                          '60to64YearOlds', '65to69YearOlds', '70to74YearOlds',
                                          '75to79YearOlds', '80to84YearOlds', '85YearsAndOlder'],
                            'Sex': ['Female', 'Female', 'Female', 'Female', 'Female',
                                    'Female', 'Female', 'Female', 'Female', 'Female',
                                    'Female', 'Female', 'Female', 'Female', 'Female',
                                    'Female', 'Female', 'Female', 'Male', 'Male',
                                    'Male', 'Male', 'Male', 'Male', 'Male', 'Male',
                                    'Male', 'Male', 'Male', 'Male', 'Male', 'Male',
                                    'Male', 'Male', 'Male', 'Male'],
                            'Sequence': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21,
                                         23, 25, 27, 29, 31, 33, 35, 2, 4, 6, 8,
                                         10, 12, 14, 16, 18, 20, 22, 24, 26, 28,
                                         30, 32, 34, 36]})
    # Create a dataframe for year i
    df_i = df[df['Year'] == i]
    # Find the median age of all sexes and assign to variable
    medianage = df_i[(df_i['Sex'] == 'Total') & (df_i['AgeRange'] == 'MedianAge')]['Value'].sum()
    # Create metric assigning a sequence value to each possible median age value for plotting on y-axis
    medianage_sequence = np.where(medianage < 5, 17,
                                  np.where(medianage < 10, 16,
                                           np.where(medianage < 15, 15,
                                                    np.where(medianage < 20, 14,
                                                             np.where(medianage < 25, 13,
                                                                      np.where(medianage < 30, 12,
                                                                               np.where(medianage < 35, 11,
                                                                                        np.where(medianage < 40, 10,
                                                                                                 np.where(medianage < 45, 9,
                                                                                                          np.where(medianage < 50, 8,
                                                                                                                   np.where(medianage < 55, 7,
                                                                                                                            np.where(medianage < 60, 6,
                                                                                                                                     np.where(medianage < 65, 5,
                                                                                                                                              np.where(medianage < 70, 4,
                                                                                                                                                       np.where(medianage < 75, 3,
                                                                                                                                                                np.where(medianage < 80, 2,
                                                                                                                                                                         np.where(medianage < 85, 1, 0)))))))))))))))))
    # Move median age line up and down within interval
    ageline = np.where(np.round(medianage) % 5 == 1, medianage_sequence + 0.8,
                        np.where(np.round(medianage) % 5 == 2, medianage_sequence + 0.6,
                                 np.where(np.round(medianage) % 5 == 3, medianage_sequence + 0.4,
                                          np.where(np.round(medianage) % 5 == 4, medianage_sequence + 0.2,
                                                   medianage_sequence+1))))
    # Assign negative values to all cases where Sex = Male to reflect graph over 0
    df_i['Value'] = np.where(df_i['Sex'] == 'Male', df_i['Value'] * -1, df_i['Value'])
    # Merge annual dataframe with empty dataframe to keep only the factors of interest
    df_i = blank_df.merge(df_i, how='left', on=['AgeRange', 'Sex']).sort_values('Sequence').fillna(0).reset_index(drop=True)
    # Save created annual dataframe to list
    df_list.append(df_i)
    # Create the plot, assign colors to groups of interest (Sex), and sort values in descending order (oldest on top)
    fig, ax = plt.subplots(figsize=(10, 5))
    group_col = 'Sex'
    order_of_bars = df_i['AgeRange'].unique()[::-1]
    colors = [plt.cm.RdYlBu(x/float(len(df_i[group_col].unique())-1)) for x in range(len(df_i[group_col].unique()))]
    # Create horizontal barplot using values assigned above
    for c, group in zip(colors, df_i[group_col].unique()):
        sns.barplot(x='Value', y='AgeRange', data=df_i.loc[df_i[group_col]==group, :], order=order_of_bars, color=c, alpha=0.9, label=group, ci=None)
    # Add value labels outside the ends of the bars
    for y, (x, c) in enumerate(zip(df_i['Value'].iloc[::-1], df_i['Value'].iloc[::-1])):
            if y % 2 == 0:
                ax.text(x-3500, ((y+1)/2)-.5, str(int(abs(c))), ha='center', va='center', color='black', fontsize=8)
            else:
                ax.text(x+3500, (y/2)-.5, str(int(abs(c))), ha='center', va='center', color='black', fontsize=8)
    # Set the x-axis length and add labels and ticks to all axes
    plt.xlim(-50000, 60000)
    plt.title("Population Pyramid of Jefferson County KY, " +str(i), fontsize=22)
    plt.xlabel("Population Estimate", fontsize=16)
    plt.ylabel("Age Range", fontsize=16)
    ax.set_xticklabels([])
    ax.set_yticklabels(['85+', '80-84', '75-79', '70-74', '65-69', '60-64', '55-59', '50-54', '45-49', '40-44', '35-39', '30-34', '25-29', '20-24', '15-19', '10-14', '5-9', '0-4'])
    plt.yticks(fontsize=10)
    # Add the dashed horizontal line at the median age point set above
    plt.axhline(y=ageline, xmin=0, xmax=1, color='k', linestyle='--', alpha=0.5)
    # Add text above median age line and total numbers in bottom right corner; add legend in top right corner
    ax.text(42500, ageline-0.1, 'Median Age: {:.2f}'.format(medianage), fontsize=8)
    ax.text(42500, 15.5, '# Men: '+str(abs(df_i[df_i['Sex'] == 'Male']['Value']).sum().astype(int)), fontsize=8)
    ax.text(42500, 16.25, '# Women: '+str(abs(df_i[df_i['Sex'] == 'Female']['Value']).sum().astype(int)), fontsize=8)
    ax.text(42500, 17, '# Total: '+str(abs(df_i['Value']).sum().astype(int)), fontsize=8)
    plt.legend(loc=(0.85,0.85))
    # Show figure and save
    plt.show()
    fig.savefig(cwd+'JeffCoPopPyramid'+str(i)+'.png')
    
