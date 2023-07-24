from collections import defaultdict

from boardgamegeek import BGGClient

from notion_bg.get_notion_games import get_notion_games


def sync_bgg():
    data = get_notion_games()
    notion_games = [get_id_and_status(g) for g in data["results"]]
    notion_states = defaultdict(list)
    for game, status in notion_games:
        notion_states[status] += [game]
    sync_bought(notion_states)


def get_id_and_status(g):
    bgg_id = g["properties"]["bgg_id"]["number"]
    status = g["properties"]["Status"]["select"]["name"]
    return bgg_id, status


def sync_bought(notion_states):
    notion_bought = set(notion_states["Bought"])
    bgg_owned = get_bgg_owned()
    new_bought = notion_bought - bgg_owned
    mark_as_owned(new_bought)


def get_bgg_owned():
    bgg = BGGClient()
    games_batch = bgg.collection("nraw", own=True)
    owned = {game.id: game._data for game in games_batch if "id" in dir(game)}
    bgg_owned = set(owned.keys())
    return bgg_owned


def mark_as_owned(new_bought):
    pass


#  def sync_ordered(data):
#      notion_ordered = get_notion_ordered(data)
#      bgg_ordered = get_bgg_ordered()
#      new_ordered = notion_ordered - bgg_ordered
#      mark_as_ordered(new_ordered)


#  def get_bgg_ordered():
#      bgg = BGGClient()
#      games_batch = bgg.collection("nraw", preordered=True)
#      preordered = {game.id: game._data for game in games_batch if "id" in dir(game)}
#      bgg_ordered = set(preordered.keys())
#      return bgg_ordered
