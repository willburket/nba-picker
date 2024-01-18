from helpers.model.logistic_regression import * 
from sklearn.model_selection import TimeSeriesSplit
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import RidgeClassifier
from helpers.model.pred_prep import *
import pandas as pd


# activate virtual environment: source nba-predictor/bin/activate

# run download.py to get data for the first time 

# run update.py to update data
# run prep.py to prep data
# run main.py to get predictions/acc score
# run aggregate.py to get a full prediction csv     # should run in main, test tomorrow


# set up
removed_columns = ['INDEX','Team_ID', 'Game_ID', 'GAME_DATE', 'TEAM', 'OPPONENT',
                       'WL', 'W', 'L', 'target', 'MIN', 'Game_Num', 'HOME', 'DATE', 'Unnamed: 0']   

rolling_cols =['W_PCT_10','FGM_10','FGA_10','FG_PCT_10','FG3M_10','FG3A_10','FG3_PCT_10','FTM_10','FTA_10','FT_PCT_10',
               'OREB_10','DREB_10','REB_10','AST_10','STL_10','BLK_10','TOV_10','PF_10','PTS_10','E_OFF_RATING_10',
               'OFF_RATING_10','E_DEF_RATING_10','DEF_RATING_10','E_NET_RATING_10','NET_RATING_10','AST_PCT_10',
               'AST_TOV_10','AST_RATIO_10','OREB_PCT_10','DREB_PCT_10','REB_PCT_10','E_TM_TOV_PCT_10','TM_TOV_PCT_10',
               'EFG_PCT_10','TS_PCT_10','USG_PCT_10','E_USG_PCT_10','E_PACE_10','PACE_10','PACE_PER40_10','POSS_10','PIE_10','WL_10']

rr = RidgeClassifier(alpha=1)
split = TimeSeriesSplit(n_splits=3)
sfs = SequentialFeatureSelector(rr, n_features_to_select=30, direction='forward', cv = split)

df = pd.read_csv('./data/next_game_incl.csv')

# include opponents 10 game rolling avg's 
full = df.merge(df[rolling_cols + ["team_opp_next", "date_next", "TEAM"]], left_on=["TEAM", "date_next"], right_on=["team_opp_next", "date_next"])
removed_columns = list(full.columns[full.dtypes == 'object']) + removed_columns
selected_columns = full.columns[~full.columns.isin(removed_columns)]
print(selected_columns)
sfs.fit(full[selected_columns],full["target"])

# predictions 
predictors = list(selected_columns[sfs.get_support()])
predictions = backTest(full,rr,predictors)

# get future predictions
upcoming_games = predictions[predictions['actual'] == 2]
upcoming_games.to_csv('./data/upcoming_games.csv', index=False)

# check accuracy 
acc = accuracy_score(predictions['actual'], predictions['prediction'])
print(acc)

# aggregate prediction data 
aggregate()     # test tomorrow
