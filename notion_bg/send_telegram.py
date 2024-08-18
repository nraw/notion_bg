import os

from telegram import Bot


def send_telegram(message):
    try:
        bot_token = os.getenv("TELEGRAM_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        bot = Bot(token=bot_token)
        bot.send_message(chat_id=chat_id, text=message)
    except Exception:
        print("Error sending telegram message")
