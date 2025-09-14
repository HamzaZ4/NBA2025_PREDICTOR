from nba_api.stats.endpoints import leaguegamefinder, boxscoresummaryv2, boxscoretraditionalv3
import pandas as pd

finder = leaguegamefinder.LeagueGameFinder(season_nullable="2023-24")

games_df = finder.get_data_frames()[0]

sample_games = games_df.head(1)["GAME_ID"].tolist()

all_games = []
all_players = []

for game_id in sample_games:
    summary = boxscoresummaryv2.BoxScoreSummaryV2(game_id = game_id)
    game_info_df = summary.get_data_frames()[0]
    game_row = {
        "game_id": game_id,
        "date" : game_info_df.loc[0, "GAME_DATE_EST"],
        "home_team" : game_info_df.loc[0, "HOME_TEAM_ID"],
        "away_team" : game_info_df.loc[0, "VISITOR_TEAM_ID"],
    }
    all_games.append(game_row)

    boxscore = boxscoretraditionalv3.BoxScoreTraditionalV3(game_id = game_id).get_data_frames()[0]
    players = boxscore.rename(columns={
        "firstName" : "FIRST_NAME",
        "familyName" : "LAST_NAME",
        "teamTricode": "TEAM",
        "points" : "PTS",
        "assists" : "AST",
        "minutes" : "MIN",
        "gameId" : "GAME_ID",
    })
    players["GAME_ID"] = game_id
    players = players[["FIRST_NAME", "LAST_NAME", "TEAM", "PTS", "AST", "MIN", "GAME_ID"]]
    all_players.append(players)


#from records = to take a list of dictionaries ( records ) specifically
games_final = pd.DataFrame.from_records(all_games)
players_final = pd.concat(all_players, ignore_index=True)

games_final.to_csv("./sandbox_data/games_final.csv", index = False)
players_final.to_csv("./sandbox_data/players_final.csv", index = False)