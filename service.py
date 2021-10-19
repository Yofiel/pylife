import json
import random

from models import Player

N = 50  # N = número de casas do tabuleiro
BR = 10  # B = S (sorte); R = revés
P = 10  # P = número de casas a serem avançadas


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
    init_special_fields(game_path)
    return game_path


def init_special_fields(game_path):
    with open("specialfields.json", "r") as file:
        data = json.load(file)

    count = 0
    while count < BR:
        bonus_position = random.randint(0, len(game_path) - 1)

        if game_path[bonus_position] != 0:
            continue

        loss_position = random.randint(0, len(game_path) - 1)

        if game_path[loss_position] != 0:
            continue

        bonus_choice = _, _ = random.choice(list(data["bonus"].items()))
        loss_choice = _, _ = random.choice(list(data["loss"].items()))

        game_path[bonus_position] = bonus_choice
        game_path[loss_position] = loss_choice

        count += 1


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


# def save_game_results(players, removed_players, winner):
#    with open("results.txt", "a") as file:
#        file.write(results_text(players, removed_players, winner))
