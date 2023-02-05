from loguru import logger

from notion_bg.config import conf


def filter_games(data):
    check_games_filter()
    results = data["results"]
    selected_games = {}
    for result in results:
        status = result["properties"]["Status"]["select"]["name"]
        if conf["games_filter"] == "new":
            og_input = result["properties"]["OG name"]["rich_text"]
            newly_added = not og_input
            if newly_added:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
        elif conf["games_filter"] == "all":
            bought_or_pass = status in ["Bought", "Pass"]
            if not bought_or_pass:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
        elif conf["games_filter"] == "all_including_bought_passed":
            new_id = result["id"]
            #  new_game = get_notion_name(result)
            selected_games[new_id] = result

        elif conf["games_filter"] == "id":
            if result["id"] == conf["notion_id"]:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
        elif conf["games_filter"] == "bgg_id":
            if result["properties"]["bgg_id"]["number"] == conf["bgg_id"]:
                new_id = result["id"]
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
    logger.info(f"Filtered {len(selected_games)} games")
    return selected_games


def check_games_filter():
    assert (
        conf["games_filter"] in conf["games_filters"]
    ), f"Filter '{conf['games_filter']}' not in {conf['games_filters']}"
