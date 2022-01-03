import csv
# TODO: Make row a dictionary instead of list for easier reading
# TODO: Make list of years something passed in instead of magic string


def sort(pregame_data: list) -> list:
    pregame_data.sort(key=lambda x: x[1])
    return pregame_data


def get_played_games(game_id: int, season_data: list) -> list:
    valid_games = []
    for row in season_data:
        if int(row[0]) < game_id:
            valid_games.append(row)
    return valid_games


def get_games_by_team(valid_games: list, team_name: str) -> list:
    team_games = []
    for row in valid_games:
        if row[1] == team_name or row[2] == team_name:
            team_games.append(row)
    return team_games


def game_win(game: list, team_name: str) -> bool:
    if game[1] == team_name and game[7] == "Home":
        return True
    if game[2] == team_name and game[7] == "Away":
        return True
    return False


def game_loss(game: list, team_name: str) -> bool:
    if game[1] == team_name and game[7] == "Away":
        return True
    if game[2] == team_name and game[7] == "Home":
        return True
    return False


def game_draw(game: list) -> bool:
    if game[7] == "Draw":
        return True
    return False


def get_loss_ratio(game_id: int, season_data: list, team_name: str) -> float:
    loss_ratio = 0
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)

    # Reverse to walk through previous games
    team_games.reverse()
    count = 0
    for row in team_games:
        if count == 5:
            break
        if game_loss(row, team_name):
            loss_ratio = loss_ratio + 1
        count = count + 1
    if count > 0:
        loss_ratio = float(loss_ratio) / float(count)
    return loss_ratio


def get_draw_ratio(game_id: int, season_data: list, team_name: str) -> float:
    draw_ratio = 0
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)

    # Reverse to walk through previous games
    team_games.reverse()
    count = 0
    for row in team_games:
        if count == 5:
            break
        if game_draw(row):
            draw_ratio = draw_ratio + 1
        count = count + 1
    if count > 0:
        draw_ratio = float(draw_ratio) / float(count)
    return draw_ratio


def get_win_ratio(game_id: int, season_data: list, team_name: str) -> float:
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


def get_goal_average_scoped(game_id, season_data, team_name):
    goal_ratio = 0
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)

    # Reverse to walk through previous games
    team_games.reverse()
    count = 0
    for row in team_games:
        if count == 5:
            break
        goal_ratio += get_goals(row, team_name)
        count = count + 1
    if count > 0:
        goal_ratio = float(goal_ratio) / float(count)
    return goal_ratio


def get_conceded_goal_average_scoped(game_id, season_data, team_name):
    goal_ratio = 0
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)

    # Reverse to walk through previous games
    team_games.reverse()
    count = 0
    for row in team_games:
        if count == 5:
            break
        goal_ratio += get_conceded_goals(row, team_name)
        count = count + 1
    if count > 0:
        goal_ratio = float(goal_ratio) / float(count)
    return goal_ratio


def get_single_season(historic_data: list, season: str) -> list:
    season_data = []
    for row in historic_data:
        if row[3] == season:
            season_data.append(row)
    return season_data


def get_head_to_head_ratio(game_id: int, season_data: list, team_one: str, team_two: str):
    # Get games that both teams played in
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_one)
    head_to_head_games = get_games_by_team(team_games, team_two)

    # Count games won and divide by total games
    win_ratio = 0
    count = 0
    for game in head_to_head_games:
        if game_win(game, team_one):
            win_ratio = win_ratio + 1
        count = count + 1
    if count > 0:
        win_ratio = float(win_ratio) / float(count)
    return win_ratio


def get_home_goals(game: list, team_name: str) -> int:
    if game[1] == team_name:
        return int(game[5])
    return 0


def get_away_goals(game: list, team_name: str) -> int:
    if game[2] == team_name:
        return int(game[6])
    return 0


def get_home_conceded_goals(game: list, team_name: str) -> int:
    if game[1] == team_name:
        return int(game[6])
    return 0


def get_away_conceded_goals(game: list, team_name: str) -> int:
    if game[2] == team_name:
        return int(game[5])
    return 0


def get_goals(game: list, team_name: str) -> int:
    goals = 0
    goals += get_away_goals(game, team_name)
    goals += get_home_goals(game, team_name)

    return goals


def get_conceded_goals(game: list, team_name: str) -> int:
    goals = 0
    goals += get_away_conceded_goals(game, team_name)
    goals += get_home_conceded_goals(game, team_name)

    return goals


