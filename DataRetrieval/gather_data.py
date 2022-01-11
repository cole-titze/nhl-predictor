import get_player_data
import get_game_data
import get_pregame_data
from eliteprospect import eliteprospect_scraper as ep
import os.path

train_years = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
test_years = ['2020']


def check_files() -> bool:
    return not os.path.exists('../Data/CleanedPlayers.csv') or not os.path.exists('../Data/League.csv') \
           or not os.path.exists('../Data/Team.csv')


def get_nhl_data():
    if check_files():
        # Get skater data
        nhl_skaters = get_player_data.get_player_data(train_years)
        player_data = nhl_skaters
        nhl_skaters = get_player_data.clean_player_data(nhl_skaters)
        nhl_skaters = get_player_data.convert_column_types(nhl_skaters)
        nhl_skaters.to_csv('../Data/CleanedPlayers.csv')
        print("Skater Data Saved")

        # Get League Data
        league_data = ep.getSeasonStat(player_data)
        league_data.to_csv('../Data/League.csv')
        print("League Data Saved")

        # Get Team Data
        team_data = ep.getTeamStat(player_data)
        team_data.rename(columns={"nbr_players": "nbr_players_team"}, inplace=True)
        team_data.to_csv('../Data/Team.csv')
        print("Team Data Saved")


def get_match_history():
    if not os.path.exists('../Data/Matches.csv') or not os.path.exists('../Data/TestingMatches.csv'):
        # Get Training Game Data
        game_data = get_game_data.get_games(train_years)
        get_game_data.to_csv(game_data, '../Data/Matches.csv')
        print("Training Game Data Saved")

        # Get Test Data
        game_data = get_game_data.get_games(test_years)
        get_game_data.to_csv(game_data, '../Data/TestingMatches.csv')
        print("Testing Game Data Saved")


def get_pregame_stats():
    if not os.path.exists('../Data/PregameStats.csv') or not os.path.exists('../Data/TestingPregameStats.csv'):
        # Gather Training Pregame Statistics
        pregame_data = get_pregame_data.get_pregame_statistics('../Data/Matches.csv')
        get_pregame_data.to_csv(pregame_data, '../Data/PregameStats.csv')
        print("Training Pregame Data Saved")

        # Gather Testing Pregame Statistics
        testing_data = get_pregame_data.get_pregame_statistics('../Data/TestingMatches.csv')
        get_pregame_data.to_csv(testing_data, '../Data/TestingPregameStats.csv')
        print("Testing Pregame Data Saved")


def gather_data() -> None:
    get_nhl_data()
    get_match_history()
    get_pregame_stats()


gather_data()
