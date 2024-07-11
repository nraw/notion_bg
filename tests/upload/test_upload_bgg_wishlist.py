from notion_bg.upload.upload_bgg_wishlist import *


def test_upload_upload_bgg_wishlist():
    upload_games()



def test_create_bgg_game():
    game_id = 123
    game_data = {
        "wishlistpriority": "1",
        "minplayers": 2,
        "maxplayers": 4,
        "name": "Test Game"
    }
    create_bgg_game(game_id, game_data)

def test_get_bgg_wishlist():
    games = get_bgg_wishlist()
    assert type(games) == dict

def test_get_notion_game_list():
    notion_game_list = get_notion_game_list()
    assert type(notion_game_list) == list

