import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger
from tqdm import tqdm


def get_svet_her():
    logger.info("Obtaining Svet Her games")
    games_raw = []
    for page in tqdm(range(198, 200)):
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


def clean_games(games_raw):
    games = pd.DataFrame([game.text for game in games_raw], columns=["raw_game"])
    games["czech"] = games.raw_game.str.contains("\(CZ\)")
    games = games[~games.czech].copy()
    games["brackets"] = games.raw_game.str.extract("(\(.*\))")
    games["game"] = games.raw_game.str.extract("(.*)\(")
    games["game"] = games.apply(
        lambda x: x["raw_game"] if x["game"] is np.NaN else x["game"], axis=1
    )
    games["game"] = games.game.str.strip()
    #  whatever = games.iloc[:89].game.progress_apply(get_bgg_id)
    return games
