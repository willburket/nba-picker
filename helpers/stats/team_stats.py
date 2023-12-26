from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamGameLog, CommonTeamRoster;
from nba_api.stats.endpoints import BoxScoreScoringV2
from nba_api.stats.endpoints import BoxScoreAdvancedV2

from .player_stats import *
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# hornets id = 1610612766
def getTeamId(team_abbreviation):
    team = teams.find_team_by_abbreviation(team_abbreviation)
    return team['id']

def getTeamPlayers(id):
    roster = CommonTeamRoster(team_id=id)
    df_roster = roster.get_data_frames()[0]
    return df_roster

def getTeamPlayersByPosition(team_id,position):
    roster = CommonTeamRoster(team_id=team_id)
    df_roster = roster.get_data_frames()[0]
    condition = df_roster['POSITION'] == position
    position_list = df_roster[condition]
    return position_list

def getTeamGamelog(id):
    logs = TeamGameLog(team_id = id)
    df_logs = logs.get_data_frames()
    return df_logs[0]

def getTeamPlayerBoxScores(game_id):
    scores = BoxScoreScoringV2(game_id=game_id)
    df_scores = scores.get_data_frames()
    return df_scores

def getTeamPlayersGameLogs(team_id):
    players = getTeamPlayers(team_id)
    # df = pd.DataFrame()

    for player in players['PLAYER_ID']:
        logs = getPlayerGameLog(player, '2023')
        print(logs)
        # cleaned_gamelogs = cleanGamelog(logs)
        # df = df.append

def getTeamAdvancedBoxScore(game_id, team):
    score = BoxScoreAdvancedV2(game_id=game_id)
    df_scores = score.get_data_frames()[1]          # set to 0 for player stats
    # print(df_scores)
    condition = df_scores['TEAM_ABBREVIATION'] == team 
    adv_box_score = df_scores[condition]
    return adv_box_score



def cleanTeamGameLog(gamelog):
    length = len(gamelog)
    ordered_log = gamelog[::-1]
    
    ordered_log['TEAM'] = ordered_log['MATCHUP'].str[:3]
    ordered_log['OPPONENT'] = ordered_log['MATCHUP'].str[-3:]
    ordered_log['HOME'] = ordered_log['MATCHUP'].str[4] != '@'
    ordered_log['DATE'] = pd.to_datetime(ordered_log['GAME_DATE'], format='%b %d, %Y')

    cleaned_log = ordered_log[['Team_ID','Game_ID','DATE','GAME_DATE','TEAM','OPPONENT','HOME','WL','W','L','W_PCT','MIN','FGM','FGA',
                               'FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','STL','BLK',
                               'TOV','PF','PTS']]
    return cleaned_log

def buildLeagueCsv():  # move later
    # get all teams gamelogs 
    # add advanced stats to df
    # add defensive stats, etc    
    pass









