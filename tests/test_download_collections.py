from notion_bg.download_collections import *


def test_download_collections():
    collections = download_collections()
    assert type(collections) is dict
