from eliteprospect import eliteprospect_scraper as ep
import numpy as np
import pandas as pd

shl_2012 = ep.getPlayers('shl', '2012-13')
shl_2013 = ep.getPlayers('shl', '2013-14')
shl_2014 = ep.getPlayers('shl', '2014-15')
shl_2015 = ep.getPlayers('shl', '2015-16')
shl_2016 = ep.getPlayers('shl', '2016-17')
shl_2017 = ep.getPlayers('shl', '2017-18')
shl_2018 = ep.getPlayers('shl', '2018-19')
shl_2019 = ep.getPlayers('shl', '2019-20')

players_shl = pd.concat([shl_2012,shl_2013,shl_2014,shl_2015,shl_2016,shl_2017,shl_2018,shl_2019])

print("here")

allsvenskan_2012 = ep.getPlayers('allsvenskan', '2012-13')
allsvenskan_2013 = ep.getPlayers('allsvenskan', '2013-14')
allsvenskan_2014 = ep.getPlayers('allsvenskan', '2014-15')
allsvenskan_2015 = ep.getPlayers('allsvenskan', '2015-16')
allsvenskan_2016 = ep.getPlayers('allsvenskan', '2016-17')
allsvenskan_2017 = ep.getPlayers('allsvenskan', '2017-18')
allsvenskan_2018 = ep.getPlayers('allsvenskan', '2018-19')
allsvenskan_2019 = ep.getPlayers('allsvenskan', '2019-20')

players_allsvenskan = pd.concat([allsvenskan_2012,allsvenskan_2013,allsvenskan_2014,
                                 allsvenskan_2015,allsvenskan_2016,allsvenskan_2017,
                                 allsvenskan_2018,allsvenskan_2019])

teamstat = ep.getTeamStat(pd.concat([players_shl, players_allsvenskan]))
teamstat.rename(columns={ "nbr_players":"nbr_players_team"}, inplace=True)

leaguestat_shl = ep.getSeasonStat(players_shl)
leaguestat_shl['league'] = 'SHL'
leaguestat_allsvenskan = ep.getSeasonStat(players_allsvenskan)
leaguestat_allsvenskan['league'] = 'allsvenskan'



leaguestat_allsvenskan.rename(columns={ "avg_+/-_team":"avg_+/-_season"}, inplace=True)
leaguestat_shl.rename(columns={ "avg_+/-_team":"avg_+/-_season"}, inplace=True)

leaguestat_allsvenskan.rename(columns={ "nbr_players":"nbr_players_season"}, inplace=True)
leaguestat_shl.rename(columns={ "nbr_players":"nbr_players_season"}, inplace=True)

# Merge

leaguestat = leaguestat_shl.append(pd.DataFrame(data = leaguestat_allsvenskan), ignore_index=True)

playersmeta = ep.getPlayerMetadata(pd.concat([players_shl, players_allsvenskan]))
print("Here 2")
playerlinks = playersmeta['link']
