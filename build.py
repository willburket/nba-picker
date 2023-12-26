from helpers.stats.league_stats import *

standard_data_path = './data/game_data.csv'
adv_data_path = './data/adv_data_incl.csv'



# run python3 build.py to download most up to date stats as csv

# 1 download stats 
stats = loadnewData()
stats.to_csv(standard_data_path, index=False)

# 2 add advanced stats
advanced_included = addAdvancedStats(stats)
advanced_included.to_csv(adv_data_path, index=False)

# need to add a way for this to just add new games 


