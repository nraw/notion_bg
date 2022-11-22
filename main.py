import requests, json
import fire

#  import argh
from bs4 import BeautifulSoup

from notion_bg.get_notion_games import get_notion_games
from notion_bg.update_notion_game import update_notion_game
from notion_bg.config import conf
from loguru import logger
from notion_bg.get_game_meta import get_game_meta
from notion_bg.download_collections import download_collections


def main(
    games_filter: str = conf["games_filter"],
    data_updates: list = conf["data_updates"],
    bgg_id: int = conf["bgg_id"],
):
    conf["games_filter"] = games_filter
    conf["data_updates"] = data_updates
    conf["bgg_id"] = bgg_id
    logger.info(f"game_filter: {games_filter}")
    logger.info(f"data_updates: {data_updates}")
    if games_filter == "bgg_id":
        logger.info(f"data_updates: {bgg_id}")

    data = get_notion_games()
    selected_games = filter_games(data)
    process_selected_games(selected_games, data)


def filter_games(data):
    assert (
        conf["games_filter"] in conf["games_filters"]
    ), f"Filter '{conf['games_filter']}' not in {conf['games_filters']}"
    results = data["results"]
    selected_games = {}
    for result in results:
        status = result["properties"]["Status"]["select"]["name"]
        if conf["games_filter"] == "new":
            og_input = result["properties"]["OG name"]["rich_text"]
            newly_added = not og_input
            if newly_added:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
        elif conf["games_filter"] == "all":
            bought_or_pass = status in ["Bought", "Pass"]
            if not bought_or_pass:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
        elif conf["games_filter"] == "all_including_bought_passed":
            new_id = result["id"]
            #  new_game = get_notion_name(result)
            selected_games[new_id] = result

        elif conf["games_filter"] == "id":
            if result["id"] == conf["notion_id"]:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
        elif conf["games_filter"] == "bgg_id":
            if result["properties"]["bgg_id"]["number"] == conf["bgg_id"]:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
    logger.info(f"Filtered {len(selected_games)} games")
    return selected_games


def process_selected_games(selected_games, data):
    if selected_games:
        collections = download_collections()
    for new_id, new_game_data in selected_games.items():
        game_meta = get_game_meta(new_id, new_game_data, collections)
        new_game = game_meta
        update_notion_game(new_id, game_meta)


if __name__ == "__main__":
    #  argh.dispatch_command(main)
    fire.Fire(main)
