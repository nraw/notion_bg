import os
import requests

from boardgamegeek import BGGClient, BGGItemNotFoundError
from loguru import logger
from urllib.parse import quote

from notion_bg.get_bgg_game import get_bgg_game


def get_bgg_data(new_game, bgg_id=None):
    game = get_bgg_game(new_game, bgg_id)
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


def get_bgg_name(new_game, bgg_id):
    game = get_bgg_game(new_game, bgg_id)
    bgg_name = game.name
    if new_game != bgg_name:
        logger.warning(f"Name change: {new_game} -> {bgg_name}")
    else:
        logger.info(f"Found game: {bgg_name}")
    return bgg_name


def get_bgg_id(new_id, new_game_data):
    bgg_id = check_bgg_id(new_game)
    game = get_bgg_game(new_game, bgg_id)
    bgg_id = game.id
    return bgg_id


def get_bgg_url(new_game, bgg_id):
    game = get_bgg_game(new_game, bgg_id)
    bgg_url = "https://boardgamegeek.com/boardgame/" + str(bgg_id)
    return bgg_url


def get_bgg_thumbnail(new_game, bgg_id):
    game = get_bgg_game(new_game, bgg_id)
    bgg_thumbnail = game.thumbnail
    return bgg_thumbnail


def get_bgg_rating(new_game, bgg_id):
    game = get_bgg_game(new_game, bgg_id)
    bgg_rating = game.rating_average
    return bgg_rating


def get_bgg_players(new_game, bgg_id):
    game = get_bgg_game(new_game, bgg_id)
    bgg_players = list(range(game.min_players, game.max_players + 1))
    return bgg_players


def check_bgg_id(new_id, new_game_data):
    bgg_id = new_game_data["properties"]["bgg_id"]["number"]
    if bgg_id:
        logger.info("bgg id exists")
    else:
        logger.info("bgg id doesn't exist")
    return bgg_id
