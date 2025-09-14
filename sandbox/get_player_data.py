from nba_api.stats.endpoints import leaguegamefinder
import json

# reg = leaguegamefinder.LeagueGameFinder(
#             team_id_nullable=1610612737,
#             season_nullable="2023-24",
#             player_or_team_abbreviation="T",
#             season_type_nullable="Regular Season"
#         ).get_data_frames()[0]
#
# print(reg)


from nba_api.stats.endpoints import commonteamroster, commonplayerinfo
from nba_api.stats.static import players, teams

def fetch_players_data(season: str, out_dir: str = "../../data/raw/teams/"):
        player_ids = []
        team_players = commonteamroster.CommonTeamRoster(
            team_id=1610612742,
            season=season
        ).get_data_frames()[0]
        player_ids.extend(team_players["PLAYER_ID"].to_list())
        print(player_ids)
        for player_id in player_ids:
            print(commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0])
