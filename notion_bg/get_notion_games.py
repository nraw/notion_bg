import json
import os

import requests


def get_notion_games():
    notion_token = os.environ["notion_token"]
    database_id = "14a0eda608be4da284229fe06491ecb7"
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    data = get_notion_data(database_id, headers)
    return data


def get_notion_data(database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.post(url, headers=headers)
    data = res.json()
    has_more = data["has_more"]
    while has_more:
        next_cursor = data["next_cursor"]
        query_data = {"start_cursor": next_cursor}
        res = requests.post(url, headers=headers, data=json.dumps(query_data))
        new_data = res.json()
        data["results"] += new_data["results"]
        has_more = new_data["has_more"]

    return data
