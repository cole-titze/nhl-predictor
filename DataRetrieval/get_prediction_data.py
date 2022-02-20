from sklearn.preprocessing import StandardScaler
import DataRetrieval.get_pregame_data as pg
import csv

def get_games(file_path: str) -> list:
    games = []
    with open(file_path, 'r') as read_obj:
        csv_reader = list(csv.reader(read_obj))
        for row in csv_reader:
            if row[19] == "False":
                games.append(row)
    return games

def get_independent(games: list) -> list:
    x = []
    for game in games:
        x.append(game[3:18])
    return x

def get_dependent(games: list) -> list:
    y = []
    for game in games:
        y.append(game[18])
    replacements = {"Home": 0, "Away": 1}
    replacer = replacements.get
    y = [replacer(n, n) for n in y]

    return y

def get_info(games: list) -> list:
    info = []
    for game in games:
        info.append(game[0:3])
    return info

def split_data():
    training_games = get_games("Data/PregameStats.csv")
    x_training = get_independent(training_games)
    y_training = get_dependent(training_games)
    # info_training = get_info(training_games)

    # Test Season data
    test_games = get_games("Data/TestingPregameStats.csv")
    x_test_season = get_independent(test_games)
    y_test_season = get_dependent(test_games)

    # Standardize all data
    x_training = StandardScaler().fit_transform(x_training)
    x_test_season = StandardScaler().fit_transform(x_test_season)

    return x_training, y_training, x_test_season, y_test_season

def clean_x(x):
    cleaned_x = []
    for row in x:
        row.pop(-3)
        row.pop(2)
        row.pop(1)

        cleaned_x.append(row)

    return cleaned_x

def get_single_game(home_team, away_team):
    with open('./Data/CurrentMatches.csv', 'r') as read_obj:
        csv_reader = list(csv.reader(read_obj))
    season = '20212022'
    season_data = pg.get_single_season(csv_reader, season)
    game_id = int(1000)
    pregame_row = [
        pg.get_win_ratio(game_id, season_data, home_team),
        pg.get_current_goals_per_game(game_id, season_data, home_team),
        pg.get_current_goals_per_game_home(game_id, season_data, home_team),
        pg.get_current_conceded_goals_per_game(game_id, season_data, home_team),
        pg.get_current_conceded_goals_per_game_home(game_id, season_data, home_team),
        pg.get_goal_average_scoped(game_id, season_data, home_team),
        pg.get_conceded_goal_average_scoped(game_id, season_data, home_team),
        pg.get_win_ratio(game_id, season_data, away_team),
        pg.get_current_goals_per_game(game_id, season_data, away_team),
        pg.get_current_goals_per_game_away(game_id, season_data, away_team),
        pg.get_current_conceded_goals_per_game(game_id, season_data, away_team),
        pg.get_current_conceded_goals_per_game_away(game_id, season_data, away_team),
        pg.get_goal_average_scoped(game_id, season_data, away_team),
        pg.get_conceded_goal_average_scoped(game_id, season_data, away_team),
        pg.get_head_to_head_ratio(game_id, season_data, away_team, home_team)
    ]
    return pregame_row