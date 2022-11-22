from loguru import logger


@lru_cache(100)
def get_bgg_game(new_game, bgg_id):
    bgg = BGGClient()
    if bgg_id:
        logger.info(f"Getting bgg info via id - {new_game}")
        game = bgg.game(game_id=bgg_id)
    else:
        try:
            logger.info(f"Getting bgg info via name - {new_game}")
            game = bgg.game(new_game)
        except Exception:
            logger.info(f"Getting bgg info via google - {new_game}")
            bgg_id, bgg_url = get_bgg_id_wishlist_scanner(new_game)
            game = bgg.game(game_id=bgg_id)
    return game


def get_bgg_id_wishlist_scanner(new_game):
    wishlist_scanner_url = os.environ["wishlist_scanner_url"]
    url = wishlist_scanner_url + "?barcode=" + quote(new_game)
    res = requests.get(url)
    bgg_url = res.text
    bgg_id = bgg_url.split("/")[-2]
    return bgg_id, bgg_url
