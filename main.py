# Get list of games then call predict.py

# TODO: Gather current season data and use to train.
#  Only grab current season and add to spreadsheet, don't re-add all years
from nhlstats import list_games
from Models.predict import run_models

for game in list_games():
    home_team = game['home_team']
    away_team = game['away_team']
    print("Test")
    run_models(away_team, home_team)
