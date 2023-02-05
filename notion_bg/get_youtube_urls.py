import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from loguru import logger

from notion_bg.config import conf

youtube_channel_maps = {
    "Youtube": None,
    "Youtube SUSD": "UCyRhIGDUKdIOw07Pd8pHxCw",
    "Youtube Dice Tower": "UCiwBbXQlljGjKtKhcdMliRA",
}


def get_youtube_meta(bgg_name):
    api_service_name = "youtube"
    api_version = "v3"
    google_api_key = os.environ["google_api_key"]

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=google_api_key
    )
    yt_meta = {}
    for channel_name in youtube_channel_maps:
        if channel_name in conf["data_updates"]:
            channel_id = youtube_channel_maps[channel_name]
            if channel_id:
                query = bgg_name
            else:
                query = bgg_name + " board game review"
            yt_meta[channel_name] = get_yt_meta(query, None, youtube)
        else:
            yt_meta[channel_name] = None
    return yt_meta


def get_yt_meta(game, channel_id, youtube):
    try:
        first_vid = get_first_vid(game, channel_id, youtube)
        if first_vid:
            yt_id = first_vid["id"]["videoId"]
            url = "https://www.youtube.com/watch?v=" + yt_id
            title = first_vid["snippet"]["title"]
            yt_meta = dict(url=url, title=title, yt_id=yt_id)
        else:
            yt_meta = None
    except Exception as e:
        logger.error(f"Youtube problem: {e}")
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
