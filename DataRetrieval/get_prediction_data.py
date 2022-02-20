import csv
from sklearn.preprocessing import StandardScaler

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
