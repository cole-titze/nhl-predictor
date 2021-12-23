import TopDownHockey_Scraper.TopDownHockey_EliteProspects_Scraper as hockeyScraper
import numpy as np
# import hockey_scraper


def getPlayerData():
    leagues = ["nhl"]
    seasons = ["2018-2019"]

    nhl_skaters = hockeyScraper.get_skaters(leagues, seasons)
    return nhl_skaters


def cleanPlayerData(nhl_skaters):
    # Drop player column (player name column exists)
    nhl_skaters = nhl_skaters.drop(columns='player')

    # Strip whitespace from player name column
    nhl_skaters.playername = nhl_skaters.playername.str.strip()

    # Reorder and rename columns
    nhl_skaters = nhl_skaters.loc[:, ['playername', 'team', 'season', 'league', 'position', 'gp', 'g', 'a', 'tp', 'ppg', 'pim', '+/-', 'link']]
    nhl_skaters = nhl_skaters.rename(columns={'playername': 'player'})

    nhl_skaters.ppg = np.where(nhl_skaters.ppg == "-", 0, nhl_skaters.ppg)
    return nhl_skaters
