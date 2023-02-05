import json
import os
from functools import partial

import requests
from loguru import logger

from notion_bg.config import conf
from notion_bg.notion_handlers import (checkbox_handler, multiselect_handler,
                                       number_handler, rich_text_handler,
                                       title_handler, url_handler)

notion_handlers_map = {
    "title": title_handler,
    "text": rich_text_handler,
    "number": number_handler,
    "checkbox": checkbox_handler,
    "url": url_handler,
    "multi": multiselect_handler,
}

variables_map = {
    "Name": "title",
    "OG name": "text",
    "bgg_id": "number",
    "bgg_url": "url",
    "bgg_rating": "number",
    "Num players": "multi",
    "In BGA": "checkbox",
    "In BBB": "checkbox",
    "In Tlama Showroom": "checkbox",
    "In Svet Her": "checkbox",
    "Youtube": "url",
    "Youtube SUSD": "url",
    "Youtube Dice Tower": "url",
    "Tlama": "url",
}


def update_notion_game(new_id, game_meta):
    properties = get_properties(game_meta)
    update_properties(properties, new_id)


def get_properties(game_meta):
    properties = {}
    for property in variables_map:
        if property in conf["data_updates"]:
            if property in game_meta:
                variable = variables_map[property]
                handler = notion_handlers_map[variable]
                value = game_meta[property]
                properties[property] = handler(value)
    return properties


def update_properties(properties, new_id):
    if not properties:
        logger.info("Nothing to update. Skipping")
        return
    headers = get_headers()
    json_data = {"properties": properties}
    response = requests.patch(
        f"https://api.notion.com/v1/pages/{new_id}",
        headers=headers,
        data=json.dumps(json_data),
    )
    logger.info(response.json())


def get_headers():
    notion_token = os.environ["notion_token"]
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    return headers
