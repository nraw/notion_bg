from loguru import logger

from notion_bg.get_geeklist import get_geeklist


def get_bga_games():
    logger.info("Obtaining BGA games")
    bga_geeklist_id = "252354"  # BGA
    bga_games = get_geeklist(bga_geeklist_id)
    bga_games = [int(game) for game in bga_games]
    return bga_games
