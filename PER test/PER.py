import pandas as pd 

def PERCalculation():
    df_players = pd.read_csv('BR_1999-2019-Regular-PlayerStats-edit.csv')
    df_teams = pd.read_csv('BR_1999-2019-Regular-TeamTotals-edit.csv')
    df_players = df_players[df_players['Season'] == '2018-2019']
    df_teams = df_teams[df_teams['Season'] == '2018-2019']

    # league totals and calculations
    lg_AST = df_players['AST'].sum()
    lg_FG = df_players['FG'].sum()
    lg_FT = df_players['FT'].sum()

    factor = (2 / 3) - (0.5 * (lg_AST / lg_FG)) / (2 * (lg_FG / lg_FT))
    
    lg_PTS = df_players['PTS'].sum()
    lg_FGA = df_players['FGA'].sum()
    lg_ORB = df_players['ORB'].sum()
    lg_TOV = df_players['TOV'].sum()
    lg_FTA = df_players['FTA'].sum()

    VOP = lg_PTS / (lg_FGA - lg_ORB + lg_TOV + 0.44 * lg_FTA)

    lg_TRB = df_players['TRB'].sum()
    
    DRB_perc  = (lg_TRB - lg_ORB) / lg_TRB

    # uPER variables and calculation
    names = df_players['Player']
    player_teams = df_players['Tm']
    MP = df_players['MP']
    player_3P = df_players['3P']
    AST = df_players['AST']
    FG = df_players['FG']
    FT = df_players['FT']
    TOV = df_players['TOV']
    FGA = df_players['FGA']
    FTA = df_players['FTA']
    TRB = df_players['TRB']
    ORB = df_players['ORB']
    STL = df_players['STL']
    BLK = df_players['BLK']
    PF = df_players['PF']

    # team variables
    unique_teams = list(set(df_players['Tm']))

    team_AST, team_FG, team_Pace = {}, {}, {}
    for each_team in unique_teams:
        team_AST[each_team] = sum(df_players[df_players['Tm'] == each_team]['AST'])
        team_FG[each_team] = sum(df_players[df_players['Tm'] == each_team]['FG'])
        team_Pace[each_team] = df_teams[each_team]['Pace']
        print(each_team, team_AST[each_team], team_FG[each_team], team_Pace[each_team])

    # league variables
    lg_FT = sum(df_players['FT'])
    lg_FTA = sum(df_players['FTA'])
    lg_PF = sum(df_players['PF'])

    team_tm = {
        'Atlanta Hawks': 'ATL'
        'Boston Celtics': 'BOS'
        'Brooklyn Nets': 'BRK'
        'Charlotte Hornets': 'CHI'
        'Chicago Bulls': 'CHO'
        'Cleveland Cavaliers': 'CLE'
        'Dallas Mavericks': 'DAL'
        'Denver Nuggets': 'DEN'
        'Detroit Pistons': 'DET'
        'Golden State Warriors': 'GSW'
        'Houston Rockets': 'HOU'
        'Indiana Pacers': 'IND'
        'Los Angeles Clippers': 'LAC'
        'Los Angeles Lakers': 'LAL'
        'Memphis Grizzlies': 'MEM'
        'Miami Heat': 'MIA'
        'Milwaukee Bucks': 'MIL'
        'Minnesota Timberwolves': 'MIN'
        'New Orleans Pelicans': 'NOP'
        'New York Knicks': 'NYK'
        'Oklahoma City Thunder': 'OKC'
        'Orlando Magic': 'ORL'
        'Philadelphia 76ers': 'PHI'
        'Phoenix Suns': 'PHO'
        'Portland Trail Blazers': 'POR'
        'Sacramento Kings': 'SAC'
        'San Antonio Spurs': 'SAS'
        'Toronto Raptors': 'TOR'
        'Utah Jazz': 'UTA'
        'Washington Wizards': 'WAS'
        'ATL': 'Atlanta Hawks'
        'BOS': 'Boston Celtics'
        'BRK': 'Brooklyn Nets'
        'CHI': 'Charlotte Hornets'
        'CHO': 'Chicago Bulls'
        'CLE': 'Cleveland Cavaliers'
        'DAL': 'Dallas Mavericks'
        'DEN': 'Denver Nuggets'
        'DET': 'Detroit Pistons'
        'GSW': 'Golden State Warriors'
        'HOU': 'Houston Rockets'
        'IND': 'Indiana Pacers'
        'LAC': 'Los Angeles Clippers'
        'LAL': 'Los Angeles Lakers'
        'MEM': 'Memphis Grizzlies'
        'MIA': 'Miami Heat'
        'MIL': 'Milwaukee Bucks'
        'MIN': 'Minnesota Timberwolves'
        'NOP': 'New Orleans Pelicans'
        'NYK': 'New York Knicks'
        'OKC': 'Oklahoma City Thunder'
        'ORL': 'Orlando Magic'
        'PHI': 'Philadelphia 76ers'
        'PHO': 'Phoenix Suns'
        'POR': 'Portland Trail Blazers'
        'SAC': 'Sacramento Kings'
        'SAS': 'San Antonio Spurs'
        'TOR': 'Toronto Raptors'
        'UTA': 'Utah Jazz'
        'WAS': 'Washington Wizards'
    }

    #Figure out way to use player team abb to link to team full team 
    print(df_teams[df_teams['Team'] == 'Atlanta Hawks']['Pace'])
    lg_Pace = sum(df_teams['Pace'])

    
    '''
    aPER_list = []
    # maybe DRB% is not league DRB? - see if calculations work first
    for each_name, each_player_team, each_MP, each_player_3P, each_AST, each_FG, each_FT, \
    each_TOV, each_FGA, each_FTA, each_TRB, each_ORB, each_STL, each_BLK, \
    each_PF in zip(names, player_teams, MP, player_3P, AST, FG, FT, TOV, FGA, FTA, TRB, ORB, \
    STL, BLK, PF): 

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

        pace_adj = lg_Pace / team_Pace[each_player_team]
        aPER = pace_adj * uPER
        aPER_list.append(aPER)

    # lg_aPER
    lg_aPER = sum(aPER_list)
    for each_aPER in aPER_list:
        PER = each_aPER * (15 / lg_aPER)

        print(each_name, PER)
        
    print('factor', factor)
    print('VOP', VOP)
    print('DRB%', DRB_perc)
    '''
PERCalculation()