from helpers.stats.player_stats import *
from helpers.stats.team_stats import *
from nba_api.stats.endpoints import PlayerNextNGames
import pandas as pd
# from datetime import datetime

# Get the current date
# current_date = datetime.now()

team_names =['ATL','BOS','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU',
        'IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','BKN',
        'OKC','ORL','PHI','PHX','POR','SAC','TOR','UTA','SAS','WAS']

ordered_team_players = ['Trae Young', 'Jayson Tatum', 'Lamelo Ball', 'Coby White', 'Darius Garland', 'Luka Doncic', 
                        'Nikola Jokic', 'Cade Cunningham', 'Stephen Curry', 'Dillon Brooks', 'Tyrese Haliburton', 'Paul George',
                        'Lebron James', 'Ja Morant', 'Bam Adebayo', 'Giannis Antetokounmpo', 'Anthony Edwards', 'Brandon Ingram',
                        'Jalen Brunson', 'Mikal Bridges', 'Chet Holmgren', 'Paolo Banchero', 'Joel Embiid', 'Devin Booker', 'Shaedon Sharpe',
                        'Malik Monk', 'Pascal Siakam', 'Lauri Markkanen', 'Victor Wembanyama','Jordan Poole']

columns = ['Team_ID','Game_ID','GAME_DATE','TEAM','OPPONENT','WL','W','L','W_PCT','MIN','FGM','FGA',
            'FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','STL','BLK',
            'TOV','PF','PTS']

def getTeamIdArray():
    ids = []
    for name in team_names:
        id = getTeamId(name)
        ids.append(id)
    return ids

# def getTeamPlayersStats

def createDataframe():
    df = pd.DataFrame(columns = columns)
    return df

def getLeagueStats():
    df = createDataframe()
    ids = getTeamIdArray()

    for team in ids:
        # get player info
        roster = getTeamPlayers(team)
        players = roster['PLAYER_ID']
      
        # for player in players:
        player = players[0]
        logs = getPlayerGameLog(player,'2023')
        cleaned = cleanGamelog(logs)
        saveToCsv(cleaned)
    # get teamIdArray
    # for each id
        # get all players stats and add to df
    # clean df
    # save df to csv
    
def getAllGameLogs(year):
    df = createDataframe()
    ids = getTeamIdArray()
    for id in ids:
        logs = getTeamGamelog(id, year)
        cleaned = cleanTeamGameLog(logs)
        df = pd.concat([df, cleaned], ignore_index=True)
    df.dropna(subset=['WL'], inplace=True)
    df.insert(0,'INDEX',range(0, len(df)))
    indexed_gamelogs  = df.reset_index(drop = True)
    return indexed_gamelogs

def getMultipleSeasonGamelogs(years):
    df = createDataframe()
    ids = getTeamIdArray()
    for year in years:
        for id in ids:
            logs = getTeamGamelog(id, year)
            cleaned = cleanTeamGameLog(logs)
            df = pd.concat([df, cleaned], ignore_index=True)
    df.dropna(subset=['WL'], inplace=True)
    df.insert(0,'INDEX',range(0, len(df)))
    indexed_gamelogs  = df.reset_index(drop = True)
    return indexed_gamelogs
       
def addAdvancedStats(stats):
    # take existing stats, add columns
    # df = pd.read_csv('./data/game_data.csv')
    new_columns = ['E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING',
                   'NET_RATING','AST_PCT','AST_TOV','AST_RATIO','OREB_PCT','DREB_PCT',
                   'REB_PCT','E_TM_TOV_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','USG_PCT',
                   'E_USG_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE']
    for item in new_columns:
        stats[item] = None
    
    # for ind in stats.index:
    for ind in range(0,len(stats)):
        id = stats['Game_ID'][ind]
        # get advanced data for each game
        advanced = getTeamAdvancedBoxScore(id, stats['TEAM'][ind])
        # add proper columns to table
        print(advanced)


        for item in new_columns:
            # if advanced[item][1]:
            # stats[item][ind] = advanced[item][0]
            stats[item][ind] = advanced.iloc[0][item]
            # else:
            #     stats[item][ind] = advanced[item][0]

    return stats

def addAdvancedSave(stats):
   
    new_columns = ['E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING',
                   'NET_RATING','AST_PCT','AST_TOV','AST_RATIO','OREB_PCT','DREB_PCT',
                   'REB_PCT','E_TM_TOV_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','USG_PCT',
                   'E_USG_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE']
    
    adv_data_path = './data/21-23_adv.csv'  # update
    
    # for item in new_columns:        # delete if we already have some rows filled
    #     stats[item] = None

    stats['Game_ID'] = stats['Game_ID'].apply(str)
    
    # check dataframe for first row that has null value at e_off_rating
        # start for loop from that row's index

    for ind in range(5771,len(stats)):         # if we fail replace number with index
        id = stats['Game_ID'][ind]
        advanced = getTeamAdvancedBoxScore(id, stats['TEAM'][ind])
        print(advanced)


        for item in new_columns:
            stats[item][ind] = advanced.iloc[0][item]
       
        if ind % 10 == 0:
            stats.to_csv(adv_data_path, index=False)
    stats.to_csv(adv_data_path, index=False)
    
    return stats

