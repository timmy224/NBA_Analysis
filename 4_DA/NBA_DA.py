import pandas as pd 
import numpy as np 
from scipy import stats
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt

def getTop12():
    """
    returns: top 12 players per team per season
    * dataframe
    * excel: 'top12_test.csv'
    """

    df_players = pd.read_csv('0_Player_PER_calc.csv')

    # drop index from previous dataframe manipulation
    df_players.drop(columns={'Unnamed: 0', 'Unnamed: 0.1'}, inplace=True)

    df_players.sort_values(['Season', 'Tm', 'MP', 'PER_calc'], ascending=[False, True, False, False], inplace=True)
    df_test = df_players.groupby(['Season', 'Tm']).head(12)

    df_test.to_csv('1_top12_player.csv')

    return df_test

def hist_SeasonPlayerPER():
    """Frequency distribution for top 12 players of each team per season

    returns: histogram with of player PER across different season
    """
    df_players = getTop12()
    
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

def qq_SeasonPlayerPER():
    """Q-Q plot for player PER rating per season"""
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

def boxplot_PlayerPER():
    """boxplot of player PER"""
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

def boxcox_PlayerPER():
    """Boxcox normality test for player PER"""

    df_players = getTop12()

    # There is a single negative PER value. Need to transform so that all 
    # values are positive for scipy BoxCox function 
    df_players['PER_calc'] += 1 
    transformed_val, lambda_val = stats.boxcox(df_players['PER_calc']) 
    transformed_val = transformed_val.tolist()
    df_players.insert(5, 'Trans_PER', transformed_val)
    df_players['PER_calc'] -= 1

    #df_players.to_csv('test_trans.csv')
    print('lambda:', lambda_val)
    return df_players, lambda_val

def teamPER_calc():
    """calculates team PER value"""
    df_players = getTop12()
    df_players = df_players[['Season', 'Player', 'PER_calc', 'Tm', 'MP']]

    PER_MP = df_players['PER_calc'] * df_players['MP']
    df_players.insert(2, 'log(PER * MP)', PER_MP)

    df_players.sort_values(['Season', 'Tm'], inplace=True)

    teamPER = np.log(df_players.groupby(['Season', 'Tm'])['log(PER * MP)'].sum())

    teamPER.reset_index().to_csv('2_teamPER.csv')

def teamRatio_calc():
    """calculates team win ratio
    returns list
    """
    df_teams = pd.read_csv('0_BR_1998-2019-Regular-TeamTotals-edit.csv', index_col=0)

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
    

    df_teams.to_csv('3_team_data.csv')

def teamPER_winRatio():
    """creates dataframe with teamPER and team win ratio
    adds conference column to team_data
    
    returns: dataframe
    """
    df_team_data = pd.read_csv('3_team_data.csv', index_col=0)
    df_teamPER = pd.read_csv('2_teamPER.csv', index_col=0)

    df_team_data.sort_values(['Season', 'Tm'], ascending=[True, True], inplace=True)
    df_teamPER.sort_values(['Season', 'Tm'], ascending=[True, True], inplace=True)

    df_teamPER.index = df_team_data.index # align index of dataframes
    df_team_data.insert(5, 'Team PER', df_teamPER['log(PER * MP)'])

    # adding conference to df for colormapping in corr_teamPER_winRatio()
    western = {
        'LAL',
        'LAC', 
        'DEN', 
        'DAL', 
        'HOU', 
        'UTA', 
        'OKC', 
        'SAC', 
        'POR', 
        'PHO', 
        'MIN', 
        'SAS', 
        'MEM', 
        'NOP', 
        'GSW', 
        'SEA', 
        'VAN', 
    }

    tm_conf_list = []
    for each in df_team_data['Tm']:
        if each in western:
            tm_conf_list.append('Western')
        else: 
            tm_conf_list.append('Eastern')

    df_team_data.insert(4, 'Conference', tm_conf_list)

    df_team_data.to_csv('4_team_data_final.csv')

