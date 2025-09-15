from fetch_team_data import fetch_team_data
from fetch_player_data import fetch_players_data
from get_player_averages import get_player_averages
from get_team_rosters import get_team_rosters

SEASONS = ["2018-19","2019-20","2020-21","2021-22","2022-23","2023-24","2024-25"]


# fetching the data
# for season in seasons:
#     fetch_players_data(season)
#     fetch_team_data(season)

# Updated my approach to only considering player stats ( season totals )

for season in SEASONS:
    get_player_averages(season)
    get_team_rosters(season)