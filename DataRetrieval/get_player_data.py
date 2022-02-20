import pandas as pd
from eliteprospect import eliteprospect_scraper as ep
import numpy as np


def format_year(year: str) -> str:
    second_year = int(year[2:4]) + 1
    return year + "-" + str(second_year)


def get_player_data(years: list):
    league = "nhl"
    nhl_skaters = []
    for year in years:
        year = format_year(year)
        player_data = ep.getPlayers(league, year)
        nhl_skaters.append(player_data)
    skater_data = pd.concat(nhl_skaters)

    return skater_data


def clean_player_data(nhl_skaters):
    # Drop player column (player name column exists)
    nhl_skaters = nhl_skaters.drop(columns='player')

    # Strip whitespace from player name column
    nhl_skaters.playername = nhl_skaters.playername.str.strip()

    # Reorder and rename columns
    nhl_skaters = nhl_skaters.loc[:, ['playername', 'team', 'season', 'league', 'position', 'gp', 'g', 'a', 'tp', 'ppg', 'pim', '+/-', 'link']]
    nhl_skaters = nhl_skaters.rename(columns={'playername': 'player'})
    nhl_skaters = nhl_skaters.rename(columns={'+/-': 'pm'})

    nhl_skaters.ppg = np.where(nhl_skaters.ppg == "-", 0, nhl_skaters.ppg)
    nhl_skaters.pm = np.where(nhl_skaters.pm == "", 0, nhl_skaters.pm)

    return nhl_skaters


def convert_column_types(nhl_skaters):
    nhl_skaters.ppg = nhl_skaters.ppg.astype(float)
    nhl_skaters.gp = nhl_skaters.gp.astype(float)
    nhl_skaters.g = nhl_skaters.g.astype(float)
    nhl_skaters.a = nhl_skaters.a.astype(float)
    nhl_skaters.pim = nhl_skaters.pim.astype(float)
    nhl_skaters.pm = nhl_skaters.pm.astype(float)

    return nhl_skaters
