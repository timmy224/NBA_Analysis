import pandas as pd
import numpy as np
import csv 

def dataClean():
    
    df = pd.read_csv('ESPN_2002-2019-Regular-PlayerStats-raw.csv')
    df.dropna(inplace=True)
    df.reset_index(drop= True, inplace=True)
    df.rename(columns={'Team': 'Team Abbv'}, inplace=True)


    for each in df['Team Abbv']:
        teams = each.split('/')
        

    print(df)
            
dataClean()