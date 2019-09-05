""" Cleans raw data scraped from website """
import pandas as pd 
import numpy as np 

def Player_Totals_Clean():
    """
    Cleans player data from 1998-2019 seasons
        - adds Season column and populates with appropriate season years
        - REFACTOR duplicates variable with numpy.where()
        - removes website suffix and asterisk from player name 
        - replaces null {float} values with 0

    Input: None (hardcoded file name)

    Output: CSV file 
    """
    df = pd.read_csv('1999-2019-Regular-PlayerStats-raw.csv')

    # Add season column 
    df.insert(0, 'Season', '')

    # Remove duplicate headers from each season after first 
    # ToDo - Refactor using numpy.where() 
    duplicates = [507, 1004, 1542, 2043, 2527, 3113, 3699, 4263, 4780, 5376, 
                  5959, 6538, 7164, 7716, 8290, 8902, 9554, 10133, 10729, 11394]

    df2 = df.drop(duplicates).reset_index(drop=True)

    # Need to take row numbers and subtract by correction factor 
    # (dif. # of rows per season) 
    duplicates_corr = []

    for each, sub_correction in zip(duplicates,range(0, len(duplicates))):
        duplicates_corr.append(each-sub_correction)

    # Populates season years in season column 
    old_row_num = 0
    for row_num, ind_year in zip(duplicates_corr, range(1999, 2020)): 
        df2.iloc[old_row_num:row_num, 0:1] = '{}-{}'.format(ind_year-1,ind_year)
        old_row_num = row_num

        if row_num == duplicates_corr[-1]:
            df2.iloc[row_num:, 0:1] = '{}-{}'.format(ind_year, ind_year+1)

    # Removes website suffix from value found in player name
    name_only = []

    for player_name in df2.iloc[:, 2]:
        first_lastname = player_name.split('\\')[0]
        first_lastname = first_lastname.replace('*', '')
        name_only.append(first_lastname)

    df2.iloc[:, 2] = name_only

    # fills in null values with 0
    for each in df2:
        df2[each].fillna(0, inplace=True)

    # Saves dataframe to CSV file
    df2 = df2[df2.Tm != 'TOT']
    df2 = df2[df2.MP != 0]
    df2.to_csv('1999-2019-Regular-PlayerStats-edit.csv')

def Team_Totals_Clean():
    """
    Cleans team data from 1998-2019 seasons
        - adds Season column and populates with appropriate season years
        - removes asterisk from team name
        - replaces null {float} values with 0
        - drop cols: Arena, Attend, Attend/Game

    Input: None (hardcoded file name)

    Output: CSV file 
    """
    df = pd.read_csv('1999-2019-Regular-TeamTotals-raw.csv')

    # Remove duplicate headers from each season after first
    df.columns = df.iloc[0]

    duplicates_29teams = [0] # first and last rows
    duplicates_30teams = []

    for i in range(30, 193, 32): # for rows with 29 teams in NBA season
        for j in range(3):
            duplicates_29teams.append(i+j) 

    for i in range(223, 685, 33): # for rows with 30 teams in NBA season
        for j in range(3):
            duplicates_30teams.append(i+j)

    duplicates_30teams.append(685)

    df2 = df.drop(duplicates_29teams)
    df2 = df2.drop(duplicates_30teams).reset_index(drop=True)

    df2.insert(0, 'Season', '')
    # find the first row of each new season
    firstRow_of_each_season = np.where(df2['Rk'] == '1')

    # Populate season column with corresponding season years
    old_row_num = 0
    for row_num, ind_year in zip(firstRow_of_each_season[0], range(1998, 2020)): 
        df2.iloc[old_row_num:row_num, 0:1] = '{}-{}'.format(ind_year-1,ind_year)
        old_row_num = row_num

        if row_num == firstRow_of_each_season[0][-1]:
            df2.iloc[row_num:, 0:1] = '{}-{}'.format(ind_year, ind_year+1)

    # Removes * from the end of team names
    name_only = []

    for team_name in df2.iloc[:, 2]:
        name_only.append(team_name.replace('*', ''))
    
    df2.iloc[:, 2] = name_only

    # drop unnecessary columns 
    df2.drop(['Arena', 'Attend.', 'Attend./G'], axis=1, inplace=True)

    # fills in null values with 0 
    for each in df2:
        df2[each].fillna(0, inplace=True)

    df2.to_csv('1999-2019-Regular-TeamTotals-edit.csv')

Player_Totals_Clean()
Team_Totals_Clean()