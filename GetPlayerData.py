import pandas as pd
from eliteprospect import eliteprospect_scraper as ep
import numpy as np


def getPlayerData():
    league = "nhl"
    nhl_2012 = ep.getPlayers(league, '2012-13')
    nhl_2013 = ep.getPlayers(league, '2013-14')
    nhl_2014 = ep.getPlayers(league, '2014-15')
    nhl_2015 = ep.getPlayers(league, '2015-16')
    nhl_2016 = ep.getPlayers(league, '2016-17')
    nhl_2017 = ep.getPlayers(league, '2017-18')
    nhl_2018 = ep.getPlayers(league, '2018-19')

    nhl_skaters = pd.concat([nhl_2012, nhl_2013, nhl_2014, nhl_2015, nhl_2016, nhl_2017, nhl_2018])

    return nhl_skaters


def cleanPlayerData(nhl_skaters):
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


def convertColumnTypes(nhl_skaters):
    nhl_skaters.ppg = nhl_skaters.ppg.astype(float)
    nhl_skaters.gp = nhl_skaters.gp.astype(float)
    nhl_skaters.g = nhl_skaters.g.astype(float)
    nhl_skaters.a = nhl_skaters.a.astype(float)
    nhl_skaters.pim = nhl_skaters.pim.astype(float)
    nhl_skaters.pm = nhl_skaters.pm.astype(float)

    return nhl_skaters
