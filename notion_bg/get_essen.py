from collections import Counter

import yaml
from loguru import logger

from notion_bg.get_geeklist import get_geeklist
from notion_bg.get_notion_games import get_notion_games


def compare_essen_sales():
    essen_url = "https://boardgamegeek.com/geeklist/319184/essen-2023-no-shipping-auction-list-post-your-own?itemid="
    notion_game_list = get_notion_game_list()
    essen_sales_games, essen_sales_ids = get_essen_sales()
    #  nset = set(expansions['id'].astype(int))
    #  nset = set(nraw_games_list)
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

    lesgo = [
        [g.get("objectname"), essen_url + g.get("id"), get_last_bid(g)]
        for g in available_games
    ]
    lesgo.sort()
    print(yaml.dump(lesgo))

    my_bids = [g for g in essen_sales_games if (get_last_bidder(g) == "nraw")]
    lesgo = [
        [g.get("objectname"), essen_url + g.get("id"), get_last_bid(g)] for g in my_bids
    ]
    lesgo.sort()
    print(yaml.dump(lesgo))

    my_bids = [get_last_bidder(g) for g in essen_sales_games]

    my_offers = [g for g in essen_sales_games if g.get("username") == "nraw"]
    lesgo = [
        [
            g.get("objectname"),
            essen_url + g.get("id"),
            get_last_bid(g),
            g.find("comment") is not None,
        ]
        for g in my_offers
    ]
    print(yaml.dump(lesgo))
    people_offering = [g.get("username") for g in essen_sales_games]


def get_essen_sales():
    logger.info("Obtaining Essen sale games")
    essen_geeklist_id = "319184"  # Essen
    essen_sales_games = get_geeklist(essen_geeklist_id, None, comments=True)
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


def get_last_bid(g):
    comments = g.find_all("comment")
    price = 0
    if comments:
        comment = comments[-1]
        comment_text = comment.text
        ugly_price = re.search(r"\d+", comment_text)
        if ugly_price:
            price = int(ugly_price.group(0))
    if not price:
        ugly_price = re.search(r"(\d+),-", g.text)
        if ugly_price:
            price = int(ugly_price.group(1))
    return price


def get_last_bidder(g):
    comments = g.find_all("comment")
    last_bidder = None
    if comments:
        comment = comments[-1]
        last_bidder = comment.get("username")
    return last_bidder
