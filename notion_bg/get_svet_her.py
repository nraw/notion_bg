import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from loguru import logger

from notion_bg.get_bbb_games import clean_games


def get_svet_her():
    logger.info("Obtaining Svet Her games")
    games_raw = []
    for page in tqdm(range(1, 100)):
        json_data = {
            "sort": "products_last_modified-DESC",
            "hDemo": "1",
            "page": str(page),
            "url": "/herna/hry",
        }

        response = requests.post(
            "https://www.svet-deskovych-her.cz/produkty/html_load/products_list/",
            data=json_data,
        )
        res_html = response.text

        bs = BeautifulSoup(res_html, "lxml")
        games_raw_batch = bs.find_all("h3", class_="item-name")
        if games_raw_batch:
            games_raw += games_raw_batch
        else:
            break
    games = clean_games(games_raw)
    games_list = list(games["game"])
    return games_list
