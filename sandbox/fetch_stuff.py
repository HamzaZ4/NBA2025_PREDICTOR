from nba_api.stats.endpoints import commonteamroster
import pandas as pd

team_id = "1610612739"  # Cleveland Cavaliers
season = "2025-26"      # Season string must be "YYYY-YY"

# Fetch roster for given season + team
roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)

# The endpoint returns multiple result sets (players + coaches)
players, coaches = roster.get_data_frames()

print("Players:")
print(players)

print("\nCoaches:")
print(coaches)
