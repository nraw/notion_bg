import re
from time import sleep

import requests
from boardgamegeek import BGGApiError, BGGClient
from bs4 import BeautifulSoup
from loguru import logger

from notion_bg.config import conf
from notion_bg.get_collection import get_collection


def get_tlama(bgg_name, new_game_data):
    tlama_meta = None
    if "Tlama" in conf["data_updates"]:
        tlama_backup = new_game_data["properties"]["Tlama Backup"]["url"]
        tlama_current = new_game_data["properties"]["Tlama"]["url"]
        is_manual = tlama_current is not None and tlama_backup != tlama_current
        #  url = f"https://www.tlamagames.com/vyhledavani/?string={bgg_name}"
        games_raw = get_games_raw(bgg_name)
        for first_game in games_raw:
            tlama_meta = get_tlama_game_meta(first_game)
            tlama_meta = check_tlama_meta(
                tlama_meta, tlama_current, tlama_backup, is_manual
            )
            if tlama_meta is not None:
                logger.info(f"Found {tlama_meta['title']}")
                break
    return tlama_meta


def check_tlama_meta(tlama_meta, tlama_current, tlama_backup, is_manual):
    if is_manual:
        if tlama_meta["url"] != tlama_current:
            logger.info("Tlama url was manually meddled with and this is not it")
            tlama_meta = None
        else:
            logger.info("Tlama url was matched with manual entry")
            tlama_meta["url"] = None
    elif "/board-games/" not in tlama_meta["url"]:
        logger.info(f"Skipping wrong url: {tlama_meta['url']}")
        tlama_meta = None
    elif tlama_current is not None:
        tlama_current_url = re.sub(r".*\(", "", tlama_current).replace(")", "")
        if tlama_current_url == tlama_meta["url"]:
            logger.info("Tlama url same as before")
            tlama_meta["url"] = None
    elif tlama_backup is not None:
        tlama_backup_url = re.sub(r".*\(", "", tlama_backup).replace(")", "")
        if tlama_backup_url == tlama_meta["url"]:
            logger.info("Tlama url same as backup.")
            tlama_meta["url"] = None
            tlama_meta["price"] = None
            tlama_meta["availability"] = None
    return tlama_meta


def get_games_raw(bgg_name) -> list:
    url = f"https://www.tlamagames.com/en/search/?string={bgg_name}"
    res = requests.get(url)
    res_html = res.text
    bs = BeautifulSoup(res_html, "lxml")
    games_raw = bs.find_all("div", class_="p")
    return games_raw


def get_tlama_game_meta(first_game) -> dict:
    tlama_name = first_game.find(attrs={"data-micro": "name"}).text.strip()
    # under div with class "price"
    tlama_price = first_game.find("div", class_="price").text.strip()
    tlama_availability = first_game.find("div", class_="availability").text.strip()
    tlama_url_rel = first_game.find("a", attrs={"data-micro": "url"})["href"]
    tlama_url = "https://www.tlamagames.com" + tlama_url_rel
    tlama_meta = dict(
        title=tlama_name,
        url=tlama_url,
        price=tlama_price,
        availability=tlama_availability,
    )
    return tlama_meta


def get_tlama_showroom():
    logger.info("Obtaining Tlama Showroom games")
    bgg = BGGClient()

    games_batch = get_collection(
        bgg, user_name="mirdata", own=True, exclude_subtype="boardgameexpansion"
    )
    tlama_showroom = {game.id: game._data for game in games_batch if "id" in dir(game)}
    tlama_showroom_list = tlama_showroom.keys()
    return tlama_showroom_list
