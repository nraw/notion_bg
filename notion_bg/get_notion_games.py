import json
import os

import requests
from loguru import logger


def get_notion_games():
    notion_token = os.environ["notion_token"]
    database_id = "14a0eda608be4da284229fe06491ecb7"
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2025-09-03",
    }
    data_source_id = get_data_source_id(database_id, headers)
    data = get_notion_data(data_source_id, headers)
    return data


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


def get_notion_data(data_source_id, headers):
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    res = requests.post(url, headers=headers)
    data = res.json()
    has_more = data["has_more"]
    next_cursor = data["next_cursor"]
    while has_more:
        query_data = {"start_cursor": next_cursor}
        res = requests.post(url, headers=headers, data=json.dumps(query_data))
        new_data = res.json()
        data["results"] += new_data["results"]
        has_more = new_data["has_more"]
        next_cursor = new_data["next_cursor"]
    return data
