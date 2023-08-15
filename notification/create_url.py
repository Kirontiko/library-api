import os
from secrets import token_urlsafe

telegram_url = "https://t.me"
token = token_urlsafe(8)

url = f"{telegram_url}/{os.environ['BOT_NAME']}?start={token}"
print(url)
