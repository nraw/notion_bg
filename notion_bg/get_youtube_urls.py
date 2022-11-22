import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from notion_bg.config import conf

channels = {
    "Youtube Dice Tower": "UCiwBbXQlljGjKtKhcdMliRA",
    "Youtube SUSD": "UCyRhIGDUKdIOw07Pd8pHxCw",
}

query_additions = {"Youtube": " board game review", "Youtube HowTo": " how to play"}


def get_youtube_metas(bgg_name):
    yt_meta = dict()
    for data_update in conf["data_updates"]:
        if data_update.split()[0] == "Youtube":
            yt_meta[data_update] = get_youtube_meta(bgg_name, data_update)
    return yt_meta


def get_youtube_meta(bgg_name, data_update):
    youtube = get_youtube_engine()
    query_addition = query_additions.get(data_update, "")
    query = bgg_name + query_addition
    channel_id = channels.get(data_update, None)
    yt_meta = get_yt_meta(query, channel_id, youtube)
    return yt_meta


@lru_cache(1)
def get_youtube_engine():
    api_service_name = "youtube"
    api_version = "v3"
    google_api_key = os.environ["google_api_key"]

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=google_api_key
    )
    return youtube


def get_yt_meta(game, channel_id, youtube):
    first_vid = get_first_vid(game, channel_id, youtube)
    if first_vid:
        yt_id = first_vid["id"]["videoId"]
        url = "https://www.youtube.com/watch?v=" + yt_id
        title = first_vid["snippet"]["title"]
        yt_meta = dict(url=url, title=title, yt_id=yt_id)
    else:
        yt_meta = None
    return yt_meta


def get_first_vid(game, channel_id, youtube):
    request = youtube.search().list(
        part="snippet", channelId=channel_id, maxResults=1, q=game
    )
    response = request.execute()
    if response["items"]:
        first_vid = response["items"][0]
    else:
        first_vid = None
    return first_vid
