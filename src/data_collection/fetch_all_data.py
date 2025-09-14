from fetch_team_data import fetch_team_data
from fetch_player_data import fetch_players_data

seasons = ["2021-22","2022-23","2023-24","2024-25"]


# fetching the data
# for season in seasons:
#     fetch_players_data(season)
#     fetch_team_data(season)

import pandas as pd
df = pd.read_csv("../../data/raw/teams/team_game_log_2023-24.csv")
print(df.shape)
print(df["TEAM_ID"].nunique())  # should be 30
print(df["GAME_ID"].nunique())  # should be ~1230

df = pd.read_csv("../../data/raw/players/player_game_log_2023-2ok 4.csv")
print(df.shape)
print(df["Player_ID"].nunique())  # ~450–500
print(df["Game_ID"].nunique())    # should line up with teams file
