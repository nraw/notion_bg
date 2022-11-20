from main import *


def test_main():
    conf["games_filter"] = "bgg_id"
    conf["bgg_id"] = 324345
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
    process_selected_games(selected_games, data)
