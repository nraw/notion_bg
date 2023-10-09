import re
from collections import Counter

import iterfzf
import yaml
from loguru import logger

from notion_bg.get_geeklist import get_geeklist
from notion_bg.get_my_expansions import get_my_expansions, get_my_games_list
from notion_bg.get_notion_games import get_notion_games


def compare_essen_sales():
    essen_url = "https://boardgamegeek.com/geeklist/319184/essen-2023-no-shipping-auction-list-post-your-own?itemid="
    notion_game_list = get_notion_game_list()
    essen_sales_games, essen_sales_ids = get_essen_sales()
    #  nset = set(nraw_games_list)
    nset = set(notion_game_list)
    eset = set(essen_sales_ids)

    whitelist = ["9963241", "10087556", "10008677", "10066644", "10020531"]  # kupljeno
    whitelist += ["9980317", "9976957"]  # prodano
    blacklist = ["10017821", "9963360"]

    # my bids stuff
    my_bids = [g for g in essen_sales_games if (get_last_bidder(g) == "nraw")]
    my_bids = [g for g in my_bids if g.get("id") not in whitelist]
    my_bids = [g for g in my_bids if g.get("id") not in blacklist]
    lesgo = [
        [
            g.get("objectname"),
            get_auction_end(g),
            essen_url + g.get("id"),
            get_last_bid(g),
        ]
        for g in my_bids
    ]
    lesgo.sort()
    lesgo.sort(key=lambda x: x[1])
    print(yaml.dump(lesgo))
    sum([i[3] for i in lesgo])

    # find game
    all_games = list({g.get("objectname") for g in essen_sales_games})
    all_games.sort()
    check_game(all_games, essen_sales_games)

    # my past bids stuff
    player = "nraw"
    my_past_bids = []
    for g in essen_sales_games:
        bidders = get_all_bidders(g)
        if bidders:
            if player in bidders[:-1]:
                my_past_bids += [g]
    lesgo = [
        [
            g.get("objectname"),
            get_auction_end(g),
            essen_url + g.get("id"),
            get_last_bid(g),
        ]
        for g in my_past_bids
    ]
    lesgo.sort(key=lambda x: x[1])
    print(yaml.dump(lesgo))

    bought_stuff = [g for g in essen_sales_games if g.get("id") in whitelist]
    lesgo = [
        [
            g.get("objectname"),
            get_auction_end(g),
            essen_url + g.get("id"),
            get_last_bid(g),
        ]
        for g in bought_stuff
    ]
    lesgo.sort()
    print(yaml.dump(lesgo))
    sum([i[3] for i in lesgo])

    # wishlist stuff
    available = nset.intersection(eset)
    available_games = [g for g in essen_sales_games if not check_is_sold(g, available)]
    my_bids_ids = [g.get("objectid") for g in my_bids]
    not_bidding_already = [
        g for g in available_games if g.get("objectid") not in my_bids_ids
    ]
    lesgo = [
        [
            g.get("objectname") + " (" + get_language(g) + ")",
            essen_url + g.get("id"),
            get_last_bid(g),
            get_auction_end(g),
        ]
        for g in not_bidding_already
    ]
    lesgo.sort()
    lesgo.sort(key=lambda x: x[0])
    lesgo.sort(key=lambda x: x[1])
    print(yaml.dump(lesgo))

    # expansions

    expansions = get_my_expansions(drop_promo=False, obtain_meta=False)
    nset = set(expansions["id"].astype(int))
    available = nset.intersection(eset)
    available_games = [g for g in essen_sales_games if not check_is_sold(g, available)]
    lesgo = [
        [
            g.get("objectname") + " (" + get_language(g) + ")",
            essen_url + g.get("id"),
            get_last_bid(g),
            get_auction_end(g),
        ]
        for g in available_games
    ]
    lesgo.sort()
    lesgo.sort(key=lambda x: x[1])
    print(yaml.dump(lesgo))

    # expansions outside the scope

    #  notion_game_names = get_notion_game_list(return_feature="bgg_name")

    nraw_games_list = get_my_games_list(bgg, return_feature="bgg_name")
    outside_name = "Outside the Scope of BGG"
    outside_games = [
        g for g in essen_sales_games if g.get("objectname") == outside_name
    ]
    expansion_mentions = [
        (g, check_expansion_mentions(g, nraw_games_list))
        for g in outside_games
        if check_expansion_mentions(g, nraw_games_list)
    ]
    lesgo = [
        [
            g.get("objectname") + " (" + get_language(g) + ")",
            essen_url + g.get("id"),
            get_last_bid(g),
            get_auction_end(g),
            mentions,
        ]
        for g, mentions in expansion_mentions
    ]
    lesgo.sort()
    lesgo.sort(key=lambda x: x[1])
    print(yaml.dump(lesgo))

    # my offers
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

    bidders = [get_last_bidder(g) for g in essen_sales_games]
    bidders = [g for g in bidders if g is not None]
    Counter(bidders).most_common(10)
    best_bidder = Counter(bidders).most_common(10)[1][0]
    best_bidder_bids = [
        g for g in essen_sales_games if (get_last_bidder(g) == best_bidder)
    ]
    lesgo = [
        [g.get("objectname"), essen_url + g.get("id"), get_last_bid(g)]
        for g in best_bidder_bids
    ]
    sum([l[2] for l in lesgo])
    lesgo.sort(key=lambda x: x[2])
    print(yaml.dump(lesgo))

    most_sold = Counter(
        [g.get("objectname") for g in essen_sales_games if "[-]" in str(g)]
    )
    most_sold.most_common(20)

    most_offered = Counter([g.get("objectname") for g in essen_sales_games])
    most_offered.most_common(20)

    people_offering = [g.get("username") for g in essen_sales_games]
    Counter(people_offering).most_common(10)

    most_expensive = [
        (get_last_bid(g), essen_url + g.get("id"), g.get("objectname"))
        for g in essen_sales_games
        if g.find("comment") is not None
    ]
    most_expensive.sort(key=lambda x: x[0], reverse=True)
    most_expensive[:10]

    most_bid = [
        (len(g.find_all("comment")), essen_url + g.get("id"), g.get("objectname"))
        for g in essen_sales_games
        if g.find("comment") is not None
    ]
    most_bid.sort(key=lambda x: x[0], reverse=True)
    most_bid[:10]

    # cheap games

    available_games = [g for g in essen_sales_games if not check_is_sold(g, eset)]
    cheap_games = [g for g in available_games if get_last_bid(g) == 1]
    lesgo = [
        [g.get("objectname") + " (" + get_language(g) + ")", essen_url + g.get("id")]
        for g in cheap_games
    ]
    lesgo.sort()
    lesgo.sort(key=lambda x: x[1])
    print(yaml.dump(lesgo))
    cheap_ids = {int(game.get("objectid")) for game in cheap_games}
    games_info = get_games_info(cheap_ids)

    cheapos = pd.DataFrame([g.data() for g in games_info])
    bayes_averages = cheapos["stats"].apply(lambda x: x["bayesaverage"])
    cheapos["bayesaverage"] = bayes_averages
    bayes_averages = cheapos["stats"].apply(lambda x: x["average"])
    cheapos["average"] = bayes_averages
    cheapos = cheapos[(~cheapos.expansion) & (~cheapos.accessory)]
    rankings = pd.DataFrame(
        cheapos.apply(lambda x: get_best_rank(x), axis=1).to_list(),
        index=cheapos.index,
        columns=["rank", "rank_category"],
    )
    cheapos = pd.concat([cheapos, rankings], axis=1)
    sort_value = "rank"
    i = 0
    # i = 46
    view_cheapos(i, cheapos, cheap_games, sort_value)


