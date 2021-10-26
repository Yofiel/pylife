import json
import random
from os.path import join

from src.dao import save_winner

from .models import Player

N = 50  # N = número de casas do tabuleiro
BR = 10  # B = S (sorte); R = revés
P = 6  # P = número de casas a serem avançadas


def create_players(players_name, colors):
    players = []

    for index, name in enumerate(players_name):
        new_player = Player(name, colors[index])
        players.append(new_player)

    return players


def sort_players(players):
    random.shuffle(players)


def init_path():
    game_path = [0] * N

    with open(join("assets", "specialfields.json"), "r") as file:
        data = json.load(file)

    count = 0
    while count < BR:
        bonus_position = random.randint(1, len(game_path) - 2)

        if game_path[bonus_position] != 0:
            continue

        loss_position = random.randint(1, len(game_path) - 2)

        if game_path[loss_position] != 0:
            continue

        bonus_choice = _, _ = random.choice(list(data["bonus"].items()))
        loss_choice = _, _ = random.choice(list(data["loss"].items()))

        game_path[bonus_position] = bonus_choice
        game_path[loss_position] = loss_choice

        count += 1

    return game_path


def spin_roulette():
    return random.randint(1, P)


def is_over(player, removed_players):
    if player.position == N - 1:
        return True
    if len(removed_players) == 3:
        return True

    return False


def check_winner(players):
    winner = players[0]
    for player in players:
        if player.money > winner.money or (
            player.money >= winner.money and player.position > winner.position
        ):
            winner = player

    return winner


def move_player(game_path, player, removed_players, drawn_number):
    player.position += drawn_number

    if player.position >= len(game_path) - 1:
        player.position = len(game_path) - 1

    if game_path[player.position] != 0:
        player.money += int(game_path[player.position][0])

    if player.money < 0:
        removed_players.append(player)

    return game_path[player.position]


def save_game_result(winner):
    save_winner(winner)
