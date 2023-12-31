import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.fantasynerds.com/nba/injuries'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

teams = {
    'Atlanta Hawks Injuries': 'ATL',
    'Brooklyn Nets Injuries': 'BKN',
    'Boston Celtics Injuries': 'BOS',
    'Charlotte Hornets Injuries': 'CHA',
    'Chicago Bulls Injuries': 'CHI',
    'Cleveland Cavaliers Injuries': 'CLE',
    'Dallas Mavericks Injuries': 'DAL',
    'Denver Nuggets Injuries': 'DEN',
    'Detroit Pistons Injuries': 'DET',
    'Golden State Warriors Injuries': 'GSW',
    'Houston Rockets Injuries': 'HOU',
    'Indiana Pacers Injuries':'IND',
    'Los Angeles Clippers Injuries':'LAC',
    'Los Angeles Lakers Injuries':'LAL',
    'Memphis Grizzlies Injuries':'MEM',
    'Miami Heat Injuries':'MIA',
    'Milwaukee Bucks Injuries':'MIL',
    'Minnesota Timberwolves Injuries':'MIN',
    'New Orleans Pelicans Injuries':'NOP',
    'New York Knicks Injuries':'NYK',
    'Oklahoma City Thunder Injuries':'OKC',
    'Orlando Magic Injuries':'ORL',
    'Philadelphia Sixers Injuries':'PHI',
    'Phoenix Suns Injuries':'PHX',
    'Portland Trail Blazers Injuries':'POR',
    'Sacramento Kings Injuries':'SAC',
    'Toronto Raptors Injuries':'TOR',
    'Utah Jazz Injuries':'UTA',
    'San Antonio Spurs Injuries':'SAS',
    'Washington Wizards Injuries':'WAS',
}

injuries = {}

def scrape():
    data = []
    cleaned = []

    results = soup.find_all("div", class_="pad")

    for element in results:
        text = element.text
        text = text.split('\n')
        data.append(text)
    

    for item in data[0]:
        if item == '' or item == 'Player' or item == 'Injury' or item == 'Notes' or item == ' ':
            continue
        else:
            item = item.strip()
            cleaned.append(item)

    # loop through cleaned 
    x = 0
    while x < len(cleaned):
        if cleaned[x] in teams.keys():
            injuries[teams[cleaned[x]]] = []
            last = teams[cleaned[x]]
        else: 
            inj = []
            for i in range(3):
                inj.append(cleaned[x + i])
            injuries[last].append(inj)
            x += 2

        x += 1


    return injuries

injuries = scrape()
file = '../../data/injuries.json'
with open(file, 'w') as json_file:
    json.dump(injuries, json_file, indent=2)
# print(injuries)