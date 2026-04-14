import os
import requests

TOKEN = os.getenv("BOT_MAFIA")

url = f"https://api.telegram.org/bot{TOKEN}/getMe"

print(requests.get(url).text)
