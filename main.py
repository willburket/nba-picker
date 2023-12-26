from helpers.model.logistic_regression import * 
from sklearn.model_selection import TimeSeriesSplit
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import RidgeClassifier
import pandas as pd

# run build.py to get data 
# run prep.py to prep data
# run main.py to get predictions/acc score

# set up
removed_columns = ['INDEX','Team_ID', 'Game_ID', 'GAME_DATE', 'TEAM', 'OPPONENT',
                       'WL', 'W', 'L', 'target', 'MIN', 'Game_Num', 'HOME', 'DATE']   
rolling_cols =['W_PCT_5','FGM_5','FGA_5','FG_PCT_5','FG3M_5','FG3A_5','FG3_PCT_5','FTM_5','FTA_5','FT_PCT_5',
               'OREB_5','DREB_5','REB_5','AST_5','STL_5','BLK_5','TOV_5','PF_5','PTS_5','E_OFF_RATING_5',
               'OFF_RATING_5','E_DEF_RATING_5','DEF_RATING_5','E_NET_RATING_5','NET_RATING_5','AST_PCT_5',
               'AST_TOV_5','AST_RATIO_5','OREB_PCT_5','DREB_PCT_5','REB_PCT_5','E_TM_TOV_PCT_5','TM_TOV_PCT_5',
               'EFG_PCT_5','TS_PCT_5','USG_PCT_5','E_USG_PCT_5','E_PACE_5','PACE_5','PACE_PER40_5','POSS_5','PIE_5','WL_5']

rr = RidgeClassifier(alpha=1)
split = TimeSeriesSplit(n_splits=3)
sfs = SequentialFeatureSelector(rr, n_features_to_select=30, direction='forward', cv = split)

# df = pd.read_csv('./data/opp_data_incl.csv')
df = pd.read_csv('./data/next_game_incl.csv')


# include opponents 5 game rolling avg's 
full = df.merge(df[rolling_cols + ["team_opp_next", "date_next", "TEAM"]], left_on=["TEAM", "date_next"], right_on=["team_opp_next", "date_next"])
removed_columns = list(full.columns[full.dtypes == 'object']) + removed_columns
selected_columns = full.columns[~full.columns.isin(removed_columns)]
sfs.fit(full[selected_columns],full["target"])

# add in next game data on rows with null (most recent games)


# predictions 
predictors = list(selected_columns[sfs.get_support()])
predictions = backTest(full,rr,predictors)

if predictions['actual'] == 2:
    print 
predictions.to_csv('./data/predictions.csv', index=False)

# check accuracy 
acc = accuracy_score(predictions['actual'], predictions['prediction'])
print(acc)
