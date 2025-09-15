from nba_api.stats.endpoints import commonplayerinfo
from pathlib import Path
import pandas as pd

# SEASONS = ["2018-19","2019-20","2020-21","2021-22","2022-23","2023-24","2024-25"]
SEASONS = ["2023-24","2024-25"]

new_top5Rookies=[]
new_lotteryRookies=[]
avg_joes = []
avg_rookie= []

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT/"data"/"raw"
SCRIPT_DIR = Path(__file__).resolve().parent

for i in range(1,len(SEASONS)):
    season = SEASONS[i]
    prev_season = SEASONS[i-1]

    current_roster = pd.read_csv(f"{DATA_DIR}/team_rosters/team_rosters_{season}.csv")
    prev_season_roster = pd.read_csv(f"{DATA_DIR}/team_rosters/team_rosters_{prev_season}.csv")

    current_ids = set(current_roster["PLAYER_ID"])
    prev_ids = set(prev_season_roster["PLAYER_ID"])

    # these are newp players
    new_players = current_roster[current_roster["PLAYER_ID"].isin(current_ids - prev_ids)]


    print(new_players)
    # current_season_stats = pd.read_csv(f"../../../data/processed/player_stats/player_season_totals_{season}.csv")






