import pandas as pd 
import numpy as np 
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

def getTop12():
    df_players = pd.read_csv('Player_PER_calc.csv')

    # drop index from previous dataframe manipulation
    df_players.drop(columns={'Unnamed: 0', 'Unnamed: 0.1'}, inplace=True)

    df_players.sort_values(['Season', 'Tm', 'MP', 'PER_calc'], ascending=[False, True, False, False], inplace=True)
    df_test = df_players.groupby(['Season', 'Tm']).head(12)

    df_test.to_csv('top12_test.csv')

    return df_test

def histSeasonPlayerPER():
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

def qqSeasonPlayerPER():
    df_players = getTop12()

    PER_values = {}
    fig, ax = plt.subplots(3, 7, figsize=(16, 8), tight_layout=True, sharey='all')
    
    title_list = []
    for i in range(1998, 2019): # to make title list 
        title_list.append('{}-{}'.format(i, i+1))

    for i in range(3):
        for j in range(7):
            ax[int('{}'.format(i)), int('{}'.format(j))].set_xticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].set_yticklabels([])
            ax[int('{}'.format(i)), int('{}'.format(j))].tick_params(axis='both', which='both', length=0)
            ax[int('{}'.format(i)), int('{}'.format(j))].set_title(title_list.pop(0))

    for i, num  in zip(range(1998, 2019), range(1, 22)):
        PER_values['{}-{}'.format(i, i+1)] = df_players[df_players['Season'] == '{}-{}'.format(i, i+1)]['PER_calc']

        sm.qqplot(PER_values['{}-{}'.format(i, i+1)], line='q', ax=fig.add_subplot(3, 7, num), markersize=1)
    
def boxPlayerPER():
    df_players = getTop12()

    PER_values = {}
    positions = ['C', 'PF', 'PG', 'SF', 'SG']
    for pos in positions: 
        PER_values[pos] = df_players[df_players['Pos'] == pos]['PER_calc']

    fig, ax = plt.subplots(figsize=(16, 8))
    ax.boxplot(PER_values.values())
    ax.set_xticklabels(PER_values.keys(), fontsize=16)
    ax.set_title('PER For Different Basketball Positions',  fontsize=20)
    ax.set_ylabel('PER Value', fontsize=16)

def boxcoxPlayerPER():
    df_players = getTop12()

    # There is a single negative PER value. Need to transform so that all 
    # values are positive for scipy BoxCox function 
    df_players['PER_calc'] += 1 
    transformed_val, lambda_val = stats.boxcox(df_players['PER_calc']) 
    transformed_val = transformed_val.tolist()
    df_players.insert(5, 'Trans_PER', transformed_val)
    df_players['PER_calc'] -= 1

    df_players.to_csv('test_trans.csv')
    print('lambda:', lambda_val)
    return df_players, lambda_val

def teamPER_calc():
    df_players = getTop12()

    PER_MP = df_players['PER_calc'] * df_players['MP']
    teamPER = df_players[['Season', 'Tm']]
    teamPER.insert(2, 'PER_MP', PER_MP)

    teamPER = teamPER.groupby(['Season', 'Tm']).sum()
    teamPER.to_csv('test_teamPER.csv')
    return teamPER
    
def teamRatio_calc():
    df_teams = pd.read_csv('BR_1998-2019-Regular-TeamTotals-edit.csv', index_col=0)


    team_tm = {
            'Atlanta Hawks': 'ATL',
            'Boston Celtics': 'BOS',
            'Brooklyn Nets': 'BRK',
            'Charlotte Bobcats': 'CHA',
            'Charlotte Hornets': ['CHH', 'CHO'],
            'Chicago Bulls': 'CHI',
            'Cleveland Cavaliers': 'CLE',
            'Dallas Mavericks': 'DAL',
            'Denver Nuggets': 'DEN',
            'Detroit Pistons': 'DET',
            'Golden State Warriors': 'GSW',
            'Houston Rockets': 'HOU',
            'Indiana Pacers': 'IND',
            'Los Angeles Clippers': 'LAC',
            'Los Angeles Lakers': 'LAL',
            'Memphis Grizzlies': 'MEM',
            'Miami Heat': 'MIA',
            'Milwaukee Bucks': 'MIL',
            'Minnesota Timberwolves': 'MIN',
            'New Jersey Nets': 'NJN',
            'New Orleans Hornets': 'NOH',
            'New Orleans/Oklahoma City Hornets': 'NOK',
            'New Orleans Pelicans': 'NOP',
            'New York Knicks': 'NYK',
            'Oklahoma City Thunder': 'OKC',
            'Orlando Magic': 'ORL',
            'Philadelphia 76ers': 'PHI',
            'Phoenix Suns': 'PHO',
            'Portland Trail Blazers': 'POR',
            'Sacramento Kings': 'SAC',
            'San Antonio Spurs': 'SAS',
            'Seattle SuperSonics': 'SEA',
            'Toronto Raptors': 'TOR',
            'Utah Jazz': 'UTA',
            'Vancouver Grizzlies': 'VAN',
            'Washington Wizards': 'WAS',
        }

    # Charlotte Hornets name splits 
    CHH_season = []
    for i in range(1998, 2002):
        CHH_season.append('{}-{}'.format(i, i+1))

    CHO_season = []
    for i in range(2014, 2019):
        CHO_season.append('{}-{}'.format(i, i+1))

    # adding tm col to df_teams_inst 
    tm_list = []
    for each_team, season in zip(df_teams['Team'], df_teams['Season']):
        if each_team == 'Charlotte Hornets':
            if season in CHH_season:
                tm_list.append(team_tm['Charlotte Hornets'][0])
            else: 
                tm_list.append(team_tm['Charlotte Hornets'][1])
        else:
            tm_list.append(team_tm[each_team])
    df_teams.insert(3, 'Tm', tm_list)

    win_ratio = df_teams['W'] / (df_teams['W'] + df_teams['L'])
    df_teams.insert(5, 'Win Ratio', win_ratio)

    df_teams.to_csv('team_tm.csv')

def reg_teamPER_teamRatio():
    pass

def nba_team_line():
    pass

teamRatio_calc()