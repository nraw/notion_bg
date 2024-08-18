import os

import requests


def send_telegram(message):
    try:
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message}

        response = requests.post(url, data=payload)
    except Exception:
        print("Error sending telegram message")
