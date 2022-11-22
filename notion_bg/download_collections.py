from notion_bg.config import conf
from notion_bg.get_bga_games import get_bga_games
from notion_bg.get_bbb_games import get_bbb_games
from notion_bg.get_svet_her import get_svet_her
from notion_bg.get_tlama import get_tlama_showroom
from loguru import logger

collection_functions = {
    "In BGA": get_bga_games,
    "In BBB": get_bbb_games,
    "In Tlama Showroom": get_tlama_showroom,
    "In Svet Her": get_svet_her,
}


def download_collections():
    collections = {}
    for data_update in conf["data_updates"]:
        if data_update in collection_functions:
            collection_function = collection_functions[data_update]
            collections[data_update] = collection_function()
    return collections
