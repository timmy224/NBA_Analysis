import pandas as pd
import statistics 

# Iterates through 1998 to 2019 player data
# Basketball reference scraped data differs from ESPN data
# Team pace is different
def PERCalculation():
    """ Calculates Hollinger's Player Efficiency Rating
    Input: None (hardcoded filename)
    Output: CSV file
    """
    df_players = pd.read_csv('BR_1998-2019-Regular-PlayerStats-edit.csv', index_col=0)
    df_teams = pd.read_csv('BR_1998-2019-Regular-TeamTotals-edit.csv')

    PER_list = []

    for i in range(1998, 2019):
        df_players_inst = df_players[df_players['Season'] == '{}-{}'.format(i, i+1)]
        df_teams_inst = df_teams[df_teams['Season'] == '{}-{}'.format(i, i+1)]

        # league totals and calculations
        lg_AST = df_players_inst['AST'].mean()
        lg_FG = df_players_inst['FG'].mean()
        lg_FT = df_players_inst['FT'].mean()

        factor = (2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT))
        
        lg_PTS = df_players_inst['PTS'].mean()
        lg_FGA = df_players_inst['FGA'].mean()
        lg_ORB = df_players_inst['ORB'].mean()
        lg_TOV = df_players_inst['TOV'].mean()
        lg_FTA = df_players_inst['FTA'].mean()

        VOP = lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA)

        lg_TRB = df_players_inst['TRB'].mean()
        
        DRB_perc  = (lg_TRB - lg_ORB) / lg_TRB

        # uPER variables and calculation
        names = df_players_inst['Player']
        player_teams = df_players_inst['Tm']
        MP = df_players_inst['MP']
        player_3P = df_players_inst['3P']
        AST = df_players_inst['AST']
        FG = df_players_inst['FG']
        FT = df_players_inst['FT']
        TOV = df_players_inst['TOV']
        FGA = df_players_inst['FGA']
        FTA = df_players_inst['FTA']
        TRB = df_players_inst['TRB']
        ORB = df_players_inst['ORB']
        STL = df_players_inst['STL']
        BLK = df_players_inst['BLK']
        PF = df_players_inst['PF']

        # team variables
        unique_teams = list(set(df_players_inst['Tm']))

        # 2-way dict used to convert full team name to abbreviation and vice-versa
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
        for each_team, season in zip(df_teams_inst['Team'], df_teams_inst['Season']):
            if each_team == 'Charlotte Hornets':
                if season in CHH_season:
                    tm_list.append(team_tm['Charlotte Hornets'][0])
                else: 
                    tm_list.append(team_tm['Charlotte Hornets'][1])
            else:
                tm_list.append(team_tm[each_team])
        df_teams_inst.insert(4, 'Tm', tm_list)


        team_AST, team_FG, team_Pace = {}, {}, {}
        for each_team in unique_teams:
            team_AST[each_team] = df_players_inst[df_players_inst['Tm'] == each_team]['AST'].mean()
            team_FG[each_team] = df_players_inst[df_players_inst['Tm'] == each_team]['FG'].mean()
            team_Pace[each_team] = df_teams_inst[df_teams_inst['Tm'] == each_team]['Pace']
            #print(each_team, team_AST[each_team], team_FG[each_team], team_Pace[each_team])
        
        # league variables
        lg_FT = df_players_inst['FT'].mean()
        lg_FTA = df_players_inst['FTA'].mean()
        lg_PF = df_players_inst['PF'].mean()
        
        #Figure out way to use player team abb to link to team full team 
        lg_Pace = df_teams_inst['Pace'].mean()
        
        aPER_list = []
        # maybe DRB% is not league DRB? - see if calculations work first
        for each_name, each_player_team, each_MP, each_player_3P, each_AST, each_FG, each_FT, \
        each_TOV, each_FGA, each_FTA, each_TRB, each_ORB, each_STL, each_BLK, \
        each_PF in zip(names, player_teams, MP, player_3P, AST, FG, FT, TOV, FGA, FTA, TRB, ORB, \
        STL, BLK, PF): 

            try:
                uPER = (1 / each_MP) * \
                    (each_player_3P \
                    + (2/3) * each_AST + (2 - factor \
                    * (team_AST[each_player_team] / team_FG[each_player_team])) \
                    * each_FG + (each_FT * 0.5 * (1 + (1 - (team_AST[each_player_team] \
                    / team_FG[each_player_team])) + (2/3) 
                    * (team_AST[each_player_team] / team_FG[each_player_team]))) \
                    - VOP * each_TOV \
                    - VOP * DRB_perc * (each_FGA - each_FG) \
                    - VOP * 0.44 * (0.44 + (0.56 * DRB_perc)) * (each_FTA - each_FT) \
                    + VOP * (1 - DRB_perc) * (each_TRB - each_ORB) \
                    + VOP * DRB_perc * each_ORB \
                    + VOP * each_STL \
                    + VOP * DRB_perc * each_BLK \
                    - each_PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP))
            except ZeroDivisionError:
                uPER = 0

            pace_adj = lg_Pace / team_Pace[each_player_team].values
            aPER = pace_adj * uPER
            aPER_list.append(aPER.item())
            #print(each_name, aPER)
            
        # lg_aPER
        lg_aPER = statistics.mean(aPER_list)

        for each_name, each_aPER in zip(names, aPER_list):
            PER = each_aPER * (15 / lg_aPER)
            PER_list.append(PER)

    df_players.insert(6, 'PER_calc', PER_list)
    #print(df_players)
    df_players.to_csv('PER_Calc.csv')
    
PERCalculation()