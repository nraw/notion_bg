import requests, json
from bs4 import BeautifulSoup

from notion_bg.get_notion_games import get_notion_games
from notion_bg.get_bgg_data import get_bgg_data, check_bgg_id
from notion_bg.get_bga_games import get_bga_games
from notion_bg.get_bbb_games import get_bbb_games
from notion_bg.get_svet_her import get_svet_her
from notion_bg.get_tlama import get_tlama_showroom, get_tlama
from notion_bg.get_youtube_urls import get_youtube_meta
from notion_bg.update_notion_game import update_notion_game
from notion_bg.config import conf
from loguru import logger

def main():
    logger.info(f"game_filter: {conf['games_filter']}")
    logger.info(f"data_updates: {conf['data_updates']}")

    data = get_notion_games()
    selected_games = filter_games(data)
    process_selected_games(selected_games, data)
    
def filter_games(data):
    results = data['results'] 
    selected_games = {}
    for result in results:
        if conf['games_filter'] == 'new':
            og_input = result['properties']['OG name']['rich_text']
            if not og_input:
                new_id = result['id']
                #  new_game = get_notion_name(result)
                selected_games[new_id] = result
        elif conf['games_filter'] == 'all':
            new_id = result['id']
            #  new_game = get_notion_name(result)
            selected_games[new_id] = result
    logger.info(f"Filtered {len(selected_games)} games")
    return selected_games

def get_notion_name(game):
    game_name = game['properties']["Name"]['title'][0]['plain_text']
    return game_name


def process_selected_games(selected_games, data):
    if 'In BGA' in conf['data_updates']:
        bga_games = get_bga_games()
    if 'In BBB' in conf['data_updates']:
        bbb_games = get_bbb_games()
    if 'In Tlama Showroom' in conf['data_updates']:
        tlama_showroom = get_tlama_showroom()
    if 'In Svet Her' in conf['data_updates']:
        svet_her_games = get_svet_her()
    for new_id, new_game_data in selected_games.items():
        new_game = get_notion_name(new_game_data)
        logger.info(f"Processing {new_game}")
        bgg_id = check_bgg_id(new_id, new_game_data)
        bgg_meta = get_bgg_data(new_game, bgg_id)
        bgg_name = bgg_meta['bgg_name']
        bgg_id = bgg_meta['bgg_id']
        if 'In BGA' in conf['data_updates']:
            in_bga = str(bgg_id) in bga_games
        else:
            in_bga = None
        if 'In BBB' in conf['data_updates']:
            in_bbb = bgg_name in list(bbb_games['game'])
        else:
            in_bbb = None
        if 'In Tlama Showroom' in conf['data_updates']:
            in_tlama_showroom = bgg_id in list(tlama_showroom.keys())
        else:
            in_tlama_showroom = None
        if 'In Svet Her' in conf['data_updates']:
            in_svet_her = bgg_name in list(svet_her_games['game'])
        else:
            in_svet_her = None
        yt_meta = get_youtube_meta(bgg_name)
        tlama_meta = get_tlama(bgg_name)
        game_meta = dict(
                bgg_meta = bgg_meta,
                in_bga = in_bga,
                in_tlama_showroom = in_tlama_showroom,
                in_bbb = in_bbb,
                in_svet_her = in_svet_her,
                yt_meta = yt_meta,
                tlama_meta = tlama_meta)
        update_notion_game(new_id, new_game, game_meta)

if __name__ == '__main__':
    main()
