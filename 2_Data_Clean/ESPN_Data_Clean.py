import pandas as pd
import numpy as np
import csv 

def dataClean():
    
    df = pd.read_csv('ESPN_2002-2019-Regular-PlayerStats-raw.csv')
    df.dropna(inplace=True)
    df.reset_index(drop= True, inplace=True)
    df.rename(columns={'Team': 'Team Abbv'}, inplace=True)


    df['Team Abbv'].replace('', np.nan, inplace=True)

    df.to_csv('ESPN_2002-2019-Regular-PlayerStats-edit.csv')

    return df
            
dataClean()