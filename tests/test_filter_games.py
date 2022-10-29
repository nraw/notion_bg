from main import *


def test_games_filter_all():
    conf["games_filter"] = "all"
    conf["data_updates"] = []
    data = get_notion_games()
    selected_games = filter_games(data)
    assert type(selected_games) == dict


def test_games_filter_bgg_id():
    conf["games_filter"] = "bgg_id"
    conf["bgg_id"] = 98778
    data = get_notion_games()
    selected_games = filter_games(data)
    assert type(selected_games) == dict