def updateData(stats):

    ids = getTeamIdArray()
    # stats['Game_ID'] = stats['Game_ID'].apply(str)
    id_count = stats['Game_ID'].value_counts()
    id_offset = 0

    for id in ids:
        logs = getTeamGamelog(id, '2023')   # only need to update current year
        cleaned = cleanGamelogForUpdate(logs)

        for x in range(len(cleaned)):
            # if item game id is in stats less than 2 times 
            id = cleaned['Game_ID'][x]
            row = cleaned.iloc[x]


            if id in id_count.index:
                count = id_count.loc[id]
                if count < 2:
                    # row.insert(0,'INDEX',len(stats) + id_offset)
                    row['INDEX'] = len(stats) + id_offset

                    # stats = pd.concat([stats, row], ignore_index=True)
                    stats.loc[len(stats)] = row
                    id_offset += 1

                    print(row)
            else:
                # row.insert(0,'INDEX',len(stats) + id_offset)
                row['INDEX'] = len(stats) + id_offset

                # stats = pd.concat([stats, row], ignore_index=True)
                stats.loc[len(stats)] = row

                id_offset += 1
                
                print(row)
        
    stats.dropna(subset=['WL'], inplace=True)
    indexed_gamelogs  = stats.reset_index(drop = True)
    indexed_gamelogs['DATE'] = pd.to_datetime(indexed_gamelogs['DATE'])
    indexed_gamelogs['DATE'] = indexed_gamelogs['DATE'].dt.strftime('%Y-%m-%d')
    return indexed_gamelogs


def addAdvancedToEmptyRows(df):

    new_columns = ['E_OFF_RATING','OFF_RATING','E_DEF_RATING','DEF_RATING','E_NET_RATING',
                   'NET_RATING','AST_PCT','AST_TOV','AST_RATIO','OREB_PCT','DREB_PCT',
                   'REB_PCT','E_TM_TOV_PCT','TM_TOV_PCT','EFG_PCT','TS_PCT','USG_PCT',
                   'E_USG_PCT','E_PACE','PACE','PACE_PER40','POSS','PIE']
    
    adv_data_path = './data/21-23_adv.csv'  # update

    for ind in range(0,len(df)):         # if we fail replace number with index
        id = df['Game_ID'][ind]
        is_nan = pd.isna(df.at[ind, 'E_OFF_RATING'])


        if is_nan:
            advanced = getTeamAdvancedBoxScore(id, df['TEAM'][ind])
            print(advanced)

            for item in new_columns:
                df[item][ind] = advanced.iloc[0][item]
        
            if ind % 10 == 0:
                df.to_csv(adv_data_path, index=False)
    df.to_csv(adv_data_path, index=False)

    return df
           
        

def loadnewData():
    year = '2023'
    logs = getAllGameLogs(year)
    logs['Game_Num'] = logs['W'] + logs['L']
    # save logs to csv
    # filepath = './data/game_data.csv'
    # df = pd.read_csv(filepath)
    # advanced_logs = addAdvancedStats(logs)      # paginate to like 250 at a time
    
    # logs.to_csv(filepath, index=False)
    # saveToCsv(logs) 
    return logs

def getNextGame():
    next_game = {}
    deleted_columns =['HOME_TEAM_NICKNAME', 'VISITOR_TEAM_NICKNAME', 'GAME_TIME', 'HOME_WL', 'VISITOR_WL', 'HOME_TEAM_NAME', 'AWAY_TEAM_NAME']

    # next_games = {key: None for key in team_names}
    for key, value in zip(team_names, ordered_team_players):
        id = getPlayerId(value)
        games = PlayerNextNGames(number_of_games=1, player_id=id)
        df = games.get_data_frames()[0]
        selected_columns = df.columns[~df.columns.isin(deleted_columns)]
        next_game[key] = df[selected_columns]
        next_game[key]['GAME_DATE'] = pd.to_datetime(next_game[key]['GAME_DATE'], format='%b %d, %Y')


    return next_game

def addOpponentInfo():
    next_games = getNextGame()
    next_game_path = './data/next_game_incl.csv'

    stats = pd.read_csv('./data/opp_data_incl.csv')

    last_games = []

    for ind in range(0,len(stats)):
        is_empty = pd.isna(stats.loc[ind, 'date_next'])
        if is_empty:

            last_games.append(ind)

    print(last_games)

    for idx in last_games:
        team = stats['TEAM'][idx]

        stats['date_next'][idx] = next_games[team]['GAME_DATE'][0].strftime('%Y-%m-%d')

        if next_games[team]['HOME_TEAM_ABBREVIATION'][0] == team:
            stats['team_opp_next'][idx] = next_games[team]['VISITOR_TEAM_ABBREVIATION'][0]
            stats['home_next'][idx] = True
        else:
            stats['team_opp_next'][idx] = next_games[team]['HOME_TEAM_ABBREVIATION'][0]
            stats['home_next'][idx] = False
    stats.to_csv(next_game_path, index=False)
    return