def get_current_conceded_goals_per_game(game_id: int, season_data: list, team_name: str) -> float:
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)

    goals_avg = 0
    count = 0
    for game in team_games:
        goals_avg = goals_avg + get_conceded_goals(game, team_name)
        count = count + 1
    if count > 0:
        goals_avg = goals_avg / count
    return goals_avg


def get_current_goals_per_game(game_id: int, season_data: list, team_name: str) -> float:
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)

    goals_avg = 0
    count = 0
    for game in team_games:
        goals_avg = goals_avg + get_goals(game, team_name)
        count = count + 1
    if count > 0:
        goals_avg = goals_avg / count
    return goals_avg


def get_home_games(team_games: list, team_name: str) -> list:
    home_games = []
    for game in team_games:
        if game[1] == team_name:
            home_games.append(game)
    return home_games


def get_away_games(team_games: list, team_name: str) -> list:
    away_games = []
    for game in team_games:
        if game[2] == team_name:
            away_games.append(game)
    return away_games


def get_current_goals_per_game_home(game_id: int, season_data: list, team_name: str) -> float:
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)
    home_games = get_home_games(team_games, team_name)

    goals_avg = 0
    count = 0
    for game in home_games:
        goals_avg += get_home_goals(game, team_name)
        count = count + 1
    if count > 0:
        goals_avg = goals_avg / count
    return goals_avg


def get_current_goals_per_game_away(game_id: int, season_data: list, team_name: str) -> float:
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)
    away_games = get_away_games(team_games, team_name)

    goals_avg = 0
    count = 0
    for game in away_games:
        goals_avg += get_away_goals(game, team_name)
        count = count + 1
    if count > 0:
        goals_avg = goals_avg / count
    return goals_avg


def get_current_conceded_goals_per_game_home(game_id: int, season_data: list, team_name: str) -> float:
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)
    home_games = get_home_games(team_games, team_name)

    goals_avg = 0
    count = 0
    for game in home_games:
        goals_avg += get_home_conceded_goals(game, team_name)
        count = count + 1
    if count > 0:
        goals_avg = goals_avg / count
    return goals_avg


def get_current_conceded_goals_per_game_away(game_id: int, season_data: list, team_name: str) -> float:
    valid_games = get_played_games(game_id, season_data)
    team_games = get_games_by_team(valid_games, team_name)
    away_games = get_away_games(team_games, team_name)

    goals_avg = 0
    count = 0
    for game in away_games:
        goals_avg += get_away_conceded_goals(game, team_name)
        count = count + 1
    if count > 0:
        goals_avg = goals_avg / count
    return goals_avg


def get_pregame_statistics(file_path: str):
    years = ['20122013', '20132014', '20142015', '20152016', '20162017', '20172018', '20182019', '20192020', '20202021']
    pregame_data = []
    with open(file_path, 'r') as read_obj:
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
                    get_draw_ratio(game_id, season_data, home_team),
                    get_loss_ratio(game_id, season_data, home_team),
                    get_head_to_head_ratio(game_id, season_data, home_team, away_team),
                    get_current_goals_per_game(game_id, season_data, home_team),
                    get_current_goals_per_game_home(game_id, season_data, home_team),
                    get_current_conceded_goals_per_game(game_id, season_data, home_team),
                    get_current_conceded_goals_per_game_home(game_id, season_data, home_team),
                    get_goal_average_scoped(game_id, season_data, home_team),
                    get_conceded_goal_average_scoped(game_id, season_data, home_team),
                    row[7]
                ]
                pregame_row_away = [
                    game_id,
                    away_team,
                    get_win_ratio(game_id, season_data, away_team),
                    get_draw_ratio(game_id, season_data, away_team),
                    get_loss_ratio(game_id, season_data, away_team),
                    get_head_to_head_ratio(game_id, season_data, away_team, home_team),
                    get_current_goals_per_game(game_id, season_data, away_team),
                    get_current_goals_per_game_away(game_id, season_data, away_team),
                    get_current_conceded_goals_per_game(game_id, season_data, away_team),
                    get_current_conceded_goals_per_game_away(game_id, season_data, away_team),
                    get_goal_average_scoped(game_id, season_data, away_team),
                    get_conceded_goal_average_scoped(game_id, season_data, away_team),
                    row[7]
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
                  'current_goals_avg_h_a', 'conceded_goals_avg', 'conceded_goals_avg_h_a', 'goal_average_5',
                  'conceded_average_5', 'result']
        csv_writer.writerow(header)

        csv_writer.writerows(game_rows)
