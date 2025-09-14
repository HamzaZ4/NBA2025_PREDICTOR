from nba_api.stats.endpoints import commonteamroster, playergamelog
from nba_api.stats.static import players, teams
import pandas as pd
import time

def fetch_players_data(season: str, out_dir: str = "../../data/raw/players/"):
    all_teams = teams.get_teams()
    player_ids = []
    for team in all_teams:
        team_players = commonteamroster.CommonTeamRoster(
            team_id=team["id"],
            season=season
        ).get_data_frames()[0]
        player_ids.extend(
            [pid for pid in team_players["PLAYER_ID"].to_list() if pid not in player_ids]
        )
        time.sleep(0.5)

    frames = []
    for player_id in player_ids:
        player_game_log = playergamelog.PlayerGameLog(
            player_id=player_id,
            season=season,
            season_type_all_star="Regular Season"
        ).get_data_frames()[0]

        frames.append(player_game_log)
        time.sleep(0.5)

    df = pd.concat(frames, ignore_index=True)

    df.to_csv(f"{out_dir}player_game_log_{season}.csv", index=False)
    return f"{out_dir}player_game_log_{season}.csv"




