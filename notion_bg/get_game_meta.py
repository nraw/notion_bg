from notion_bg.get_bgg_data import get_bgg_data, check_bgg_id
from notion_bg.get_tlama import get_tlama
from notion_bg.get_youtube_urls import get_youtube_metas
from loguru import logger
from functools import lru_cache

slow_functions = {"In BBB", "In Svet Her", "In Tlama Showroom", "In BGA"}

fast_functions = {
    "Youtube": (get_youtube_meta, ["bgg_name"]),
    "bgg_id": (get_bgg_id, ["new_id", "new_game_data"]),
    "bgg_url": (get_bgg_url, ["new_game", "bgg_id"]),
    "bgg_thumbnail": (get_bgg_thumbnail, ["new_game", "bgg_id"]),
    "bgg_rating": (get_bgg_rating, ["new_game", "bgg_id"]),
    "bgg_players": (get_bgg_players, ["new_game", "bgg_id"]),
    # TODO: moar stuff
}
#  'Youtube SUSD',
#  'Youtube Dice Tower',
#  'Tlama'}


def get_game_meta(new_id, new_game_data, collections):
    game_meta = dict(
        new_id=new_id, new_game_data=new_game_data, collections=collections
    )
    game_meta["new_game"] = get_notion_name(new_game_data)
    logger.info(f"Processing {new_game}")
    game_meta["bgg_id"] = check_bgg_id(new_id, new_game_data)
    bgg_meta = get_bgg_data(new_game, bgg_id)
    bgg_name = bgg_meta["bgg_name"]
    bgg_id = bgg_meta["bgg_id"]
    in_bga = check_in_collection(bgg_id, "In BGA", collections)
    in_tlama_showroom = check_in_collection(bgg_id, "In Tlama Showroom", collections)
    in_bbb = check_in_collection(bgg_name, "In BBB", collections)
    in_svet_her = check_in_collection(bgg_id, "In Svet Her", collections)
    yt_meta = get_youtube_metas(bgg_name)
    tlama_meta = get_tlama(bgg_name, new_game_data)
    game_meta = dict(
        bgg_meta=bgg_meta,
        in_bga=in_bga,
        in_tlama_showroom=in_tlama_showroom,
        in_bbb=in_bbb,
        in_svet_her=in_svet_her,
        yt_meta=yt_meta,
        tlama_meta=tlama_meta,
        og_name=new_game,
    )
    return game_meta


def get_notion_name(game):
    game_name = game["properties"]["Name"]["title"][0]["plain_text"]
    return game_name


@lru_cache()
def get_fast_meta_information(data_update, game_meta):
    func_tuple = fast_functions[data_update]
    f = func_tuple[0]
    param_names = func_tuple[1]
    params = {p: game_meta[p] for p in param_names}
    game_meta[data_update] = f(**params)
    return game_meta


def check_in_collection(game_info, collection, collections):
    if collection in conf["data_updates"]:
        in_collection = game_info in collections[collection]
    else:
        in_collection = None
    return in_collection
