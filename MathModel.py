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
    fileName = teamName + ".csv"
    path = "../TeamData/" + fileName
    rows = []

    with open(path, "r") as csvfile:
        csvreader = csv.reader(csvfile)
    for row in csvreader:
        if row[1] == teamName:
            teamData.GPG = row[3]

    return teamData


def Main(teamName1, teamName2):
    team1Data = GetTeamData(teamName1)
    team2Data = GetTeamData(teamName2)

    team1WinAverage = PredictedWinRate(team1Data)
    team2WinAverage = PredictedWinRate(team2Data)
