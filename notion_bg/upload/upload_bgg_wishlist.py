import os

import requests
from boardgamegeek import BGGClient
from loguru import logger

from notion_bg.get_collection import get_collection
from notion_bg.get_notion_games import get_notion_games


def upload_games():
    logger.info("Uploading games from bgg wishlist")
    games = get_bgg_wishlist()
    notion_game_list = get_notion_game_list()
    missing_games = get_missing_games(games, notion_game_list)
    logger.info(f"Adding {len(missing_games)} games")
    for game_id, game_data in missing_games.items():
        game_name = game_data["name"]
        logger.info(f"Adding {game_name}")
        create_bgg_game(game_id, game_data)


def get_bgg_wishlist():
    bgg = BGGClient()
    games_batch = get_collection(bgg, user_name="nraw", wishlist=True)
    games = {game.id: game._data for game in games_batch if "id" in dir(game)}
    return games


def get_notion_game_list():
    data = get_notion_games()
    results = data["results"]
    notion_game_list = [g["properties"]["bgg_id"]["number"] for g in results]
    return notion_game_list


def get_missing_games(games, notion_game_list):
    missing_games = {
        game_id: game_data
        for game_id, game_data in games.items()
        if game_id not in notion_game_list
    }
    return missing_games


def create_bgg_game(game_id, game_data):
    states = [
        "Wakalaka",
        "Want to buy",
        "Want to try",
        "Need more info",
        "Need more info",
        "Pass",
    ]
    state = states[int(game_data["wishlistpriority"])]

    database_id = "14a0eda608be4da284229fe06491ecb7"
    notion_token = os.environ["notion_token"]
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    players = list(range(game_data["minplayers"], game_data["maxplayers"] + 1))
    players_multi_select = [dict(name=str(p)) for p in players]
    bgg_url = "https://boardgamegeek.com/boardgame/" + str(game_id)

    json_data = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {"title": [{"text": {"content": game_data["name"]}}]},
            "Status": {"select": {"name": state}},
            "bgg_id": {"number": game_id},
            "bgg_url": {"url": bgg_url},
            "Num players": {"multi_select": players_multi_select},
        },
    }

    response = requests.post(
        "https://api.notion.com/v1/pages", headers=headers, json=json_data
    )
    print(game_data["name"])
    print(response)
