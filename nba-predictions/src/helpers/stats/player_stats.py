from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playervsplayer
from nba_api.stats.endpoints import playercompare

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# '2544' = lebron james player id for testing 

def getPlayerId(full_name):
    player = players.find_players_by_full_name(full_name)[0]
    return player['id'] 

def getPlayerStats(id):
    # career = id 
    career = playercareerstats.PlayerCareerStats(player_id=id)
    dataFrame = career.get_data_frames()[0]
    return dataFrame

def getPlayerGameLog(playerId, year):
    gamelog = playergamelog.PlayerGameLog(player_id=playerId, season = year)
    df_gamelog = gamelog.get_data_frames()
    return df_gamelog[0]

def getPlayerVsPlayer(playerId,opponentId):
    pvp = playervsplayer.PlayerVsPlayer(player_id=playerId, vs_player_id=opponentId)
    df_pvp = pvp.get_data_frames()
    return df_pvp

def playerCompare(id_list,vs_id_list):
    compare = playercompare.PlayerCompare(player_id_list=id_list, vs_player_id_list=vs_id_list)
    df_compare = compare.get_data_frames()
    return df_compare

def cleanGamelog(gamelog):
    length = len(gamelog)
    del gamelog['VIDEO_AVAILABLE']
    chrono_gamelog = gamelog[::-1]
    chrono_gamelog['INDEX'] = range(0, length)
    chrono_gamelog['TEAM'] = chrono_gamelog['MATCHUP'].str[:3]
    chrono_gamelog['OPPONENT'] = chrono_gamelog['MATCHUP'].str[-3:]
    # reset index 
    data = chrono_gamelog[['INDEX', 'SEASON_ID', 'Player_ID', 'TEAM','OPPONENT','Game_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'PTS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT','OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']]
    data = data.reset_index(drop = True)
    return data

def getPlayerVsTeam(player_id, team_abbreviation, year):
    
    pass

def saveToCsv(data):
    file_path = './data/game_data2.csv'
    data.to_csv(file_path, index=False)

def test():
    return 'test passed'









