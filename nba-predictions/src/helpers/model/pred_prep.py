import pandas as pd
from ..injuries.scrape import *



def aggregate():

    preds = pd.read_csv('./data/upcoming_games.csv')
    stats = pd.read_csv('./data/next_game_incl.csv')
    agg_filepath = './data/aggregated_preds.csv'
    injuries = scrape()


    columns = ['game_id','team','opponent']


    df = pd.DataFrame(columns = columns)

    for x in range(len(preds)):
        id = preds['game_id'][x]
        team_id = preds['team_id'][x]
        row = stats[(stats['Game_ID'] == id) & (stats['Team_ID'] == team_id)]
        df.loc[x,'game_id'] = id
        df.loc[x,'team'] = row['TEAM'].values[0]
        df.loc[x,'opponent'] = row['team_opp_next'].values[0]

        if preds['prediction'][x] == 1:
            winner = row['TEAM'].values[0]
        else:
            winner = row['team_opp_next'].values[0]

        df.loc[x,'winner'] = winner

        # if row['TEAM'].values[0] in injuries.keys():
        #     df.loc[x,'team_injuries'] = injuries[row['TEAM'].values[0]]
        # if row['team_opp_next'].values[0] in injuries.keys():
        #     df.loc[x,'opp_injuries'] = injuries[row['team_opp_next'].values[0]]
    obj = df.to_json(orient='records')

    for item in obj:
        if item["team"] in injuries.keys():
            item["team_injuries"] = injuries[item["team"]]
        else:
            item["team_injuries"] = None
        if item["opponent"] in injuries.keys():
            item["opp_injuries"] = injuries[item["opponent"]]
        else:
            item["opp_injuries"] = None
            

    print(obj)
    # only show the next day of games? 
    df.to_csv(agg_filepath, index=False)
    return

def addInjuries():
    return