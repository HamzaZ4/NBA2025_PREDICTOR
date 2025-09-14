from nba_api.stats.endpoints import boxscoretraditionalv3, boxscoresummaryv2, commonteamroster
import pandas as pd

team_id = "1610612739"
season = "2023-24"

roster = commonteamroster.CommonTeamRoster(team_id)
players = roster.get_data_frames()

game_id = "1610612739"
boxscore = boxscoresummaryv2.BoxScoreSummaryV2(game_id).get_data_frames()
print(boxscore)