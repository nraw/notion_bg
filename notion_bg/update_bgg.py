import json
import os
from datetime import date, datetime

import requests


def update_bgg(game_id, status):
    #  game_id = 161417
    username = os.environ["BGG_USERNAME"]
    password = os.environ["BGG_PASS"]

    login_payload = {"credentials": {"username": username, "password": password}}
    headers = {"content-type": "application/json"}

    with requests.Session() as s:
        p = s.post(
            "https://boardgamegeek.com/login/api/v1",
            data=json.dumps(login_payload),
            headers=headers,
        )

        #  url = "https://boardgamegeek.com/api/collectionitems/93717675"
        #  json_data = {
        #      "item": {
        #          "collid": "93717675",
        #          "versionid": None,
        #          "objecttype": "thing",
        #          "objectid": str(game_id),
        #          #  "user": {
        #          #      "username": "nraw",
        #          #      "avatar": "0",
        #          #      "avatarfile": "",
        #          #      "country": "Luxembourg",
        #          #      "city": "",
        #          #      "state": "",
        #          #      "microbadges": [],
        #          #      "flagimgurl": "https://cf.geekdo-static.com/images/flags/16x16/shadow/flag_luxembourg.png",
        #          #  },
        #          #  "objectname": "Hive Pocket",
        #          "status": {
        #              "own": True,
        #          },
        #          "status_tstamp": "2023-06-05 17:05:20",
        #      },
        #  }
        #  response = s.put(
        #      url,
        #      headers=headers,
        #      json=json_data,
        #  )

        #  json_data = {
        #      "item": {
        #          "collid": 107138178,
        #          #  "pp_currency": "USD",
        #          #  "cv_currency": "USD",
        #          "objecttype": "thing",
        #          "objectid": "295293",
        #          "status": {
        #              "own": True,
        #          },
        #      },
        #  }

        #  response = s.post(
        #      "https://boardgamegeek.com/api/collectionitems",
        #      headers=headers,
        #      json=json_data,
        #  )
        url = "https://boardgamegeek.com/geekcollection.php"

        data = {
            "fieldname": "status",
            "collid": "93717776",
            "objecttype": "thing",
            "objectid": "171131",
            "own": "1",
            "B1": "Cancel",
            "wishlistpriority": "3",
            "ajax": "1",
            "action": "savedata",
        }
        response = s.post(
            url,
            headers=headers,
            json=data,
        )
    return r
