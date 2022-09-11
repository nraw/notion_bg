import requests

def get_notion_games():
    database_id = "14a0eda608be4da284229fe06491ecb7"
    headers = {
        "Authorization": "Bearer " + notion_token,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = get_notion_data(database_id, headers)
    return data

def get_notion_data(database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    res = requests.post(url, headers=headers)
    data = res.json()
    return data


