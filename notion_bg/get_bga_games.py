import requests
from bs4 import BeautifulSoup
from loguru import logger


def get_bga_games():
    logger.info("Obtaining BGA games")
    bga_geeklist_id = "252354"  # BGA
    bga_games = get_geeklist(bga_geeklist_id)
    bga_games = [int(game) for game in bga_games]
    return bga_games


def get_geeklist(geeklist_id):
    geeklist_url = f"https://www.boardgamegeek.com/xmlapi/geeklist/{geeklist_id}"
    res = requests.get(geeklist_url)
    xml_content = res.content
    bs = BeautifulSoup(xml_content, "lxml")
    items = bs.find_all("item")
    geeklist = [item.get("objectid") for item in items]
    return geeklist
