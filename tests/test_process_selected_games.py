from notion_bg.process_selected_games import *


def test_process_selected_games(selected_games, collections):
    process_selected_games(selected_games, collections)

def get_game_meta(selected_games, collections):
    new_game_data = selected_games[list(selected_games.keys())[0]]
    get_game_meta(new_game_data, collections)
