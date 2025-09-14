import pandas as pd
from nba_api.stats.static import teams

def get_teamId_for_player_data(player_data):
    """
    Adding a TEAM_ID column to the player_data based on the MATCHUP column.
    Dropping the
    :param player_data:
        player data (pd.DataFrame): Must contain a 'MATCHUP' column
                                                        with values like 'GSW vs LAL' or 'BOS @ LAL'
    :return:player_data:
        The player_data with a TEAM_ID column added
    """
    all_teams = teams.get_teams()
    abbr_to_id = {t["abbreviation"]: t["id"] for t in all_teams}

    player_data["Team_ID"] = player_data["MATCHUP"].str.split(" ").str[0].map(abbr_to_id)
    player_data = player_data.drop(columns=["MATCHUP"])
    return player_data


def get_home_visitor_data(df):
    """
    Adds a HOME_VISITOR column:
        1 = Home game
        0 = Away game
    Based on the MATCHUP column (which looks like 'GSW vs LAL' or 'LAL @ BOS').
    """
    df["HOME_VISITOR"] = df["MATCHUP"].str.contains("@").astype(int).apply(lambda x: 0 if x == 1 else 1)
    return df


player_data = pd.read_csv("../../data/raw/players/player_game_log_2023-24.csv")
team_data = pd.read_csv("../../data/raw/teams/team_game_log_2023-24.csv")

# Grab the data necessary to construct the features we want our model to classify by
player_data = player_data[["Game_ID", "MATCHUP", "Player_ID", "PTS", "AST", "MIN", "REB","TOV"]]
team_data = team_data[["TEAM_ID", "PTS", "AST", "MIN", "REB","TOV","MATCHUP"]]


# get the visitor or home data
player_data = get_home_visitor_data(player_data)
team_data = get_home_visitor_data(team_data)

# Get the Team_id for player_data
player_data = get_teamId_for_player_data(player_data)



print(player_data.head())
print(team_data.head())