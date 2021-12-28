import requests
import csv


def build_row(gameData: dict) -> list:
    date = gameData['gameData']['datetime']['dateTime'].split('T')[0]

    clean_row = [gameData['gameData']['teams']['home']['name'],
                 gameData['gameData']['teams']['away']['name'],
                 date,
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['shots'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['shots'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['powerPlayGoals'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['powerPlayGoals'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['pim'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['pim'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['faceOffWinPercentage'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['faceOffWinPercentage'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['blocked'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['blocked'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['hits'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['hits'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['takeaways'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['takeaways'],
                 gameData['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['giveaways'],
                 gameData['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['giveaways']]

    return clean_row


def get_games():
    # Set up the API call variables
    games = []
    game_data = []
    year = '2019'
    season_type = '02'
    max_game_ID = 2  # 1312

    # Loop over the counter and format the API call
    for i in range(0, max_game_ID):
        r = requests.get(url='http://statsapi.web.nhl.com/api/v1/game/'
                             + year + season_type + str(i).zfill(4)+'/feed/live')
        print('http://statsapi.web.nhl.com/api/v1/game/' + year + season_type + str(i).zfill(4) + '/feed/live')
        data = r.json()
        game_data.append(data)

    count = 0
    for game in game_data:
        # Skip bad entries
        if 'message' in game:
            continue
        # Create list
        row = [count]
        row.extend(build_row(game))
        games.append(row)
        count = count + 1

    return games


def to_csv(game_rows: list) -> None:
    file_path = './Data/Matches.csv'

    # now we will open a file for writing
    with open(file_path, 'w') as data_file:

        # create the csv writer object
        csv_writer = csv.writer(data_file)

        # Counter variable used for writing
        # headers to the CSV file
        header = ['id', 'home_team', 'away_team', 'date', 'home_g', 'away_g', 'home_sog', 'away_sog', 'home_ppg', 'away_ppg',
                  'home_pim', 'away_pim', 'home_face_off_win_percent', 'away_face_off_win_percent', 'home_blocked_shots',
                  'away_blocked_shots', 'home_hits', 'away_hits', 'home_takeaways', 'away_takeaways', 'home_giveaways',
                  'away_giveaways']
        csv_writer.writerow(header)

        csv_writer.writerows(game_rows)
