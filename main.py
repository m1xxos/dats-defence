import os
from time import sleep

import requests
import json
import logging
import time
from dotenv import load_dotenv

# Загрузка токена из .env файла
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://games-test.datsteam.dev/"

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_round_start():
    """Проверка на начало нового раунда."""
    logging.info("Checking if the round has started...")
    response = requests.get(f"{API_URL}/play/zombidef/units", headers={"X-Auth-Token": API_TOKEN})
    if response.status_code == 200:
        return True
    elif response.status_code == 400:
        data = response.json()
        if data.get("errCode") == 1002:
            logging.info("Lobby is ending soon. Time left: %s sec", data.get("error").split()[-2])
            return False
    logging.error("Error checking round start: %s", response.text)
    return False

def get_current_units():
    """Получение текущего состояния юнитов и карты."""
    response = requests.get(f"{API_URL}/play/zombidef/units", headers={"X-Auth-Token": API_TOKEN})
    if response.status_code == 200:
        logging.info("Current units: %s", response.json())
        return response.json()
    logging.error("Error getting current units: %s", response.text)
    return None

def send_commands(commands):
    """Отправка команд на сервер."""
    response = requests.post(f"{API_URL}/play/zombidef/command", headers={"X-Auth-Token": API_TOKEN}, json=commands)
    if response.status_code == 200:
        logging.info("Commands sent successfully.")
        logging.info(commands)
        return response.json()
    logging.error("Error sending commands: %s", response.text)
    return None

def build_new_cells(player_data):
    """Покупка новых клеток базы."""
    base = player_data['base']
    gold = player_data['player']['gold']

    if not base or gold <= 0:
        logging.warning("No base or insufficient gold.")
        return

    base_cells = [(cell['x'], cell['y']) for cell in base]
    new_cells = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for cell in base_cells:
        for direction in directions:
            new_cell = (cell[0] + direction[0], cell[1] + direction[1])
            if new_cell not in base_cells and new_cell not in new_cells and gold > 0:
                new_cells.append(new_cell)
                gold -= 1

    if new_cells:
        commands = {
            "build": [{"x": cell[0], "y": cell[1]} for cell in new_cells]
        }
        send_commands(commands)
    else:
        logging.info("No new cells to build.")

def main():
    logging.info("Starting game loop...")
    while True:
        if check_round_start():
            while True:
                player_data = get_current_units()
                if player_data:
                    build_new_cells(player_data)
                sleep(2)
            else:
                logging.info("No units information available.")
        else:
            logging.info("Waiting for the next round to start.")
            time.sleep(10)

if __name__ == "__main__":
    main()
