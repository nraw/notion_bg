import numpy as np
import pandas as pd
from boardgamegeek import BGGClient
from tqdm import tqdm


def get_sizes():
    bgg = BGGClient()
    nraw_games_list = get_my_games_list(bgg, return_feature="bgg_id")
    games = [
        bgg.game(game_id=bgg_id, versions=True) for bgg_id in tqdm(nraw_games_list)
    ]
    games_data = pd.concat([get_size(g) for g in games])
    games_data = games_data[games_data.game != "Hive Pocket"]
    games_data = games_data.reset_index()
    available_data = games_data.copy()

    bought_ids = [204466, 82168, 197443, 12942, 113294, 174614, 182172, 300731, 242343]
    bought_games = [
        bgg.game(game_id=bgg_id, versions=True) for bgg_id in tqdm(bought_ids)
    ]
    bought_data = pd.concat([get_size(g) for g in bought_games])

    bought_data = bought_data.sort_values("size", ascending=False)

    available_data = games_data.copy()
    pairs = []
    for _, bought_game in bought_data.iterrows():
        differences = (
            available_data[["width", "length", "depth"]]
            - bought_game[["width", "length", "depth"]]
        )
        differences = differences.abs().sum(axis=1)
        differences = differences.sort_values()
        least_different = differences.index[0]
        least_different_game = available_data.loc[least_different]
        available_data = available_data.drop(least_different)
        pairs.append((least_different_game, bought_game))
    for pair in pairs:
        pair0size = (
            str(np.round(pair[0]["width"], 1))
            + "x"
            + str(np.round(pair[0]["length"], 1))
            + "x"
            + str(np.round(pair[0]["depth"], 1))
        )
        pair1size = (
            str(np.round(pair[1]["width"], 1))
            + "x"
            + str(np.round(pair[1]["length"], 1))
            + "x"
            + str(np.round(pair[1]["depth"], 1))
        )
        print(pair[1]["game"], " - ", pair[0]["game"])
        print(pair1size, " - ", pair0size)


def get_size(g):
    versions = g.data()["versions"]
    games_df = pd.DataFrame(versions)
    games_df["game"] = g.name
    games_df["size"] = games_df["width"] + games_df["length"] + games_df["depth"]

    english_games_df = games_df[games_df.language == "English"]
    if len(english_games_df):
        games_df = english_games_df
    game_df = games_df[games_df["size"] == games_df["size"].max()].iloc[:1]
    return game_df
