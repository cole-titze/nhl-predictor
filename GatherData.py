import GetPlayerData
import GetGameData
from eliteprospect import eliteprospect_scraper as ep
import os.path


def check_files() -> bool:
    return not os.path.exists('Data/CleanedPlayers.csv') or not os.path.exists('Data/League.csv') \
           or not os.path.exists('Data/Team.csv')


def gather_data() -> None:
    if check_files():
        # Get skater data
        nhl_skaters = GetPlayerData.getPlayerData()
        player_data = nhl_skaters
        nhl_skaters = GetPlayerData.cleanPlayerData(nhl_skaters)
        nhl_skaters = GetPlayerData.convertColumnTypes(nhl_skaters)
        nhl_skaters.to_csv('Data/CleanedPlayers.csv')
        print("Skater Data Saved")

        # Get League Data
        leagueData = ep.getSeasonStat(player_data)
        leagueData.to_csv('Data/League.csv')
        print("League Data Saved")

        # Get Team Data
        teamData = ep.getTeamStat(player_data)
        teamData.rename(columns={"nbr_players": "nbr_players_team"}, inplace=True)
        teamData.to_csv('Data/Team.csv')
        print("Team Data Saved")

    if not os.path.exists('Data/Matches.csv'):
        # Get Game Data
        game_data = GetGameData.get_games()
        GetGameData.to_csv(game_data)
        print("Game Data Saved")


gather_data()
