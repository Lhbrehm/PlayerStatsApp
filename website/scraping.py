import re
from bs4 import BeautifulSoup
import requests

url = "https://www.pro-football-reference.com/leaders/rush_yds_career.htm"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

rows = doc.select('tbody tr')

players = []

# print("____________________________")



for row in rows[:5]:
    rank = row.select_one('th[data-stat="rank"]').text.strip()
    name = row.select_one('td[data-stat="player"] a').text.strip()
    yards = row.select_one('td[data-stat="rush_yds"]').text.strip()
    years = row.select_one('td[data-stat="years"]').text.strip()
    team = row.select_one('td[data-stat="team"]').text.strip()

    player_data = {'Rank': rank, 'Name': name, 'Yards': yards, 'Years': years, 'Team': team}
    players.append(player_data)

    # print(rank, name, yards, years, team)
    # print("____________________________")

def scrape():
    return players