import os

import requests

CHAT_ID = [135311138, 712291743, 514114264, 448383053]  # group
MESSAGE = "Welcome to Library API 🤓📚"


for user in CHAT_ID:
    url = f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage?chat_id={user}&text={MESSAGE}"

    requests.get(url)
