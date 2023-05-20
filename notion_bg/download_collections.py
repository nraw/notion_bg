from notion_bg.config import conf
from notion_bg.get_bbb_games import get_bbb_games
from notion_bg.get_bga_games import get_bga_games
from notion_bg.get_svet_her import get_svet_her
from notion_bg.get_tlama import get_tlama_showroom

collections_map = {
    "In BGA": get_bga_games,
    "In BBB": get_bbb_games,
    "In Tlama Showroom": get_tlama_showroom,
    "In Svet Her": get_svet_her,
}


def download_collections():
    collections = {}
    for collection_name in collections_map:
        if collection_name in conf["data_updates"]:
            collections[collection_name] = collections_map[collection_name]()
    return collections
