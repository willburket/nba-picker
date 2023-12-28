from helpers.stats.league_stats import *
import pandas as pd
# run if you already have an existing csv 
# will just add new game data 

# read df from csv 
df = pd.read_csv('./data/21-23_adv.csv', dtype={'Game_ID': str})       # read from adv data

# # download new games 
stats = updateData(df)
stats['Game_Num'] = stats['W'] + stats['L']

stats.to_csv('./data/21-23_adv.csv', index=False)
# download new adv data
# stats = pd.read_csv('./data/test.csv', dtype={'Game_ID': str})       # read from adv data
addAdvancedToEmptyRows(stats)




 
