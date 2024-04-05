from notion_bg.get_tlama import *


def test_get_tlama():
    bgg_name = "Cat in the box"
    new_game_data = {
        "properties": {"Tlama": {"url": None}, "Tlama Backup": {"url": None}}
    }
    conf["data_updates"] = ["Tlama"]
    tlama_meta = get_tlama(bgg_name, new_game_data)
    assert type(tlama_meta) in [dict, None]
    assert type(tlama_meta) == dict


def test_get_tlama_manual():
    bgg_name = "Hanabi"
    new_game_data = {
        "properties": {"Tlama": {"url": None}, "Tlama Backup": {"url": None}}
    }
    conf["data_updates"] = ["Tlama"]
    tlama_meta = get_tlama(bgg_name, new_game_data)
    new_game_data = {
        "properties": {
            "Tlama": {"url": None},
            "Tlama Backup": {"url": tlama_meta["url"]},
        }
    }
    new_tlama_meta = get_tlama(bgg_name, new_game_data)
    assert new_tlama_meta is None


def test_get_tlama_with_correct():
    bgg_name = "Hanabi"
    new_game_data = {
        "properties": {
            "Tlama": {"url": "https://www.tlamagames.com/en/board-games/hanabio/"},
            "Tlama Backup": {"url": "[hanabi](something)"},
        }
    }
    new_tlama_meta = get_tlama(bgg_name, new_game_data)
