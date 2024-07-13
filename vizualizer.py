import json
import os
from time import sleep

import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from dotenv import load_dotenv


load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
API_URL = "https://games-test.datsteam.dev/"
url = "https://games-test.datsteam.dev/play/zombidef/units"


# Функция для получения данных с URL
def fetch_data():
    response = requests.get(url, headers={"X-Auth-Token": API_TOKEN})
    return response.json()


# Функция для обновления графика
def update():
    data = fetch_data()

    bases = data['base']
    zombies = data.get('zombies', [])
    enemy_blocks = data.get('enemyBlocks', [])

    x_coords_base = [base['x'] for base in bases]
    y_coords_base = [base['y'] for base in bases]
    health_base = [base['health'] for base in bases]

    x_coords_zombie = [zombie['x'] for zombie in zombies]
    y_coords_zombie = [zombie['y'] for zombie in zombies]
    health_zombie = [zombie['health'] for zombie in zombies]

    if enemy_blocks:
        x_coords_enemy = [block['x'] for block in enemy_blocks]
        y_coords_enemy = [block['y'] for block in enemy_blocks]
        health_enemy = [block['health'] for block in enemy_blocks]

    fig = plt.figure(figsize=(13, 13))
    plt.cla()

    plt.scatter(x_coords_base, y_coords_base, c=health_base, cmap='coolwarm', s=100, label='Базы')
    plt.scatter(x_coords_zombie, y_coords_zombie, c='green', s=50, label='Зомби')
    plt.scatter(x_coords_enemy, y_coords_enemy, c='red', s=75, label='Вражеские блоки')

    for i, base in enumerate(bases):
        plt.text(base['x'] + 0.3, base['y'] + 0.3, f"HP: {base['health']}", fontsize=9)

    for i, zombie in enumerate(zombies):
        plt.text(zombie['x'] + 0.3, zombie['y'] + 0.3, f"HP: {zombie['health']}", fontsize=9)

    if enemy_blocks:
        for i, block in enumerate(enemy_blocks):
            plt.text(block['x'] + 0.3, block['y'] + 0.3, f"HP: {block['health']}", fontsize=9)

    plt.title("Базы, Зомби и Вражеские блоки")
    plt.xlabel("Координата X")
    plt.ylabel("Координата Y")
    plt.colorbar(label="Здоровье базы")
    plt.legend()
    plt.grid(True)
    plt.show()


while True:
    # ani = FuncAnimation(fig, update, interval=2000)
    try:
        update()
    except Exception as error:
        print("An error occurred:", error)
    sleep(2)
