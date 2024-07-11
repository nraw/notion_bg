import re

import requests
from bs4 import BeautifulSoup
from loguru import logger

from notion_bg.config import conf


def get_igraj_si(bgg_name):
    igraj_si_meta = None
    if "Igraj.si" in conf["data_updates"]:
        #  url = f"https://www.tlamagames.com/vyhledavani/?string={bgg_name}"
        games_raw = get_igraj_si_raw(bgg_name)
        for game_raw in games_raw:
            igraj_si_meta = get_igraj_si_game_meta(game_raw, bgg_name)
            if igraj_si_meta is not None:
                logger.info(f"Found {igraj_si_meta['title']} on igraj.si")
                break
    if igraj_si_meta is None:
        logger.info(f"igraj.si meta not found: {bgg_name}")
    return igraj_si_meta


def get_igraj_si_raw(bgg_name) -> list:
    url = f"https://www.igraj.si/index.php?route=product/search&search={bgg_name}"
    res = requests.get(url)
    bs = BeautifulSoup(res.text, "html.parser")
    games_raw = bs.find_all("div", class_="product-list-item")
    return games_raw


def get_igraj_si_game_meta(game_raw, bgg_name):
    igraj_si_meta = {}
    title = game_raw.find("h4", class_="name").text
    if title.upper() != bgg_name.upper():
        return None
    igraj_si_meta["title"] = title
    url = game_raw.find("a")["href"]
    igraj_si_meta["url"] = url
    price = game_raw.find("span", class_="price-new")
    if price is None:
        price = game_raw.find("p", class_="price").text
    else:
        price = price.text
    price = price.strip()
    price = re.sub(r" .*", "", price)
    igraj_si_meta["price"] = price
    return igraj_si_meta
