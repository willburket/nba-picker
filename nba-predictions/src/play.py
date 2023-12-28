from helpers.stats.player_stats import *
from nba_api.stats.endpoints import PlayerNextNGames
from helpers.stats.team_stats import *
from helpers.stats.league_stats import *
import pandas as pd


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