def corr_teamPER_winRatio():
    """correlation of team PER and win ratio for each season"""

    df_teams = pd.read_csv('4_team_data_final.csv')

    for each in range(2016, 2019):
        
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = list(ind_season['Team PER'])
        y_data = list(ind_season['Win Ratio'])
        names = list(ind_season['Tm'])
        
        colormap = []
        for each in ind_season['Conference']:
            if each == 'Western':
                colormap.append('tab:red')
            else: 
                colormap.append('tab:blue')

        fig = plt.figure(figsize=(10, 8))
        ax = plt.subplot(111)
        ax.set_xmargin(0.05)
        ax.set_ymargin(0.05)

        plt.scatter([], [], color='r', label='Western')
        plt.scatter([], [], color='b', label='Eastern')
        plt.legend(loc="lower right")

        for i,type in enumerate(names):
            x = x_data[i]
            y = y_data[i]
            plt.scatter(x, y, color=colormap[i], s=15)
            plt.text(x, y-0.01, type, fontsize=7)

        trend = np.polyfit(x_data,y_data,1)
        trendpoly = np.poly1d(trend) 
        ax.plot(x_data,trendpoly(x_data), c='orange')

        plt.title('Team PER v. Win Ratio During Regular Season: {}'.format(ind_season['Season'].iloc[0]))
        plt.ylabel('Win Ratio (Games Won / Total Games)')
        plt.xlabel('Team PER (log(Player PER * Player MP))')

        
    plt.show()
corr_teamPER_winRatio()
def ols_teamPER_winRatio():
    """returns table of OLS metrics"""
    df_teams = pd.read_csv('4_team_data_final.csv')

    stand_residual_dict = {}
    for each in range(2016, 2019):
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = ind_season['Win Ratio']
        x_data = sm.add_constant(x_data)
        y_data = ind_season['Team PER']
    
        ols_model = sm.OLS(y_data, x_data)
        results = ols_model.fit()
        print('{}-{} Season \n'.format(each, each+1), results.summary())

        # create instance of influence
        influence = results.get_influence()
        # residuals
        standardized_residuals = influence.resid_studentized_internal
        studentized_residuals = influence.resid_studentized_external
        #print('Standardized residuals \n', standardized_residuals)
        #print('Studentized residuals \n',  studentized_residuals)

        stand_residual_dict['{}-{}'.format(each, each+1)] = standardized_residuals
    return stand_residual_dict

def glm_teamPER_winRatio():
    """returns table of GLM metrics"""
    df_teams = pd.read_csv('4_team_data_final.csv')

    for each in range(2013, 2014):
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = ind_season['Win Ratio']
        x_data = sm.add_constant(x_data)
        y_data = ind_season['Team PER']
    
        glm_model = sm.GLM(y_data, x_data)
        results = glm_model.fit()
        print(results.summary())
        
def huber_teamPER_winRatio():
    """returns table of RLM using Huber's"""
    df_teams = pd.read_csv('4_team_data_final.csv')

    for each in range(2013, 2014):
        ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(each, each+1)]
    
        x_data = ind_season['Win Ratio']
        x_data = sm.add_constant(x_data)
        y_data = ind_season['Team PER']
    
        glm_model = sm.RLM(y_data, x_data)
        results = glm_model.fit()
        print(results.summary())

