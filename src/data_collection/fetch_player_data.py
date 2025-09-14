import nba_api.stats.endpoints as endpoints
import nba_api.stats.static.players as players

def fetch_players_data(season: str, out_dir: str = "../../data/raw/teams/"):
    all_players = players.get_players()