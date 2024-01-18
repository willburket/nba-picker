from flask import Flask, jsonify, request
from helpers.injuries.scrape import *
from helpers.stats.team_stats import *
from flask_cors import CORS
from datetime import datetime
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/injuries')
def injuries():
    # how often do we need to scrape? 
    # scrape every time or just every hour or so? 
    data = scrape()

    for item in data.keys():
        players = []
        for x in data[item]:
            player = {
                "name": x[0],
                "injury": x[1],
                "status": x[2],
            }
            players.append(player)
        data[item] = players
    return jsonify(data)

@app.route('/update')
def update():
    #### only need to update once per day
    # try 
        # update 
        # prep
        # predict and save (to s3)
    # catch 
        # retry? 
    return

@app.route('/predictions')
def getPredictions():
    # get predictions from s3 

    # get from csv for now
    df = pd.read_csv('data/aggregated_preds.csv')  #change to csv from s3 bucket
    df['date'] = pd.to_datetime(df['date'])
    current_date = datetime.now().strftime('%Y-%m-%d')
    filtered_df = df[df['date'] == current_date]
    filtered_df['date'] = filtered_df['date'].dt.strftime('%Y-%m-%d')
    json_data = filtered_df.to_json(orient='records')

    return json_data

@app.route('/stats/<team>')
def getStats(team):
    id = getTeamId(team)
    logs = getTeamGamelog(id, '2023')
    cleaned = cleanTeamGameLog(logs)
    json_logs = cleaned.to_json(orient='records')
    json_objects = json.loads(json_logs)
    last_ten = json_objects[-10:]
    return last_ten

if __name__ == '__main__':
    app.run(debug=True)
