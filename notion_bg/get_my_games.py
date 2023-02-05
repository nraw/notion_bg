from functools import lru_cache

import pandas as pd
from boardgamegeek import BGGClient
from loguru import logger
from tqdm import tqdm


def get_my_games():
    logger.info("Obtaining my games")
    bgg = BGGClient()
    nraw_games_list = get_my_games_list(bgg)
    all_expansions = get_expansions(nraw_games_list, bgg)
    expansions_not_owned = filter_owned_expansions(all_expansions, nraw_games_list)
    expansions = pd.DataFrame(expansions_not_owned)
    expansions = expansions[~expansions.name.str.lower().str.contains("promo")]


def get_my_games_list(bgg):
    games_batch = bgg.collection("nraw", own=True)
    nraw_games = {game.id: game._data for game in games_batch if "id" in dir(game)}
    nraw_games_list = list(nraw_games.keys())
    return nraw_games_list


def get_expansions(nraw_games_list, bgg):
    expansions = []
    for bgg_id in tqdm(nraw_games_list):
        game_expansions = get_expansions_for_game(bgg_id, bgg)
        expansions.append(game_expansions)
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
