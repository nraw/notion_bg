from notion_bg.update_notion_game import *


def test_update_notion_game():
    new_id = "514465c3-e878-4c4b-93c4-4106b0d94bc7"
    game_meta = {
        "bgg_name": "Hanabi",
        "bgg_id": 98778,
        "Name": "Hanabi",
        "Tlama": {
            "title": "Hanabi",
            "url": None,
            "price": "€10,75",
            "availability": "In stock at the supplier",
        },
    }
    update_notion_game(new_id, game_meta)


def test_get_properties():
    game_meta = {
        "bgg_name": "Hanabi",
        "bgg_id": 98778,
        "Name": "Hanabi",
        "Tlama": {
            "title": "Hanabi",
            "url": None,
        },
        "Tlama Price": "€10,75",
        "Tlama Availability": "In stock at the supplier",
    }
    properties = get_properties(game_meta)
    assert type(properties) == dict


def test_update_properties():
    new_id = "514465c3-e878-4c4b-93c4-4106b0d94bc7"
    properties = {
        "Tlama Price": {"rich_text": [{"text": {"content": "€10,75"}}]},
        "Tlama Availability": {
            "rich_text": [{"text": {"content": "In stock at the supplier"}}]
        },
    }
    update_properties(properties, new_id)
