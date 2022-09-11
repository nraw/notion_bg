import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.utils import quote
from loguru import logger

def get_bbb_games():
    logger.info("Obtaining bbb games")
    url = "http://bohemiaboardsandbrews.com/games"
    res = requests.get(url)
    res_html = res.text

    bs = BeautifulSoup(res_html, "lxml")
    games_raw = bs.find_all("div", class_="game_rollover")
    games = clean_games(games_raw)
    return games

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
