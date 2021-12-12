import requests
import pandas as pd
import time
import Team

finalDataFrame = pd.DataFrame

for team in Team.teams:
    teamAbbr, teamName = team.split("/")

    url = "https://www.cbssports.com/nhl/teams/" + team + "/stats/regular/"
    html = requests.get(url).content

    data = pd.read_html(html)
    dataframe = data[-2]
    fileName = "./TeamData/" + teamName + ".csv"
    dataframe.to_csv(fileName)
    time.sleep(.2)

print("Collection Completed")
