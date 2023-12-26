import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import RidgeClassifier
from sklearn.preprocessing import MinMaxScaler

from sklearn.metrics import accuracy_score

removed_columns = ['INDEX','Team_ID', 'Game_ID', 'GAME_DATE', 'TEAM', 'OPPONENT',
                       'WL', 'W', 'L', 'target', 'MIN', 'Game_Num', 'HOME', 'DATE']   

def add_target(team):
    team["target"] = team["WL"].shift(-1)      # can update to points or something
    return team

def cleanForML(file):
    # df = pd.read_csv('./data/game_data.csv')        # filepath

    df = pd.read_csv(file)
    df = df.groupby("TEAM", group_keys=False).apply(add_target)
    # df["target"] = df["target"].astype(int, errors="ignore")
    target_map = {'W': '1', 'L': '0', '2': '2'}
    df["target"] = df["target"].map(target_map)
    df["target"][pd.isnull(df["target"])] = 2
    df = df.dropna()    

    file_path = './data/cleaned_data.csv'
    df.to_csv(file_path, index=False)
    return

def checkForNull(file):
    df = pd.read_csv(file)        # data after advanced download
    # count = df["WL"].value_counts()
    # count = df["target"].value_counts()
    nulls = pd.isnull(df)
    count = nulls.sum()
    print(count)
    return

def getPredictors(file):
    df = pd.read_csv(file)        # ml data after cleaning

    rr = RidgeClassifier(alpha=1)
    split = TimeSeriesSplit(n_splits=3)
    sfs = SequentialFeatureSelector(rr, n_features_to_select=30, direction='forward', cv = split)
    # removed_columns = ['INDEX','Team_ID', 'Game_ID', 'GAME_DATE', 'TEAM', 'OPPONENT',
    #                    'WL', 'W', 'L', 'target', 'MIN', 'Game_Num']            
    selected_columns = df.columns[~df.columns.isin(removed_columns)]
    scaler = MinMaxScaler()
    df[selected_columns] = scaler.fit_transform(df[selected_columns])
    # file_path = './data/prepped_data.csv'
    # df.to_csv(file_path, index=False)
    sfs.fit(df[selected_columns], df["target"])
    predictors = list(selected_columns[sfs.get_support()])
    return predictors

def backTest(data, model, predictors, start=2, step=1):
    all_predictons = []
    games = sorted(data["Game_Num"].unique())

    for i in range(start, 25, step):        # 25 is the number of games we're looking at 
        game = games[i]
        train = data[data["Game_Num"] < game]
        test = data[data["Game_Num"] == game]

        model.fit(train[predictors], train["target"])
        preds = model.predict(test[predictors])
        preds = pd.Series(preds, index=test.index)

        combined = pd.concat([test["target"], preds], axis=1)
        combined.columns = ["actual", "prediction"]
        all_predictons.append(combined)
    return pd.concat(all_predictons)

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
    df_rolling = df[list(selected_columns) + ["WL", "Team_ID", "Game_Num"]]
    return df_rolling

def find_team_averages(team):
    rolling = team.rolling(5).mean()
    return rolling

def add_rolling_data(filepath):
    df = pd.read_csv(filepath)
    for ind in range(0,len(df)):
        if df['WL'][ind] == 'W':
            df['WL'][ind] = True
        else:
            df['WL'][ind] = False
    df_rolling = get_rolling(df).astype(float)
    df_rolling = df_rolling.groupby(["Team_ID"], group_keys=False)
    df_rolling = df_rolling.apply(find_team_averages)
    rolling_cols = [f"{col}_5" for col in df_rolling.columns]
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
