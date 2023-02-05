from urllib.parse import quote


def get_tabletop_finder(bgg_name):
    bgg_name_enc = quote(bgg_name)
    tf_base_url = "https://www.tabletopfinder.eu/"
    tf_search_url = tf_base_url + f"en/boardgame/search?query={bgg_name_enc}"
    return tf_search_url
