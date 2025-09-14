from nba_api.stats.endpoints import leaguegamefinder
import json

reg = leaguegamefinder.LeagueGameFinder(
            team_id_nullable=1610612737,
            season_nullable="2023-24",
            player_or_team_abbreviation="T",
            season_type_nullable="Regular Season"
        ).get_data_frames()[0]

print(reg)
