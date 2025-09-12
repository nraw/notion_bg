import json
import os

import pandas as pd
import requests
from loguru import logger


def upload_games():
    games = pd.read_csv("data/games.csv")
    games = games.set_index("title")["description"].to_dict()
    for game, description in games.items():
        create_game(game, description)


def get_data_source_id(database_id, headers):
    """Get the first data_source_id for a given database_id"""
    url = f"https://api.notion.com/v1/databases/{database_id}"
    res = requests.get(url, headers=headers)
    database_data = res.json()
    
    if 'data_sources' in database_data and len(database_data['data_sources']) > 0:
        data_source_id = database_data['data_sources'][0]['id']
        logger.info(f"Found data_source_id: {data_source_id} for database: {database_id}")
        return data_source_id
    else:
        logger.error(f"No data sources found for database: {database_id}")
        raise Exception(f"No data sources found for database: {database_id}")


def create_game(game, description):
    notion_token = os.environ["notion_token"]

    database_id = "14a0eda608be4da284229fe06491ecb7"
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03",
    }
    data_source_id = get_data_source_id(database_id, headers)

    json_data = {
        "parent": {"data_source_id": data_source_id},
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
