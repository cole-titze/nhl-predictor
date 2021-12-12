import Team
import csv


def trimStats(csvRow):
    csvRow.pop(8)
    csvRow.pop(-1)
    csvRow.pop(-1)
    csvRow.pop(-1)


def fixZeros(fixedRow):
    for i, value in enumerate(fixedRow):
        if value == "\xc3\xa2\xe2\x82\xac\xe2\x80\x9d" or value == "":
            fixedRow[i] = 0
    return fixedRow


def combineRows(tRow, oRow):
    gamesPlayed = int(tRow[2])
    name = str(tRow[0])
    goals = float(tRow[3])
    oGoals = float(oRow[3])
    assists = float(tRow[4])
    oAssists = float(oRow[4])
    points = float(tRow[5])
    oPoints = float(oRow[5])
    pom = float(tRow[6])
    oPom = float(oRow[6])
    pm = float(tRow[7])
    oPm = float(oRow[7])
    ppg = float(tRow[8])
    oPpg = float(oRow[8])
    ppa = float(tRow[9])
    oPpa = float(oRow[9])
    shg = float(tRow[10])
    oShg = float(oRow[10])
    sha = float(tRow[11])
    oSha = float(oRow[11])
    sog = float(tRow[12])
    oSog = float(oRow[12])
    sogp = float(tRow[13])
    oSogp = float(oRow[13])

    finalRow = [name, gamesPlayed, goals / gamesPlayed, assists / gamesPlayed, points / gamesPlayed,
                pom, pm / gamesPlayed, ppg / gamesPlayed, ppa / gamesPlayed,
                shg / gamesPlayed, sha / gamesPlayed, sog / gamesPlayed, sogp,
                oGoals / gamesPlayed, oAssists / gamesPlayed, oPoints / gamesPlayed,
                oPom, oPm / gamesPlayed, oPpg / gamesPlayed, oPpa / gamesPlayed,
                oShg / gamesPlayed, oSha / gamesPlayed, oSog / gamesPlayed,
                oSogp]
    return finalRow


finalFileName = "Final.csv"
fields = ["Name", "Games Played", "GPG", "APG", "PPG", "P/M", "PMPG",
          "PPGPG", "PPAPG", "SHGPG", "SHAPG", "SOGPG",
          "SOGP", "GAPG", "AAPG", "PAPG", "Opp P/M",
          "PMAPG", "PPGAPG", "PPAPG", "SHGAPG", "SHAAPG",
          "SOGAPG", "SOGAP"]

# opening the file with w+ mode truncates the file
f = open(finalFileName, "w+")
f.close()

with open(finalFileName, 'w') as csvWriteFile:
    csvwriter = csv.writer(csvWriteFile)
    csvwriter.writerow(fields)

teams = Team.teams
for team in teams:
    rows = []
    teamAbbr, teamName = team.split("/")
    print(teamAbbr)

    fileName = teamName + ".csv"
    path = "./TeamData/" + fileName

    with open(path, "r") as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            rows.append(row)
    teamRow = rows[-2]
    opponentRow = rows[-1]

    teamRow[0] = teamName
    opponentRow[0] = teamName

    trimStats(teamRow)
    trimStats(opponentRow)

    fixZeros(teamRow)
    fixZeros(opponentRow)

    newRow = combineRows(teamRow, opponentRow)

    with open(finalFileName, 'a') as csvWriteFile:
        csvwriter = csv.writer(csvWriteFile)
        csvwriter.writerow(newRow)
