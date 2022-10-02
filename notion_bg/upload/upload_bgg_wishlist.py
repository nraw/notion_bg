import pandas as pd
import json
import requests
from boardgamegeek import BGGClient
from loguru import logger


def upload_games():
    games = get_bgg_wishlist()
    notion_game_list = get_notion_game_list()
    for game_id, game_data in games.items():
        game_name = game_data["name"]
        if game_name not in notion_game_list:
            logger.info(f"Adding {game_name}")
            create_bgg_game(game_id, game_data)
        else:
            logger.info(f"Skipping {game_name}")


def get_bgg_wishlist():
    bgg = BGGClient()
    games_batch = bgg.collection(
        "nraw", wishlist=True, exclude_subtype="boardgameexpansion"
    )
    games = {game.id: game._data for game in games_batch if "id" in dir(game)}
    return games


def get_notion_game_list():
    data = get_notion_games()
    results = data["results"]
    notion_game_list = [
        g["properties"]["Name"]["title"][0]["plain_text"] for g in results
    ]
    return notion_game_list


def create_bgg_game(game_id, game_data):
    states = ["Bought", "Not on Tlama", "Want to buy", "Want to try", "Need more info"]
    state = states[int(game_data["wishlistpriority"])]

    database_id = "14a0eda608be4da284229fe06491ecb7"
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    players = list(range(game_data["minplayers"], game_data["maxplayers"] + 1))
    players_multi_select = [dict(name=str(p)) for p in players]
    bgg_url = "https://boardgamegeek.com/boardgame/" + str(game_id)

    json_data = {
        "parent": {"database_id": "14a0eda608be4da284229fe06491ecb7"},
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
