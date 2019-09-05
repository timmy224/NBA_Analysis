import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

def getTop12():
    df_players = pd.read_csv('Player_PER_calc.csv')

    # drop index from previous dataframe manipulation
    df_players.drop(columns={'Unnamed: 0', 'Unnamed: 0.1'}, inplace=True)

    df_players.sort_values(['Season', 'Tm', 'MP', 'PER_calc'], ascending=[False, True, False, False], inplace=True)
    df_test = df_players.groupby(['Season', 'Tm']).head(12)

    df_test.to_csv('top12_test.csv')

    return df_test

def nba_histogram():
    """Frequency distribution for top 12 players of each team per season"""
    df_players = getTop12()

    # grabs for a single season
    # PER_values = df_players[df_players['Season'] == '2017-2018']['PER_calc']

    # n, bins, patches = plt.hist(x=PER_values, bins='auto', alpha=0.7, rwidth=0.85)
    # plt.grid(axis='y', alpha=0.7)
    # plt.xlabel('PER Value')
    # plt.ylabel('Frequency')
    # plt.title('PER distribution')
    
    PER_values = {}
    fig, ax = plt.subplots(3, 7, figsize=(16, 8), tight_layout=True, sharey='all')
    
    for i in range(3):
        for j in range(7):
            ax[int('{}'.format(i)), int('{}'.format(j))].set_xticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].set_yticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].tick_params(axis='both', which='both', length=0)
            #ax[int('{}'.format(i)), int('{}'.format(j))].text()

    for i, num  in zip(range(1998, 2019), range(1, 22)):
        PER_values['{}-{}'.format(i, i+1)] = df_players[df_players['Season'] == '{}-{}'.format(i, i+1)]['PER_calc']

        mean_val = round(PER_values['{}-{}'.format(i, i+1)].mean(), 1)
        std_val = round(np.std(PER_values['{}-{}'.format(i, i+1)]), 1)

        fig.add_subplot(3, 7, num)
        n, bins, patches = plt.hist(x=PER_values['{}-{}'.format(i, i+1)], 
                                    bins='auto',
                                    alpha=0.7, 
                                    rwidth=0.85, 
                                    range=(0, 39)
                                    )

        plt.grid(axis='y', alpha=0.7)
        plt.xlabel('PER Value', labelpad=5, fontsize=8)
        plt.title('{}-{}'.format(i, i+1), fontsize=12)
        plt.yticks([10, 20, 30, 40, 50, 60, 70])
        plt.text(22, 50, 'mean: {}\nstd: {}'.format(mean_val, std_val), fontsize=8)

    plt.show()

def nba_boxplots():
    """examine boxplots of teams"""
    df_players = getTop12()

    # grabs for a single season
    PER_values = df_players[df_players['Season'] == '2017-2019']['PER_calc']


def nba_PCA():
    pass

def nba_team_line():
    pass

nba_histogram()