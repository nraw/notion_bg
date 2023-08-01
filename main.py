import fire
from loguru import logger

from notion_bg.config import conf
from notion_bg.main_pipeline import main_pipeline
from notion_bg.upload.upload_bgg_wishlist import upload_games


def main(
    games_filter: str = conf["games_filter"],
    data_updates: list = conf["data_updates"],
    bgg_id: int = conf["bgg_id"],
):
    conf["games_filter"] = games_filter
    conf["data_updates"] = data_updates
    conf["bgg_id"] = bgg_id
    logger.info(f"game_filter: {games_filter}")
    logger.info(f"data_updates: {data_updates}")
    if games_filter == "bgg_id":
        logger.info(f"data_updates: {bgg_id}")
    upload_games()
    main_pipeline()


if __name__ == "__main__":
    #  argh.dispatch_command(main)
    fire.Fire(main)
