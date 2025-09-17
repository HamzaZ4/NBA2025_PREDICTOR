from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd

NBA_LEAGUE_ID = "00"
def get_player_averages(season, out_dir = "../../data/raw/player_stats/"):

    stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        season_type_all_star="Regular Season",
        league_id_nullable=NBA_LEAGUE_ID
    )
    print(f"Fetching player stats for {season}...")
    df = stats.get_data_frames()[0]
    print(df)
    df.to_csv(f"{out_dir}player_season_totals_{season}.csv", index=False)
    return f"{out_dir}player_season_totals_{season}.csv"


if __name__ == "__main__":
    get_player_averages("2019-20")