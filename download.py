from nba_api.stats.endpoints import TeamGameLog
from nba_api.stats.static import teams
from helpers.stats.league_stats import *
import pandas as pd

# download all data for prior seasons, use if no data is downloaded yet

# step 1
seasons = ['2021','2022','2023']
logs = getMultipleSeasonGamelogs(seasons)
logs['Game_Num'] = logs['W'] + logs['L']

logs.to_csv('./data/21-23_logs.csv', index=False)

# step 2

logs = pd.read_csv('./data/21-23_logs.csv', dtype={'Game_ID': str})  

advanced_included = addAdvancedSave(logs)   # saves to './data/21-23_adv.csv'


