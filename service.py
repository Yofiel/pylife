import json
import random

from models import Player
from views import *

N = 50  # N = número de casas do tabuleiro
BR = 10  # B = S (sorte); R = revés
P = 10  # P = número de casas a serem avançadas


def create_players(players_name):
    players = []

    for name in players_name:
        new_player = Player(name)
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


def remove_players(players, removed_players):
    if not removed_players:
        return

    for player in removed_players:
        if player in players:
            players.remove(player)


def check_winner(players):
    winner = players[0]
    for player in players:
        if player.money > winner.money or (
            player.money >= winner.money and player.position > winner.position
        ):
            winner = player

    return winner


def start_round(game_path, player, removed_players, drawn_number):
    player.position += drawn_number

    if player.position >= len(game_path) - 1:
        player.position = len(game_path) - 1
        return player

    if game_path[player.position] != 0:
        print(game_path[player.position][1])
        player.money += int(game_path[player.position][0])

    if player.money < 0:
        removed_players.append(player)


def save_game_results(players, removed_players, winner):
    with open("results.txt", "a") as file:
        file.write(results_text(players, removed_players, winner))


# def main():
#     while True:
#         players = init_players()
#         removed_players = []
#         sort_players(players)
#         game_path = init_path()
#         start_round(game_path, players, removed_players)
#         winner = check_winner(players)
#         results_print(players, removed_players, winner)
#         save_game_results(players, removed_players, winner)
#
#         decision = input("Deseja jogar outra partida? [S/n]: ")
#
#         if decision.strip().lower() == "n":
#             print("Finalizando jogo...")
#             break
#
#
# if __name__ == "__main__":
#     main()
