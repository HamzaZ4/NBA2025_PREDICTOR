import pandas as pd
from pathlib import Path

SEASONS = ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT/"data"/"processed"
DATA_DIR = ROOT/"data"/"raw"
STAT_COLS = ["PTS", "AST", "REB", "STL", "TOV", "MIN", "GP"]

def build_prospective_stats(season, data_dir, out_dir):
    prev_idx = SEASONS.index(season) - 1
    if prev_idx < 0:
        raise ValueError("No previous season data to use for prospective stats")

    prev_season = SEASONS[prev_idx]

    current_rosters = pd.read_csv(f"{data_dir}/team_rosters/team_rosters_{season}.csv")
    prev_stats = pd.read_csv(f"{data_dir}/player_stats/player_season_totals_{prev_season}.csv")

    merged = current_rosters.merge(prev_stats, on="PLAYER_ID", how="left")

    keeper_cols = ["TeamID","PLAYER","PLAYER_ID","HOW_ACQUIRED","GP","REB","AST","TOV","STL","PTS","MIN","TEAM_NAME"]
    trimmed_player_stats = merged[keeper_cols].rename(columns={"TeamID":"TEAM_ID"})

    cleaned_player_stats = assign_profiles(trimmed_player_stats, season)

    cleaned_player_stats.to_csv(f"{out_dir}/prospective_player_stats/prospective_player_stats_{season}.csv",
                                index=False)

    team_stats = cleaned_player_stats.groupby(["TEAM_ID","TEAM_NAME"])[STAT_COLS].sum().reset_index()
    team_stats["SEASON"] = season


    team_stats.to_csv(f"{out_dir}/prospective_team_stats/prospective_team_stats_{season}.csv", index=False)

    return cleaned_player_stats, team_stats

def assign_profiles(player_stats, season: str):

    default_profiles = pd.read_csv(f"{OUT_DIR}/default_player_profiles.csv")
    player_profiles = pd.read_csv(f"{OUT_DIR}/player_profiles/player_profiles_{season}.csv")

    default_profiles =  default_profiles.reindex(columns=["PROFILE_LABEL"] + STAT_COLS)


    profiled_player_stats = pd.merge(player_stats, player_profiles[["PLAYER_ID","PROFILE_LABEL"]], on="PLAYER_ID", how="left")

    profiled_player_stats = pd.merge(profiled_player_stats, default_profiles, on="PROFILE_LABEL", how="left", suffixes=("", "_y"))

    for col in STAT_COLS:
        profiled_player_stats[col] = profiled_player_stats[col].fillna(profiled_player_stats[f"{col}_y"])

    profiled_player_stats.drop(columns=["PROFILE_LABEL"] + [f"{col}_y" for col in STAT_COLS], inplace=True)

    return profiled_player_stats




if __name__ == "__main__":
    build_prospective_stats("2020-21", DATA_DIR, OUT_DIR)