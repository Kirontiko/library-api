import os

import requests

from dotenv import load_dotenv

load_dotenv()


def create_start_url(user):
    telegram_url = "https://t.me"
    token = user.token

    url = f"{telegram_url}/{os.environ['BOT_NAME']}?start={token}"
    return url


def send_start_notification(user):
    MESSAGE = "Welcome to Library API 🤓📚"

    chat_id = user.chat_id
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage?chat_id={chat_id}&text={MESSAGE}"

    requests.get(url)


def send_notification(user, message):

    chat_id = user.chat_id
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage?chat_id={chat_id}&text={message}"

    requests.get(url)
