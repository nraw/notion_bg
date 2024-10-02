import numpy as np
import pandas as pd
from boardgamegeek import BGGClient
from tqdm import tqdm

from notion_bg.essen_site import get_old_essen_games
from notion_bg.get_my_expansions import get_my_games_list


def get_sizes():
    my_essen_games = get_old_essen_games()
    bgg = BGGClient()
    nraw_games_list = get_my_games_list(bgg, return_feature="bgg_id")
    games = [
        bgg.game(game_id=bgg_id, versions=True) for bgg_id in tqdm(nraw_games_list)
    ]
    games_data = pd.concat([get_size(g) for g in games])
    weird_games = ["Hive Pocket", "No Thanks!", "Love Letter", "Turncoats"]
    games_data = games_data[~games_data.game.isin(weird_games)]
    games_data = games_data.reset_index()

    #  bought_ids = [204466, 82168, 197443, 12942, 113294, 174614, 182172, 300731, 242343]
    bidding_ids = [game.bgg_id for game in my_essen_games["bidding"]]
    bought_ids = [game.bgg_id for game in my_essen_games["bought"]]
    bought_ids = bought_ids + bidding_ids
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
        create_pair_report(pair)


def create_pair_report(pair):
    width_0 = np.round(inch_to_cm(pair[0]["width"]))
    length_0 = np.round(inch_to_cm(pair[0]["length"]))
    depth_0 = np.round(inch_to_cm(pair[0]["depth"]))
    width_1 = np.round(inch_to_cm(pair[1]["width"]))
    length_1 = np.round(inch_to_cm(pair[1]["length"]))
    depth_1 = np.round(inch_to_cm(pair[1]["depth"]))

    pair0size = str(width_0) + "x" + str(length_0) + "x" + str(depth_0)
    pair1size = str(width_1) + "x" + str(length_1) + "x" + str(depth_1)
    print(pair[1]["game"], " - ", pair[0]["game"])
    print(pair1size, " - ", pair0size)
    response_text = create_pair_text(
        width_0, length_0, depth_0, width_1, length_1, depth_1
    )
    if response_text:
        print(response_text)
    print()


def create_pair_text(width_0, length_0, depth_0, width_1, length_1, depth_1):
    text_format = []
    if width_0 < width_1:
        text_format += ["wider"]
    elif width_0 > width_1:
        text_format += ["narrower"]
    if length_0 < length_1:
        text_format += ["longer"]
    elif length_0 > length_1:
        text_format += ["shorter"]
    if depth_0 < depth_1:
        text_format += ["deeper"]
    elif depth_0 > depth_1:
        text_format += ["shallower"]
    text_response = " ".join(text_format)
    return text_response


def inch_to_cm(inch):
    return inch * 2.54


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
