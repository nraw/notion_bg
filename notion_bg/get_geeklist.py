from time import sleep
import os

import requests
from bs4 import BeautifulSoup
from loguru import logger


def get_geeklist(geeklist_id, key="objectid", comments=False):
    geeklist_url = f"https://boardgamegeek.com/xmlapi/geeklist/{geeklist_id}"
    if comments:
        geeklist_url += "?comments=1"

    res = get_response_with_retries(geeklist_url)
    xml_content = res.content
    bs = BeautifulSoup(xml_content, "xml")
    items = bs.find_all("item")
    if key:
        geeklist = [item.get("objectid") for item in items]
    else:
        geeklist = items
    return geeklist


def get_response_with_retries(geeklist_url):
    status = 0
    max_retries = 25
    base_sleep_time = 10  # Start with 10 seconds
    retry_count = 0
    res = None

    bgg_api_key = os.environ.get("BGG_API_KEY", "")
    headers = {"Authorization": f"Bearer {bgg_api_key}"}
    while status != 200 and retry_count <= max_retries:
        # Exponential backoff: 10s, 20s, 40s, 80s, 160s, etc.
        wait_time = base_sleep_time * (2 ** retry_count)
        if retry_count > 0:
            logger.info(f"Retry attempt {retry_count}/{max_retries}, waiting {wait_time}s before retry")
            sleep(wait_time)
        res = requests.get(geeklist_url, headers=headers)
        status = res.status_code
        logger.info(f"status={status}, retry_count={retry_count}")
        if status == 429:
            # Rate limited, respect the Retry-After header if present
            retry_after = res.headers.get("Retry-After")
            if retry_after:
                logger.info(f"Rate limited. Retry-After header: {retry_after}s")
        retry_count += 1
    if status != 200:
        raise Exception(f"Failed to get response from {geeklist_url} after {max_retries} retries. Final status: {status}")
    return res
