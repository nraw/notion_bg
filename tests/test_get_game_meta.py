from notion_bg.get_game_meta import *


def test_get_game_meta():
    new_id = "369d1e1a-d39a-4fe6-8538-2cdc2a200631"
    new_game_data = {
        "id": "369d1e1a-d39a-4fe6-8538-2cdc2a200631",
        "properties": {
            "Status": {
                "id": "%5EOE%40",
                "type": "select",
                "select": {
                    "id": "c84ecbda-1729-4aea-9049-f9dff925b8ca",
                    "name": "Not on Tlama",
                    "color": "red",
                },
            },
            "desc": {
                "id": "_UQF",
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": "susd quantum trick taking game",
                            "link": None,
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "susd quantum trick taking game",
                        "href": None,
                    }
                ],
            },
            "bgg_id": {"id": "n%3By%60", "type": "number", "number": 324345},
            "Name": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "Cat in the box", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Cat in the box",
                        "href": None,
                    }
                ],
            },
        },
        "url": "https://www.notion.so/Cat-in-the-box-369d1e1ad39a4fe685382cdc2a200631",
    }
