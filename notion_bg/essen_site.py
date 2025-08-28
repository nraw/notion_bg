import json
from datetime import datetime
from pathlib import Path

import requests
from boardgamegeek import BGGClient
from bs4 import BeautifulSoup
from jinja2 import Template
from loguru import logger
from tqdm import tqdm

from notion_bg.get_essen import EssenGames, get_my_essen_games, get_thumbnails
from notion_bg.send_telegram import send_telegram


def create_my_essen_site(year=None, user_name="nraw"):
    # populate the jinja2 template in /notion_bg/essen.thml with my_essen_games
    # render the template and save it to /notion_bg/essen.html
    my_essen_games = get_my_essen_games(year, user_name=user_name)
    data_hash = hash(str(my_essen_games))
    #  prod_hash = get_prod_hash()
    get_all_thumbnails(my_essen_games)

    new_essen_games = EssenGames.model_validate(my_essen_games)
    old_essen_games = get_old_essen_games()
    message = new_essen_games.compare_with_old(old_essen_games)
    if message:
        message = f"My [Essen games](https://nraw.github.io/notion_bg/essen) update:\n{message}"
        try:
            send_telegram(message)
        except Exception as e:
            logger.error(f"Error sending telegram message: {e}")

    jinja_template = Path("notion_bg/essen.html").read_text()
    template = Template(jinja_template)
    # Determine current year from data or default to latest
    if year is None:
        year = max([2023, 2024, 2025])  # Default to latest supported year

    timestamp = datetime.now()
    data_json = new_essen_games.model_dump_json()

    # Available years for navigation
    available_years = [2023, 2024, 2025]

    output = template.render(
        my_essen_games=my_essen_games,
        timestamp=timestamp,
        data_hash=data_hash,
        data_json=data_json,
        current_year=year,
        available_years=available_years,
        current_user=user_name,
    )

    # Determine output file path based on user and year
    if user_name == "nraw":
        # Default user gets the main paths
        if year == max(available_years):
            output_path = "site/essen.html"
        else:
            output_path = f"site/{year}/essen.html"
    else:
        # Other users get user-specific paths
        if year == max(available_years):
            output_path = f"site/{user_name}_essen.html"
        else:
            output_path = f"site/{year}/{user_name}_essen.html"

    # Ensure directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(output)


def get_all_thumbnails(my_essen_games):
    logger.info("Getting thumbnails for Essen games")
    bgg = BGGClient()
    for games in tqdm(my_essen_games.values()):
        get_thumbnails(bgg, games)


def get_old_essen_games(data_hash=None):
    try:
        #  url = "http://localhost:8000/essen.html"
        url = "https://nraw.github.io/notion_bg/essen"
        res = requests.get(url)
        html_content = res.text
        soup = BeautifulSoup(html_content, "html.parser")
        old_hash_element = soup.find("meta", attrs={"name": "hash"})
        if old_hash_element:
            old_hash = int(old_hash_element.get("content"))
            if old_hash == data_hash:
                return None
        json_script = soup.find("script", type="application/json")
        json_data = json_script.string
        data = json.loads(json_data)
        old_essen_games = EssenGames.model_validate(data)
    except AttributeError:
        old_essen_games = None
    return old_essen_games
