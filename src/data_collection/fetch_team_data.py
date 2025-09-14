from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
import pandas as pd
import os
import time

def fetch_team_data(season: str, out_dir: str = "../../data/raw/teams/"):
    """Fetch team-level stats for a season and save to CSV. Returns path."""
    all_teams = teams.get_teams()
    df = pd.DataFrame()
    for team in all_teams:

        reg = leaguegamefinder.LeagueGameFinder(
            team_id_nullable=team["id"],
            season_nullable=season,
            player_or_team_abbreviation="T",
            season_type_nullable="Regular Season"
        ).get_data_frames()[0]
        df = pd.concat([df, reg], ignore_index=True)
        print(f"Fetching {team['full_name']}...")
        time.sleep(0.5)

    df.to_csv(f"{out_dir}team_game_log_{season}.csv", index=False)
    return f"{out_dir}team_game_log_{season}.csv"

fetch_team_data("2023-24")