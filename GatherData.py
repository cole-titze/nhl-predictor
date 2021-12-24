import GetPlayerData

# Get skater data
nhl_skaters = GetPlayerData.getPlayerData()
nhl_skaters = GetPlayerData.cleanPlayerData(nhl_skaters)
nhl_skaters = GetPlayerData.convertColumnTypes(nhl_skaters)

# Save dataframe to csv
nhl_skaters.to_csv('Data/CleanedPlayers.csv')
print("Saved skater data")

