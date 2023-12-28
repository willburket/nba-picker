from helpers.model.logistic_regression import *
from helpers.stats.league_stats import *
import pandas as pd

# run python3 prep.py after running build.py 

# file paths
stats_file = './data/21-23_adv.csv' # update 
rolling_file = './data/roll_data_incl.csv'
cleaned_file = './data/cleaned_data.csv'



# 3 clean data

cleanForML(stats_file)  # saves to cleaned_data.csv

# 4 add rolling data 
add_rolling_data(cleaned_file)    # saves to roll_data_incl.csv

# 5 add opponent data 
df = pd.read_csv(rolling_file)
add_opp_info(df)    # saves to opp_data_incl.csv

# 6 add in upcoming games (see play.py)
addOpponentInfo()                   # test when new games are out
