from loguru import logger

from notion_bg.config import conf
from notion_bg.download_collections import download_collections
from notion_bg.filter_games import filter_games
from notion_bg.get_notion_games import get_notion_games
from notion_bg.process_selected_games import process_selected_games


def main_pipeline():
    logger.info(conf)
    data = get_notion_games()
    selected_games = filter_games(data)
    if not selected_games:
        return
    collections = download_collections()
    process_selected_games(selected_games, collections)
