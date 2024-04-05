from notion_bg.config import conf
from notion_bg.main_pipeline import *


def test_main_new():
    conf["games_filter"] = "new"
    conf["data_updates"] = conf["all_updates"]
    #  conf["data_updates"] = [
    #      "Name",
    #      "OG name",
    #      "bgg_id",
    #      "bgg_url",
    #      "bgg_rating",
    #      "Num players",
    #      "In BBB",
    #      "In Svet Her",
    #      "In Tlama Showroom",
    #      "In BGA",
    #      "Youtube",
    #      "Youtube SUSD",
    #      "Youtube Dice Tower",
    #      "Tlama",
    #  ]
    data = get_notion_games()
    selected_games = filter_games(data)
    collections = download_collections()
    process_selected_games(selected_games, collections)


def test_main_bgg_id():
    conf["games_filter"] = "bgg_id"
    conf["bgg_id"] = 254640
    conf["data_updates"] = conf["all_updates"]
    conf["data_updates"] = [
        "Name",
        "OG name",
        "bgg_id",
        "bgg_url",
        "bgg_rating",
        "Num players",
        "In BBB",
        "In Svet Her",
        "In Tlama Showroom",
        "In BGA",
        "Youtube",
        "Youtube SUSD",
        "Youtube Dice Tower",
        "Tlama",
    ]
    data = get_notion_games()
    selected_games = filter_games(data)
    collections = download_collections()
    new_game_data = next(iter(selected_games.values()))
    game_meta = get_game_meta(new_game_data, collections)
    process_selected_games(selected_games, collections)


def test_main_specific():
    conf["games_filter"] = "all"
    conf["data_updates"] = [
        #  "Name",
        #  "OG name",
        #  "bgg_id",
        #  "bgg_url",
        #  "bgg_rating",
        #  "Num players",
        "In BBB",
        #  "In Svet Her",
        "In Tlama Showroom",
        #  "In BGA",
        #  "Youtube",
        #  "Youtube SUSD",
        #  "Youtube Dice Tower",
        #  "Tlama",
    ]
    data = get_notion_games()
    selected_games = filter_games(data)
    collections = download_collections()
    process_selected_games(selected_games, collections)


def test_main_tlama():
    conf["games_filter"] = "all"
    conf["data_updates"] = ["Tlama", "Tlama Price", "Tlama Availability"]
    data = get_notion_games()
    selected_games = filter_games(data)
    collections = download_collections()
    process_selected_games(selected_games, collections)
