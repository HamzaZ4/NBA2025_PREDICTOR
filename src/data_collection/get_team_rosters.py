from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.static import teams
import time
import pandas as pd
from prompt_toolkit.application import get_app


def get_team_rosters(season: str, out_dir: str = "../../data/raw/team_rosters/"):
    nba_teams = [t for t in teams.get_teams()]
    all_rosters = []

    for team in nba_teams:
        team_id = team["id"]
        team_name = team["full_name"]

        print(f"Fetching roster for {team_name}...")

        roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)
        players= roster.get_data_frames()[0]
        players["TEAM_ID"] = team_id
        players["TEAM_NAME"] = team_name
        all_rosters.append(players)
        time.sleep(0.5)

    rosters_df = pd.concat(all_rosters, ignore_index=True)

    rosters_df.to_csv(f"{out_dir}team_rosters_{season}.csv", index=False)

    return rosters_df

df = get_team_rosters("2024-25")

print(df.head())



