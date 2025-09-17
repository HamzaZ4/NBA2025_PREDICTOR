import time

from nba_api.stats.endpoints import commonplayerinfo
from pathlib import Path
import pandas as pd

# SEASONS = ["2018-19","2019-20","2020-21","2021-22","2022-23","2023-24","2024-25"]
SEASONS = ["2019-20","2020-21","2021-22","2022-23","2023-24","2024-25"]

new_top3Rookies=[]
new_lotteryRookies=[]
avg_joes = []
avg_rookie= []

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT/"data"/"raw"
PROCESSED_DIR = ROOT/"data"/"processed"
SCRIPT_DIR = Path(__file__).resolve().parent
    # current_season_stats = pd.read_csv(f"../../../data/processed/player_stats/player_season_totals_{season}.csv")


def get_new_players(seasons: list, data_dir: str):
    all_new_players = []

    for i in range(1, len(SEASONS)):
        season = SEASONS[i]
        prev_season = SEASONS[i - 1]

        current_roster = pd.read_csv(f"{DATA_DIR}/team_rosters/team_rosters_{season}.csv")
        prev_season_roster = pd.read_csv(f"{DATA_DIR}/team_rosters/team_rosters_{prev_season}.csv")

        current_ids = set(current_roster["PLAYER_ID"])
        prev_ids = set(prev_season_roster["PLAYER_ID"])

        # these are newp players
        new_players = current_roster[current_roster["PLAYER_ID"].isin(current_ids - prev_ids)]
        new_players = current_roster[current_roster["PLAYER_ID"].isin(current_ids - prev_ids)].copy()
        new_players["SEASON"] = season

        new_players["PROFILE_LABEL"] = new_players.apply(
            lambda row: assign_profile(row["PLAYER_ID"], row["SEASON"]), axis=1
        )

        new_players = new_players[["PLAYER_ID", "SEASON","PROFILE_LABEL"]]

        new_players.to_csv(f"{PROCESSED_DIR}/player_profiles/player_profiles_{season}.csv", index=False)

        all_new_players.append(new_players)

    return pd.concat(all_new_players, ignore_index=True)



def assign_profile(player_id: str, season: str):
    time.sleep(0.5)

    season_star_year = int(season.split("-")[0])
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
    print("getting data for ", player_info.loc[0, "FIRST_NAME"])

    draft_round = player_info.loc[0, "DRAFT_ROUND"]
    draft_pick = player_info.loc[0, "DRAFT_NUMBER"]
    draft_year = player_info.loc[0, "DRAFT_YEAR"]

    if draft_year and draft_year != "Undrafted":
        draft_year = int(draft_year)

    if draft_pick != 'Undrafted' and draft_pick and draft_year == season_star_year:
        draft_pick = int(draft_pick)
        draft_round = int(draft_round)

        if draft_pick <= 3:
            return "Top3Rookie"
        elif draft_pick <= 16:
            return "LotteryRookie"
        else:
            return "AverageRookie"

    else:
        return "AverageJoe"



def compute_profile_averages(new_players_df, data_dir):
    profile_stats = []
    for season in new_players_df["SEASON"].unique():

        stats = pd.read_csv(f"{data_dir}/player_stats/player_season_totals_{season}.csv")
        merged = new_players_df[new_players_df["SEASON"] == season].merge(
            stats,
            on="PLAYER_ID",
            how="left"
        )
        profile_stats.append(merged)

    full = pd.concat(profile_stats, ignore_index=True)
    cols = ["AST","TOV","PTS","MIN","GP","STL","REB"]
    profile_means = full.groupby("PROFILE_LABEL")[cols].mean().reset_index()

    return profile_means




if __name__ == "__main__":
    new_players = get_new_players(SEASONS, DATA_DIR)

    averages = compute_profile_averages(new_players, DATA_DIR)
    averages.to_csv(f"./default_player_profiles.csv", index=False)
    print(averages)