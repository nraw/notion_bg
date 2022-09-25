import requests
from loguru import logger
from bs4 import BeautifulSoup
from boardgamegeek import BGGClient
from notion_bg.config import conf
import re

def get_tlama(bgg_name, new_game_data):

    if 'Tlama' in conf['data_updates']:
        tlama_backup = new_game_data['properties']['Tlama Backup']['url']
        tlama_current = new_game_data['properties']['Tlama']['url']
        if tlama_current is not None and tlama_backup != tlama_current:
            logger.info("Tlama url was manually meddled with")
            tlama_meta = None
        else:
            #  url = f"https://www.tlamagames.com/vyhledavani/?string={bgg_name}"
            url = f"https://www.tlamagames.com/en/search/?string={bgg_name}"
            res = requests.get(url)
            res_html = res.text
            bs = BeautifulSoup(res_html, "lxml")
            games_raw = bs.find_all("div", class_="p")
            if games_raw:
                first_game = games_raw[0]
                tlama_name = first_game.find(attrs={"data-micro":"name"}).text.strip()
                tlama_url_rel = first_game.find('a', attrs={"data-micro":"url"})['href']
                tlama_url = 'https://www.tlamagames.com' + tlama_url_rel
                tlama_meta = dict(title=tlama_name, url=tlama_url)
                if tlama_backup is not None:
                    tlama_backup_url = re.sub('.*\(', '', tlama_backup).replace(')','')
                    if tlama_backup_url == tlama_url:
                        logger.info("Tlama url same as before")
                        tlama_meta = None
            else:
                tlama_meta = None
    else:
        tlama_meta = None
    return tlama_meta


def get_tlama_showroom():
    logger.info("Obtaining Tlama Showroom games")
    bgg = BGGClient()
    games_batch = bgg.collection("mirdata", own=True, exclude_subtype="boardgameexpansion")
    tlama_showroom = {game.id: game._data for game in games_batch if "id" in dir(game)}
    return tlama_showroom

