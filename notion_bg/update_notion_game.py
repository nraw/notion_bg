import os
import requests
from notion_bg.config import conf
import json
from loguru import logger


def update_notion_game(new_id, new_game, game_meta):
    notion_token = os.environ["notion_token"]

    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }
    properties = {}
    if "Name" in conf["data_updates"]:
        properties["Name"] = {
            "title": [{"text": {"content": game_meta["bgg_meta"]["bgg_name"]}}]
        }
    if "OG name" in conf["data_updates"]:
        properties["OG name"] = {"rich_text": [{"text": {"content": new_game}}]}
    if "bgg_id" in conf["data_updates"]:
        properties["bgg_id"] = {"number": game_meta["bgg_meta"]["bgg_id"]}
    if "bgg_url" in conf["data_updates"]:
        properties["bgg_url"] = {"url": game_meta["bgg_meta"]["bgg_url"]}
    if "bgg_rating" in conf["data_updates"]:
        properties["bgg_rating"] = {"number": game_meta["bgg_meta"]["bgg_rating"]}
    if "Num players" in conf["data_updates"]:
        players_multi_select = [
            dict(name=str(p)) for p in game_meta["bgg_meta"]["players"]
        ]
        properties["Num players"] = {"multi_select": players_multi_select}
    if "In BGA" in conf["data_updates"]:
        properties["In BGA"] = {"checkbox": game_meta["in_bga"]}
    if "In BBB" in conf["data_updates"]:
        properties["In BBB"] = {"checkbox": game_meta["in_bbb"]}
    if "In Tlama Showroom" in conf["data_updates"]:
        properties["In Tlama Showroom"] = {"checkbox": game_meta["in_tlama_showroom"]}
    if "In Svet Her" in conf["data_updates"]:
        properties["In Svet Her"] = {"checkbox": game_meta["in_svet_her"]}
    if "Youtube" in conf["data_updates"]:
        yt_general = get_hyperlink("general", game_meta)
        properties["Youtube"] = {"url": yt_general}
    if "Youtube SUSD" in conf["data_updates"]:
        yt_susd = get_hyperlink("susd", game_meta)
        properties["Youtube SUSD"] = {"url": yt_susd}
    if "Youtube Dice Tower" in conf["data_updates"]:
        yt_dt = get_hyperlink("dt", game_meta)
        properties["Youtube Dice Tower"] = {"url": yt_dt}
    if "Tlama" in conf["data_updates"]:
        tlama = get_hyperlink("tlama_meta", game_meta)
        if tlama:
            properties["Tlama"] = {"url": tlama}
            properties["Tlama Backup"] = {"url": tlama}
    if properties:
        json_data = {"properties": properties}
        response = requests.patch(
            f"https://api.notion.com/v1/pages/{new_id}",
            headers=headers,
            data=json.dumps(json_data),
        )
        logger.info(response.json())
    else:
        logger.info("Nothing to update. Skipping")


def get_hyperlink(yt_channel, game_meta, meta="yt_meta"):
    if yt_channel == "tlama_meta":
        if game_meta[yt_channel]:
            yt_url = f"[{game_meta['tlama_meta']['title']}]({game_meta['tlama_meta']['url']})"
        else:
            yt_url = None
    else:
        if game_meta[meta][yt_channel]:
            yt_url = f"[{game_meta[meta][yt_channel]['title']}]({game_meta[meta][yt_channel]['url']})"
        else:
            yt_url = None
    return yt_url
