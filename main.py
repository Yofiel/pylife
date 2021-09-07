import json
import random

from views import *
from models import Player


N = 50  # N = número de casas do tabuleiro
BR = 10  # B = S (sorte); R = revés
P = 10  # P = número de casas a serem avançadas


def init_players():
    num = insert_players_number()

    try:
        if not 2 <= int(num) <= 4:
            raise ValueError
        else:
            num = int(num)
    except ValueError:
        invalid_players_quantity_print()
        return init_players()

    players = []
    while True:
        name = insert_player_name()

        if not name or name.isspace():
            invalid_player_name_print()
            continue

        new_player = Player(name)
        players.append(new_player)

        if len(players) == num:
            break

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


def start_game(game_path, players, removed_players):
    while True:
        # Os jogadores falidos serão removidos de fato após o fim da rodada vigente
        remove_players(players, removed_players)
        for i in range(len(players)):
            if len(players) == 1:
                end_match_print(players[0])
                confirmation_print()
                return players

            your_turn_print(players[i])
            confirmation_print()

            drawn_number = spin_roulette()

            movement_print(drawn_number)
            confirmation_print()

            players[i].position += drawn_number

            if players[i].position >= len(game_path) - 1:
                players[i].position = len(game_path) - 1
                end_match_print(players[i])
                return players

            if game_path[players[i].position] != 0:
                print(game_path[players[i].position][1])
                players[i].money += int(game_path[players[i].position][0])

            if players[i].money < 0:
                bankruptcy_print(players[i])
                removed_players.append(players[i])
                confirmation_print()

                # Se todos os jogadores falirem com exceção de um, a rodada será encerrada
                if len(removed_players) == len(players) - 1:
                    break
                else:
                    continue

            status_update_print(players[i])
            confirmation_print()


def save_game_results(players, removed_players, winner):
    with open("results.txt", "a") as file:
        file.write(results_text(players, removed_players, winner))


def main():
    while True:
        players = init_players()
        removed_players = []
        sort_players(players)
        game_path = init_path()
        start_game(game_path, players, removed_players)
        winner = check_winner(players)
        results_print(players, removed_players, winner)
        save_game_results(players, removed_players, winner)

        decision = input("Deseja jogar outra partida? [S/n]: ")

        if decision.strip().lower() == "n":
            print("Finalizando jogo...")
            break


if __name__ == "__main__":
    main()
