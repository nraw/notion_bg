import os
from time import sleep
from urllib.parse import quote

import requests
from boardgamegeek import BGGApiError, BGGClient, BGGItemNotFoundError
from loguru import logger


def get_bgg_data(new_game, bgg_id=None):
    bgg = BGGClient()
    if bgg_id:
        logger.info(f"Getting bgg info via id - {new_game}")
        try:
            game = bgg.game(game_id=bgg_id)
        except BGGApiError:
            logger.error("Failed to connect to bgg, trying again")
            sleep(2)
            game = bgg.game(game_id=bgg_id)

    else:
        try:
            logger.info(f"Getting bgg info via name - {new_game}")
            game = bgg.game(new_game)
        except Exception:
            logger.info(f"Getting bgg info via google - {new_game}")
            bgg_id = get_bgg_url(new_game)
            game = bgg.game(game_id=bgg_id)
    bgg_name = game.name
    if new_game != bgg_name:
        logger.warning(f"Name change: {new_game} -> {bgg_name}")
    else:
        logger.info(f"Found game: {bgg_name}")
    bgg_id = game.id
    bgg_url = "https://boardgamegeek.com/boardgame/" + str(bgg_id)
    bgg_thumbnail = game.thumbnail
    players = list(range(game.min_players, game.max_players + 1))
    bgg_rating = game.rating_average
    bgg_meta = dict(
        bgg_name=bgg_name,
        bgg_id=bgg_id,
        bgg_url=bgg_url,
        bgg_thumbnail=bgg_thumbnail,
        players=players,
        bgg_rating=bgg_rating,
    )
    return bgg_meta


def check_bgg_id(new_game_data):
    bgg_id = new_game_data["properties"]["bgg_id"]["number"]
    if bgg_id:
        logger.info("bgg id exists")
    else:
        logger.info("bgg id doesn't exist")
    return bgg_id


def get_bgg_url(new_game):
    wishlist_scanner_url = os.environ["wishlist_scanner_url"]
    url = wishlist_scanner_url + "?query=" + quote(new_game)
    res = requests.get(url)
    bgg_id = res.text
    return bgg_id
