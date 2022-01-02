import csv
# TODO: Make row a dictionary instead of list for easier reading
# TODO: Make list of years something passed in instead of magic string


def sort(pregame_data):
    pregame_data.sort(key=lambda x: x[1])
    return pregame_data


def get_played_games(game_id: int, season_data: list):
    valid_games = []
    for row in season_data:
        if int(row[0]) < game_id:
            valid_games.append(row)
    return valid_games


def get_games_by_team(valid_games: list, team_name: str):
    team_games = []
    for row in valid_games:
        if row[1] == team_name or row[2] == team_name:
            team_games.append(row)
    return team_games


def game_win(game: list, team_name: str):
    if game[1] == team_name and game[7] == "Home":
        return True
    if game[2] == team_name and game[7] == "Away":
        return True
    return False


def get_win_ratio(game_id: int, season_data: list, team_name: str):
    win_ratio = 0
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)

    # Reverse to walk through previous games
    team_games.reverse()
    count = 0
    for row in team_games:
        if count == 5:
            break
        if game_win(row, team_name):
            win_ratio = win_ratio + 1
        count = count + 1
    if count > 0:
        win_ratio = float(win_ratio) / float(count)
    return win_ratio


def get_single_season(historic_data: list, season: str):
    season_data = []
    for row in historic_data:
        if row[3] == season:
            season_data.append(row)
    return season_data


def get_pregame_statistics():
    years = ['20122013', '20132014', '20142015', '20152016', '20162017', '20172018', '20182019', '20192020']
    pregame_data = []
    with open('../Data/Matches.csv', 'r') as read_obj:
        csv_reader = list(csv.reader(read_obj))
        for season in years:
            season_data = get_single_season(csv_reader, season)
            for row in season_data:
                home_team = row[1]
                away_team = row[2]
                game_id = int(row[0])
                pregame_row_home = [
                    game_id,
                    home_team,
                    get_win_ratio(game_id, season_data, home_team),
                    # get_draw_ratio(),
                    # get_loss_ratio(),
                    # get_head_to_head_ratio(),
                    # get_current_goals_per_game(),
                    # get_current_goals_per_game_home_away()
                ]
                pregame_row_away = [
                    game_id,
                    away_team,
                    get_win_ratio(game_id, season_data, away_team),
                    # get_draw_ratio(),
                    # get_loss_ratio(),
                    # get_head_to_head_ratio(),
                    # get_current_goals_per_game(),
                    # get_current_goals_per_game_home_away()
                ]
                pregame_data.append(pregame_row_home)
                pregame_data.append(pregame_row_away)
    pregame_data = sort(pregame_data)
    return pregame_data


def to_csv(game_rows: list, file_path: str) -> None:
    # open file for writing
    with open(file_path, 'w') as data_file:

        # create the csv writer object
        csv_writer = csv.writer(data_file)

        # Counter variable used for writing
        # headers to the CSV file
        header = ['id', 'team_name', 'win_ratio_5', 'draw_ratio_5', 'loss_ratio_5', 'h2h_w_d_l_ratio', 'current_goals_avg',
                  'current_goals_avg_h_a']
        csv_writer.writerow(header)

        csv_writer.writerows(game_rows)