def view_cheapos(i, cheapos, cheap_games, sort_value):
    # i = 76
    cheapos = cheapos.sort_values(sort_value)
    essen_url = "https://boardgamegeek.com/geeklist/319184/essen-2023-no-shipping-auction-list-post-your-own?itemid="
    while True:
        game = cheapos.iloc[i]
        game_id = str(game["id"])

        offers = [
            essen_url + g.get("id") for g in cheap_games if g.get("objectid") == game_id
        ]
        print(i)
        print(game["name"])
        print(game["rank_category"])
        print(game["rank"])
        print(yaml.dump(offers))
        i += 1
        input()


def get_best_rank(game):
    ranks = game["stats"]["ranks"]
    actual_ranks = [r for r in ranks if r["value"]]
    if not actual_ranks:
        return None, None
    best_rank = sorted(ranks, key=lambda x: x["value"])[0]
    rank = best_rank["value"]
    rank_category = best_rank["friendlyname"]
    return rank, rank_category


def get_games_info(game_ids):
    all_games = list(game_ids)
    batch_size = 100
    i = 0
    games_info = []
    print(len(all_games))
    while i < len(all_games):
        batch_range = [i * batch_size, (i + 1) * batch_size]
        batch_games = all_games[(batch_range[0]) : (batch_range[1])]
        batch_meta = bgg.game_list(batch_games)
        games_info += batch_meta
        i += 1
        print(i)
    return games_info


