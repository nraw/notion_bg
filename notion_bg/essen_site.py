from datetime import datetime
from pathlib import Path

import requests
from boardgamegeek import BGGClient
from jinja2 import Template

from notion_bg.get_essen import get_my_essen_games, get_thumbnails


def create_my_essen_site():
    # populate the jinja2 template in /notion_bg/essen.thml with my_essen_games
    # render the template and save it to /notion_bg/essen.html
    my_essen_games = get_my_essen_games()
    data_hash = hash(str(my_essen_games))
    #  prod_hash = get_prod_hash()
    get_all_thumbnails(my_essen_games)

    jinja_template = Path("notion_bg/essen.html").read_text()
    template = Template(jinja_template)
    timestamp = datetime.now()
    output = template.render(
        my_essen_games=my_essen_games, timestamp=timestamp, data_hash=data_hash
    )
    Path("site/essen.html").write_text(output)


def get_all_thumbnails(my_essen_games):
    bgg = BGGClient()
    for games in my_essen_games.values():
        get_thumbnails(bgg, games)


def get_prod_hash():
    """<meta name="hash" content="your-hash-value-here">"""
    try:
        url = "https://my-essen.netlify.app/essen"
        res = requests.get(url)
        res_text = res.text
        str_hash = res_text.split('hash"')[1].split("/", 1)[0].split('"')[1]
        prod_hash = int(str_hash)
    except Exception:
        prod_hash = 0
    return prod_hash
