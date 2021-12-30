import requests
import csv
# TODO: Have each year be written to the csv after it is received instead of keeping all data and saving at the end (this will help with memory hogging)


def is_invalid_game(game: dict) -> bool:
    # Check for game not returned by api
    if 'message' in game:
        return True
    # Check for covid/invalid game
    if float(game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['faceOffWinPercentage']) == 0 and \
            float(game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['faceOffWinPercentage']) == 0:
        return True
    return False


def get_winner(h_goals: int, a_goals: int) -> str:
    if h_goals > a_goals:
        return "Home"
    elif h_goals == a_goals:
        return "Draw"
    return "Away"


def build_row(game: dict) -> list:
    date = game['gameData']['datetime']['dateTime'].split('T')[0]
    home_goals = int(game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals'])
    away_goals = int(game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals'])
    winner = get_winner(home_goals, away_goals)

    clean_row = [game['gameData']['teams']['home']['name'],
                 game['gameData']['teams']['away']['name'],
                 game['gameData']['game']['season'],
                 date,
                 home_goals,
                 away_goals,
                 winner,
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['shots'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['shots'],
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['powerPlayGoals'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['powerPlayGoals'],
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['pim'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['pim'],
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['faceOffWinPercentage'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['faceOffWinPercentage'],
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['blocked'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['blocked'],
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['hits'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['hits'],
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['takeaways'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['takeaways'],
                 game['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['giveaways'],
                 game['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['giveaways']]

    return clean_row


def get_games():
    # Set up the API call variables
    games = []
    game_data = []
    years = ['2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    season_type = '02'
    max_game_ID = 1400

    print("Getting Match Data:")
    for year in years:
        print(year)
        # Loop over the counter and format the API call
        for i in range(0, max_game_ID):
            r = requests.get(url='http://statsapi.web.nhl.com/api/v1/game/'
                                 + year + season_type + str(i).zfill(4)+'/feed/live')
            data = r.json()
            game_data.append(data)

    count = 0
    for game in game_data:
        # Skip covid/invalid games
        if is_invalid_game(game):
            continue
        # Create list
        row = [count]
        row.extend(build_row(game))
        games.append(row)
        count = count + 1

    return games


def to_csv(game_rows: list) -> None:
    file_path = '../Data/Matches.csv'

    # now we will open a file for writing
    with open(file_path, 'w') as data_file:

        # create the csv writer object
        csv_writer = csv.writer(data_file)

        # Counter variable used for writing
        # headers to the CSV file
        header = ['id', 'home_team', 'away_team', 'season', 'date', 'home_g', 'away_g', 'winner', 'home_sog', 'away_sog', 'home_ppg', 'away_ppg',
                  'home_pim', 'away_pim', 'home_face_off_win_percent', 'away_face_off_win_percent', 'home_blocked_shots',
                  'away_blocked_shots', 'home_hits', 'away_hits', 'home_takeaways', 'away_takeaways', 'home_giveaways',
                  'away_giveaways']
        csv_writer.writerow(header)

        csv_writer.writerows(game_rows)