def get_essen_sales():
    logger.info("Obtaining Essen sale games")
    essen_geeklist_id = "319184"  # Essen
    essen_sales_games = get_geeklist(essen_geeklist_id, None, comments=True)
    essen_sales_ids = [int(game.get("objectid")) for game in essen_sales_games]
    return essen_sales_games, essen_sales_ids


def get_notion_game_list(return_feature="bgg_id"):
    cool_states = ["Want to buy", "Want to try", "Need more info", "Not on Tlama"]
    data = get_notion_games()
    results = data["results"]
    if return_feature == "bgg_id":
        notion_game_list = [
            g["properties"]["bgg_id"]["number"]
            for g in results
            if g["properties"]["Status"]["select"]["name"] in cool_states
        ]
    elif return_feature == "bgg_name":
        notion_game_list = [
            g["properties"]["Name"]["title"][0]["plain_text"]
            for g in results
            if g["properties"]["Status"]["select"]["name"] in cool_states
        ]
    else:
        notion_game_list = [
            g
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
        really_comment_text = re.sub("\[.*?\]", "", comment_text)
        ugly_price = re.search(r"\d+", really_comment_text)
        if ugly_price:
            price = int(ugly_price.group(0))
    if price > 1900:
        price = 0
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


def get_all_bidders(g):
    comments = g.find_all("comment")
    bidders = []
    for comment in comments:
        bidder = comment.get("username")
        bidders += [bidder]
    return bidders


def check_is_sold(g, available):
    is_available = int(g.get("objectid")) in available
    if not is_available:
        return True
    is_crossed = "[-]" in str(g)
    if is_crossed:
        return True
    comments = g.find_all("comment")
    message_bin = False
    for comment in comments:
        message_bin = "BIN" in comment.text
        if message_bin:
            return True
    return False


def get_auction_end(g):
    auction_end = re.search(r"Auction ends.*? (?:\d{1,2} \S*)", g.text)
    if auction_end:
        auction_end = auction_end[0].strip(",")[-6:].strip()
    else:
        auction_end = ""
    return auction_end


def get_language(g):
    language = re.search(r"Language.*? (.*)", g.text)
    if language:
        language = language[1]
    else:
        language = "No idea"
    return language


def check_game(all_games, essen_sales_games):
    game = iterfzf.iterfzf(all_games)
    selected_games = [g for g in essen_sales_games if g.get("objectname") == game]
    lesgo = [
        [
            g.get("objectname"),
            essen_url + g.get("id"),
            get_last_bid(g),
            g.find("comment") is not None,
        ]
        for g in selected_games
    ]
    print(yaml.dump(lesgo))


def check_expansion_mentions(g, expansion_names):
    is_there_any = [n for n in expansion_names if n in g.text]
    return is_there_any
