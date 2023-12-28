import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import RidgeClassifier
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from sklearn.metrics import accuracy_score
pd.options.mode.chained_assignment = None  # default='warn'


removed_columns = ['INDEX','Team_ID', 'Game_ID', 'GAME_DATE', 'TEAM', 'OPPONENT',
                       'WL', 'W', 'L', 'target', 'MIN', 'Game_Num', 'HOME', 'DATE', 
                       'season']   

def add_target(team):
    team["target"] = team["WL"].shift(-1)      # can update to points or something
    return team

def cleanForML(file):
    df = pd.read_csv(file)
    # add season column 
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
    conditions = [
        (df['DATE'] < pd.Timestamp('2022-08-1')),
        (df['DATE'] < pd.Timestamp('2023-08-1')),
        (df['DATE'] < pd.Timestamp('2024-08-1'))
    ]
    values = ['2021', '2022', '2023']

    # Add the 'Season' column based on the conditions
    df['season'] = pd.Series(np.select(conditions, values, default=''), dtype='str')

    df = df.groupby("TEAM", group_keys=False).apply(add_target)
    target_map = {'W': '1', 'L': '0', '2': '2'}
    df["target"] = df["target"].map(target_map)
    df["target"][pd.isnull(df["target"])] = 2
    df = df.dropna()    

    file_path = './data/cleaned_data.csv'
    df.to_csv(file_path, index=False)
    return

def checkForNull(file):
    df = pd.read_csv(file)        # data after advanced download
    nulls = pd.isnull(df)
    count = nulls.sum()
    print(count)
    return

def getPredictors(file):
    df = pd.read_csv(file)        # ml data after cleaning

    rr = RidgeClassifier(alpha=1)
    split = TimeSeriesSplit(n_splits=3)
    sfs = SequentialFeatureSelector(rr, n_features_to_select=30, direction='forward', cv = split)
         
    selected_columns = df.columns[~df.columns.isin(removed_columns)]
    scaler = MinMaxScaler()
    df[selected_columns] = scaler.fit_transform(df[selected_columns])

    sfs.fit(df[selected_columns], df["target"])
    predictors = list(selected_columns[sfs.get_support()])
    return predictors

def backTest(data, model, predictors, start=1, step=1):
    all_predictions = []
    
    seasons = sorted(data["season"].unique())
    
    for i in range(start, len(seasons), step):
        season = seasons[i]
        train = data[data["season"] < season]
        test = data[data["season"] == season]
        
        model.fit(train[predictors], train["target"])
        
        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index=test.index)
        combined = pd.concat([test["target"], preds], axis=1)
        combined.columns = ["actual", "prediction"]
        combined['game_id'] = data.loc[test.index, 'Game_ID'].values
        combined['team_id'] = data.loc[test.index, 'Team_ID'].values
        # combined['team'] = data.loc[test.index, 'TEAM'].values


        all_predictions.append(combined)
        result = pd.concat(all_predictions)
    return result


def getPredictions(filepath):
    df = pd.read_csv(filepath)
    rr = RidgeClassifier(alpha=1)
    predictors = getPredictors(filepath)
    predictions = backTest(df, rr, predictors)
    return predictions

def getAccuracyScore(predictions):
    predictions = predictions[predictions['actual'] != 2]
    score = accuracy_score(predictions["actual"], predictions["prediction"])
    return score 

def get_rolling(df):
    selected_columns = df.columns[~df.columns.isin(removed_columns)]
    df_rolling = df[list(selected_columns) + ["WL", "Team_ID", "season"]]
    return df_rolling

def find_team_averages(team):
    rolling = team.rolling(10).mean()
    return rolling

def add_rolling_data(filepath):
    df = pd.read_csv(filepath, dtype={'season': str})
    for ind in range(0,len(df)):
        if df['WL'][ind] == 'W':
            df['WL'][ind] = True
        else:
            df['WL'][ind] = False
    df_rolling = get_rolling(df)
 
    df_rolling = df_rolling.groupby(["Team_ID","season"], group_keys=False).apply(find_team_averages)

    rolling_cols = [f"{col}_10" for col in df_rolling.columns]
    df_rolling.columns = rolling_cols
    df = pd.concat([df, df_rolling], axis=1)
    df = df.dropna()
    df.to_csv('./data/roll_data_incl.csv')
    return

def shift_col(team, col_name):
    next_col = team[col_name].shift(-1)
    return next_col

def add_col(df, col_name):
    return df.groupby("TEAM", group_keys=False).apply(lambda x: shift_col(x,col_name))

def add_opp_info(df):
    df["home_next"] = add_col(df,"HOME")
    df["team_opp_next"] = add_col(df,"OPPONENT")
    df["date_next"] = add_col(df,"DATE")
    df.to_csv('./data/opp_data_incl.csv', index=False)
    return
