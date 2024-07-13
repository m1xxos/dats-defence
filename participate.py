import os
from time import sleep

import requests


from dotenv import load_dotenv
from urllib3 import request

# Загрузка токена из .env файла
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://games.datsteam.dev/"


while True:
    r = requests.put(f"{API_URL}play/zombidef/participate", headers={"X-Auth-Token": API_TOKEN})
    print(r.text)
    sleep(10)
