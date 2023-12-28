import pandas as pd

preds = pd.read_csv('./data/upcoming_games.csv')
stats = pd.read_csv('./data/next_game_incl.csv')
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


df.to_csv('./data/aggregated_preds.csv', index=False)