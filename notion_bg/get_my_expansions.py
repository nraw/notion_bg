from functools import lru_cache

import pandas as pd
from boardgamegeek import BGGApiError, BGGClient
from loguru import logger
from tqdm import tqdm

from notion_bg.get_collection import get_collection


@lru_cache(4)
def get_my_expansions(drop_promo=True, obtain_meta=True):
    logger.info("Obtaining my games")
    bgg = BGGClient()
    nraw_games_list = get_my_games_list(bgg)
    all_expansions = get_expansions(nraw_games_list, bgg)
    expansions_not_owned = filter_owned_expansions(all_expansions, nraw_games_list)
    expansions_and_promos = pd.DataFrame(expansions_not_owned)
    if drop_promo:
        expansions = expansions_and_promos[
            ~expansions_and_promos.name.str.lower().str.contains("promo")
        ]
    else:
        expansions = expansions_and_promos
    if obtain_meta:
        expansions_meta = get_expansions_meta(bgg, expansions)
        return expansions_meta
    else:
        return expansions


def get_my_games_list(bgg, return_feature="bgg_id"):
    games_batch = get_collection(bgg, user_name="nraw", own=True)
    #  games_batch = bgg.collection("nraw", own=True)
    nraw_games = {game.id: game._data for game in games_batch if "id" in dir(game)}
    if return_feature == "bgg_id":
        nraw_games_list = list(nraw_games.keys())
    elif return_feature == "bgg_name":
        nraw_games_list = [g["name"] for g in nraw_games.values()]
    else:
        nraw_games_list = nraw_games
    return nraw_games_list


def get_expansions(nraw_games_list, bgg):
    expansions = []
    for bgg_id in tqdm(nraw_games_list):
        try:
            game_expansions = get_expansions_for_game(bgg_id, bgg)
            expansions.append(game_expansions)
        except BGGApiError as e:
            logger.error(f"{e=}")
    return expansions


def get_expansions_for_game(bgg_id, bgg):
    game = bgg.game(game_id=bgg_id)
    logger.info(f"{game.name=}")
    game_expansions = []
    logger.info(f"Expansions: {len(game.expansions)}")
    for game_expansion in game.expansions:
        game_expansion = game_expansion.data()
        game_expansion["base_game"] = game.name
        game_expansion["base_bgg_id"] = bgg_id
        game_expansion["base_url"] = "https://boardgamegeek.com/boardgame/" + str(
            game_expansion["id"]
        )
        game_expansions += [game_expansion]
    return game_expansions


def filter_owned_expansions(all_expansions, nraw_games_list):
    expansions_not_owned = [e for e in all_expansions if e]
    expansions_not_owned = [
        e
        for es in expansions_not_owned
        for e in es
        if int(e["id"]) not in nraw_games_list
    ]
    return expansions_not_owned


def get_expansions_meta(bgg, expansions):
    expansions_metadata = []
    for expansion_id in tqdm(expansions.id):
        expansion = bgg.game(game_id=expansion_id)
        expansions_metadata += [expansion.data()]
    expansions_meta = pd.DataFrame(expansions_metadata)
    return expansions_meta


def get_plays(bgg):
    plays = bgg.plays("nraw")
    return plays
