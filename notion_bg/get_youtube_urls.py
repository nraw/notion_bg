import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from notion_bg.config import conf


def get_youtube_meta(bgg_name):
    api_service_name = "youtube"
    api_version = "v3"
    google_api_key = os.environ["google_api_key"]

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=google_api_key
    )

    if "Youtube" in conf["data_updates"]:
        query = bgg_name + " board game review"
        general_yt_meta = get_yt_meta(query, None, youtube)
    else:
        general_yt_meta = None

    if "Youtube SUSD" in conf["data_updates"]:
        dice_tower_id = "UCiwBbXQlljGjKtKhcdMliRA"
        dt_yt_meta = get_yt_meta(bgg_name, dice_tower_id, youtube)
    else:
        dt_yt_meta = None

    if "Youtube Dice Tower" in conf["data_updates"]:
        susd_id = "UCyRhIGDUKdIOw07Pd8pHxCw"
        susd_yt_meta = get_yt_meta(bgg_name, susd_id, youtube)
    else:
        susd_yt_meta = None
    yt_meta = dict(general=general_yt_meta, dt=dt_yt_meta, susd=susd_yt_meta)
    return yt_meta


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