def residuals_fitted_teamPER(constant, X1_coefficient, start_year):
    """generates residual plot
    Parameters:
    * constant {float}
    * 1 coefficient {float}
    """
    df_teams = pd.read_csv('4_team_data_final.csv')

    ind_season = df_teams[df_teams['Season'] == '{}-{}'.format(start_year, start_year+1)]

    x_actual = list(ind_season['Win Ratio'])
    y_actual = list(ind_season['Team PER'])
    names = list(ind_season['Tm'])

    

    # generating y-predicted values from regression model
    y_pred = []
    for x_val in x_actual:
        y_pred_val = constant + (X1_coefficient * x_val)
        y_pred.append(y_pred_val)
    
    # calculating residuals
    residual_vals = []
    for obs, pred in zip(y_actual, y_pred):
        res_val = obs - pred
        residual_vals.append(res_val)

    #automate later?
    #residual_dict['{}-{}'.format(each, each+1)] = residual_vals #alt use ind_season['Season'].iloc[0]

    colormap = []
    for each in ind_season['Conference']:
        if each == 'Western':
            colormap.append('tab:red')
        else: 
            colormap.append('tab:blue')
    
    fig = plt.figure(figsize=(10, 8))
    ax = plt.subplot(111)
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.05)

    plt.scatter([], [], color='r', label='Western')
    plt.scatter([], [], color='b', label='Eastern')
    plt.legend(loc="lower right")

    for i,type in enumerate(names):
        x = y_actual[i]
        y = residual_vals[i]
        plt.scatter(x, y, color=colormap[i], s=15)
        plt.text(x+0.002, y-0.002, type, fontsize=7)

    plt.hlines(0, linestyles='dashed', xmin=min(y_actual), xmax=max(y_actual))

    plt.title('Residuals v. Fitted Model: {} Season'.format(ind_season['Season'].iloc[0]))
    plt.ylabel('Residuals')
    plt.xlabel('Fitted Values')

    plt.show()

# residuals_fitted_teamPER(12.3710, 0.6108, 2018) # 18-19
# residuals_fitted_teamPER(12.4140, 0.5646, 2017) # 17-18
# residuals_fitted_teamPER(12.4674, 0.4974, 2016) # 16-17

def qq_teamPER():
    """normal Q-Q plot for standardized residuals for each season
    standardized residuals come from ols_teamPER_winRatio()"""
    stand_residual_dict = ols_teamPER_winRatio()

    for each in range(2016, 2019):
        fig = sm.qqplot(stand_residual_dict['{}-{}'.format(each, each+1)], line='q', markersize=1)
        fig.suptitle('Normal Q-Q: {}-{}'.format(each, each+1))

    plt.show()

def future_test():
    df_teams = pd.read_csv('4_team_data_final.csv')

    # 2018 - 2019 Western
    west_teams = df_teams[(df_teams['Season']=='2018-2019') & (df_teams['Conference']=='Western')]
    y_18_west = list(west_teams['Win Ratio'])
    x_18_west = list(west_teams['Rk'])
    names_west = west_teams['Tm']

    # 2018-2019 Eastern
    east_teams = df_teams[(df_teams['Season']=='2018-2019') & (df_teams['Conference']=='Eastern')]
    y_18_east = list(east_teams['Win Ratio'])
    x_18_east = list(east_teams['Rk'])
    names_east = east_teams['Tm']

    rk = df_teams[df_teams['Season']=='2018-2019']['Rk']
    teamPER_pred = df_teams[df_teams['Season']=='2018-2019']['Team PER']

    winR_16_pred = []
    winR_17_pred = []

    for i in teamPER_pred:
        res = (i - 12.4674)/0.4974 # 2016
        winR_16_pred.append(res)
        res = (i - 12.4140)/0.5646 # 2017
        winR_17_pred.append(res)
    
    fig = plt.figure(figsize=(12, 8))
    ax = plt.subplot(111)
    ax.set_xmargin(0.05)
    ax.set_ymargin(0.05)

    plt.scatter(x_18_west, y_18_west, color='r', label='Western')
    plt.scatter(x_18_east, y_18_east, color='b', label='Eastern')
    plt.scatter(rk, winR_16_pred, color='c', label='2016 predicted')
    plt.scatter(rk, winR_17_pred, color='m', label='2017 predicted')
    plt.legend(loc="upper right")

    for i, txt in enumerate(names_west):
        ax.annotate(txt, (x_18_west[i]+0.05, y_18_west[i]), size=10)
    
    for i, txt in enumerate(names_east):
        ax.annotate(txt, (x_18_east[i]+0.05, y_18_east[i]), size=10)

    plt.title('2018-2019 Regular Season Prediction')
    plt.ylabel('Win Ratio (Games Won / Total Games)')
    plt.xlabel('Season Ranking')
    plt.tight_layout()
    plt.show()

future_test()










