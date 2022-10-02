import pandas as pd
import json
import requests


def upload_games():
    games = pd.read_csv("data/games.csv")
    games = games.set_index("title")["description"].to_dict()
    for game, description in games.items():
        create_game(game, description)


def create_game(game, description):

    database_id = "14a0eda608be4da284229fe06491ecb7"
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    json_data = {
        "parent": {"database_id": "14a0eda608be4da284229fe06491ecb7"},
        "properties": {
            "Name": {"title": [{"text": {"content": game}}]},
            "Status": {"select": {"name": "Need more info"}},
            "desc": {"rich_text": [{"text": {"content": description}}]},
        },
    }

    response = requests.post(
        "https://api.notion.com/v1/pages", headers=headers, json=json_data
    )
    print(game)
    print(response)
