# 0.533653 + 0.204405(GPG) - 0.204638*(GAPG) - 0.009540*(SOGPG) + 0.008496*(SOGAPG)
import csv

class TeamData:
    GPG = 0.0
    GAPG = 0.0
    SOGPG = 0.0
    SOGAPG = 0.0


def PredictedWinRate(teamData):
    winAverage = 0.533653 + (0.204405*teamData.GPG) - (0.204638*teamData.GAPG) - (0.009540*teamData.SOGPG) \
                 + (0.008496*teamData.SOGAPG)
    return winAverage


def GetTeamData(teamName):
    teamData = TeamData()
    fileName = "Final.csv"
    path = "./TeamData/" + fileName

    with open(path, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row[0] == teamName:
                teamData.GPG = float(row[6])
                teamData.GAPG = float(row[17])
                teamData.SOGPG = float(row[15])
                teamData.SOGAPG = float(row[26])

    return teamData


def Main(teamName1, teamName2):
    team1Data = GetTeamData(teamName1)
    team2Data = GetTeamData(teamName2)
    favoredTeamName = ""

    team1WinAverage = PredictedWinRate(team1Data)
    team2WinAverage = PredictedWinRate(team2Data)
    if team1WinAverage > team2WinAverage:
        favoredTeamName = teamName1
    else:
        favoredTeamName = teamName2

    odds = min(team1WinAverage, team2WinAverage) / max(team1WinAverage, team2WinAverage)

    percent = (1 - odds) * 100
    odds = percent + 50
    print(str(round(odds, 2)) + "% " + favoredTeamName)


Main("pittsburgh-penguins", "carolina-hurricanes")
Main("seattle-kraken", "toronto-maple-leafs")
