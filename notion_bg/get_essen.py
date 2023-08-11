from collections import Counter

import yaml
from loguru import logger

from notion_bg.get_geeklist import get_geeklist
from notion_bg.get_notion_games import get_notion_games


def compare_essen_sales():
    essen_url = "https://boardgamegeek.com/geeklist/319184/essen-2023-no-shipping-auction-list-post-your-own?itemid="
    notion_game_list = get_notion_game_list()
    essen_sales_games, essen_sales_ids = get_essen_sales()
    nset = set(notion_game_list)
    eset = set(essen_sales_ids)
    available = nset.intersection(eset)
    available_games = [
        g
        for g in essen_sales_games
        if int(g.get("objectid")) in available and "[-]" not in str(g)
    ]
    #  most_sold = Counter([g.get("objectname") for g in essen_sales_games if "[-]" in str(g)])
    #  len([g for g in essen_sales_games if "[-]" in str(g)])

    lesgo = [[g.get("objectname"), essen_url + g.get("id")] for g in available_games]
    print(yaml.dump(lesgo))

    #  nset = set(expansions['id'].astype(int))
    #  nset = set(nraw_games_list)


def get_essen_sales():
    logger.info("Obtaining Essen sale games")
    essen_geeklist_id = "319184"  # Essen
    essen_sales_games = get_geeklist(essen_geeklist_id, None)
    essen_sales_ids = [int(game.get("objectid")) for game in essen_sales_games]
    return essen_sales_games, essen_sales_ids


def get_notion_game_list():
    cool_states = ["Want to buy", "Want to try", "Need more info", "Not on Tlama"]
    data = get_notion_games()
    results = data["results"]
    notion_game_list = [
        g["properties"]["bgg_id"]["number"]
        for g in results
        if g["properties"]["Status"]["select"]["name"] in cool_states
    ]
    return notion_game_list


#  def get_essen_previews():
#      logger.info("Obtaining Essen preview games")
#      essen_previews_id = "63"
#      essen_preview_games = get_geeklist(essen_previews_id)
#      essen_preview_games = [int(game) for game in bga_games]
