import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm


def get_bbb_games():
    logger.info("Obtaining bbb games")
    #  url = "http://bohemiaboardsandbrews.com/games"
    games_list = []
    for page in tqdm(range(1, 100)):
        url = f"https://www.bohemiaboardsandbrews.com/knihovna-her?e85fe75c_page={page}"
        res = requests.get(url)
        res_html = res.text

        bs = BeautifulSoup(res_html, "lxml")
        games_raw = bs.find_all("a", href=True)
        games = clean_games(games_raw)
        if games:
            games_list += games
        else:
            break
    return games_list


def clean_games(games_raw):
    games = [
        g["href"].split("/")[-2] for g in games_raw if "boardgamegeek" in g["href"]
    ]
    games = [int(g) for g in games if g.isdigit()]
    return games
