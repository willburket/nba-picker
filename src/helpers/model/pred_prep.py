import pandas as pd
from ..injuries.scrape import *



def aggregate():

    preds = pd.read_csv('./data/upcoming_games.csv')
    stats = pd.read_csv('./data/next_game_incl.csv')
    agg_filepath = './data/aggregated_preds.csv'
    injuries = scrape()


    columns = ['team','opponent']


    df = pd.DataFrame(columns = columns)

    for x in range(len(preds)):
        id = preds['game_id'][x]
        team_id = preds['team_id'][x]
        row = stats[(stats['Game_ID'] == id) & (stats['Team_ID'] == team_id)]
        # df.loc[x,'game_id'] = id
        df.loc[x,'team'] = row['TEAM'].values[0]
        df.loc[x,'opponent'] = row['team_opp_next'].values[0]

        if preds['prediction'][x] == 1:
            winner = row['TEAM'].values[0]
        else:
            winner = row['team_opp_next'].values[0]

        df.loc[x,'winner'] = winner
        df.loc[x,'date'] = row['date_next'].values[0]
        df.loc[x,'home'] = row['home_next'].values[0]

    df.to_csv(agg_filepath, index=False)
    return

def addInjuries():
    return