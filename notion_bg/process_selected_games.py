from loguru import logger

from notion_bg.config import conf
from notion_bg.get_bgg_data import check_bgg_id, get_bgg_data
from notion_bg.get_igraj_si import get_igraj_si
from notion_bg.get_tabletop_finder import get_tabletop_finder
from notion_bg.get_tlama import get_tlama
from notion_bg.get_youtube_urls import get_youtube_meta
from notion_bg.update_notion_game import update_notion_game

game_info_map = {
    "In BGA": "bgg_id",
    "In BBB": "bgg_id",
    "In Tlama Showroom": "bgg_id",
    "In Svet Her": "bgg_name",
}


def process_selected_games(selected_games, collections):
    for new_id, new_game_data in selected_games.items():
        try:
            game_meta = get_game_meta(new_game_data, collections)
            update_notion_game(new_id, game_meta)
        except Exception as e:
            logger.error(f"Failed to process {new_id}: {e}")


def get_game_meta(new_game_data, collections):
    new_game = get_notion_name(new_game_data)
    logger.info(f"Processing {new_game}")
    bgg_id = check_bgg_id(new_game_data)
    bgg_meta = get_bgg_data(new_game, bgg_id)
    game_meta = bgg_meta
    game_meta["Name"] = bgg_meta["bgg_name"]
    game_meta["Num players"] = bgg_meta["players"]
    for collection_name in game_info_map:
        game_info = bgg_meta[game_info_map[collection_name]]
        game_meta[collection_name] = check_in_collection(
            game_info, collection_name, collections
        )
    game_meta["Tabletop Finder"] = get_tabletop_finder(bgg_meta["bgg_name"])
    tlama_meta = get_tlama(bgg_meta["bgg_name"], new_game_data)
    if tlama_meta:
        if tlama_meta["price"]:
            game_meta["Tlama Price"] = tlama_meta["price"]
        if tlama_meta["availability"]:
            game_meta["Tlama Availability"] = tlama_meta["availability"]
        if tlama_meta["url"]:
            game_meta["Tlama"] = tlama_meta
            game_meta["Tlama Backup"] = tlama_meta
    yt_meta = get_youtube_meta(bgg_meta["bgg_name"])
    igraj_si_meta = get_igraj_si(bgg_meta["bgg_name"])
    if igraj_si_meta:
        game_meta["Igraj.si"] = igraj_si_meta["url"]
        game_meta["Igraj.si Price"] = igraj_si_meta["price"]

    if yt_meta:
        game_meta.update(yt_meta)
    game_meta["OG name"] = new_game
    return game_meta


def get_notion_name(game):
    game_name = game["properties"]["Name"]["title"][0]["plain_text"]
    return game_name


def check_in_collection(game_info, collection_name, collections):
    if collection_name in conf["data_updates"]:
        in_collection = game_info in collections[collection_name]
    else:
        in_collection = None
    return in_collection
