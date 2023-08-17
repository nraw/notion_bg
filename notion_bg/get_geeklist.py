from time import sleep

import requests
from bs4 import BeautifulSoup
from loguru import logger


def get_geeklist(geeklist_id, key="objectid", comments=False):
    geeklist_url = f"https://www.boardgamegeek.com/xmlapi/geeklist/{geeklist_id}"
    if comments:
        geeklist_url += '?comments=1'

    res = get_response_with_retries(geeklist_url)
    xml_content = res.content
    bs = BeautifulSoup(xml_content, "lxml")
    items = bs.find_all("item")
    if key:
        geeklist = [item.get("objectid") for item in items]
    else:
        geeklist = items
    return geeklist


def get_response_with_retries(geeklist_url):
    status = 0
    max_retries = 10
    sleep_time = 5
    retry_count = 0
    res = None
    while status != 200 and retry_count <= max_retries:
        sleep(sleep_time * retry_count)
        res = requests.get(geeklist_url)
        status = res.status_code
        logger.info(f"{status=}")
        logger.info(f"{retry_count=}")
        retry_count += 1
    return res
