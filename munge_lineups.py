import pandas as pd

pbp_df = pd.read_csv("42000232.csv")
pbp_df = pbp_df.sort_values("eventnum")

home_players = [
    "home_player_1_id",
    "home_player_2_id",
    "home_player_3_id",
    "home_player_4_id",
    "home_player_5_id",
]
away_players = [
    "away_player_1_id",
    "away_player_2_id",
    "away_player_3_id",
    "away_player_4_id",
    "away_player_5_id",
]
home_players_name = [
    "home_player_1",
    "home_player_2",
    "home_player_3",
    "home_player_4",
    "home_player_5",
]
away_players_name = [
    "away_player_1",
    "away_player_2",
    "away_player_3",
    "away_player_4",
    "away_player_5",
]
pbp_df["home_lineup_key"] = [
    ", ".join(sorted(list(map(str, x)))) for x in pbp_df[home_players].values
]
pbp_df["away_lineup_key"] = [
    ", ".join(sorted(list(map(str, x)))) for x in pbp_df[away_players].values
]

home_columns = [
    pbp_df[[x, y]].rename(columns={x: "id", y: "name"})
    for x, y in zip(home_players, home_players_name)
]
away_columns = [
    pbp_df[[x, y]].rename(columns={x: "id", y: "name"})
    for x, y in zip(away_players, away_players_name)
]
player_list = home_columns + away_columns
player_df = pd.concat(player_list)
player_df = player_df.drop_duplicates()

home_lineup_time_df = (
    pbp_df[["home_lineup_key", "event_length"]]
    .groupby("home_lineup_key")
    .sum("event_length")
    .reset_index()
)
away_lineup_time_df = (
    pbp_df[["away_lineup_key", "event_length"]]
    .groupby("away_lineup_key")
    .sum("event_length")
    .reset_index()
)
home_lineup_time_df = home_lineup_time_df[home_lineup_time_df["event_length"] > 0]
away_lineup_time_df = away_lineup_time_df[away_lineup_time_df["event_length"] > 0]
home_lineup_time_df["names"] = home_lineup_time_df["home_lineup_key"].map(
    lambda x: [
        player_df["name"][player_df["id"] == int(y)].values[0] for y in x.split(",")
    ]
)
away_lineup_time_df["names"] = away_lineup_time_df["away_lineup_key"].map(
    lambda x: [
        player_df["name"][player_df["id"] == int(y)].values[0] for y in x.split(",")
    ]
)

away_lineup_time_df.to_csv("away_lineups.csv")
home_lineup_time_df.to_csv("home_lineups.csv")
