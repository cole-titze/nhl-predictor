import get_player_data
import get_game_data
import get_pregame_data
from eliteprospect import eliteprospect_scraper as ep
import os.path


def check_files() -> bool:
    return not os.path.exists('../Data/CleanedPlayers.csv') or not os.path.exists('../Data/League.csv') \
           or not os.path.exists('../Data/Team.csv')


def gather_data() -> None:
    if check_files():
        # Get skater data
        nhl_skaters = get_player_data.getPlayerData()
        player_data = nhl_skaters
        nhl_skaters = get_player_data.cleanPlayerData(nhl_skaters)
        nhl_skaters = get_player_data.convertColumnTypes(nhl_skaters)
        nhl_skaters.to_csv('../Data/CleanedPlayers.csv')
        print("Skater Data Saved")

        # Get League Data
        leagueData = ep.getSeasonStat(player_data)
        leagueData.to_csv('../Data/League.csv')
        print("League Data Saved")

        # Get Team Data
        teamData = ep.getTeamStat(player_data)
        teamData.rename(columns={"nbr_players": "nbr_players_team"}, inplace=True)
        teamData.to_csv('../Data/Team.csv')
        print("Team Data Saved")

    if not os.path.exists('../Data/Matches.csv'):
        # Get Game Data
        game_data = get_game_data.get_games()
        get_game_data.to_csv(game_data, '../Data/Matches.csv')
        print("Game Data Saved")

    if not os.path.exists('../Data/PregameStats.csv'):
        # Gather Pregame Statistics
        pregame_data = get_pregame_data.get_pregame_statistics()
        get_pregame_data.to_csv(pregame_data, '../Data/PregameStats.csv')
        print("Pregame Data Saved")


gather_data()
