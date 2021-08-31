import json
import random

from views import *
from models import Player


N = 10
BR = 3
P = 4


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
    with open('specialfields.json', 'r') as file:
        data = json.load(file)

    count = 0
    while count < BR:
        bonus_position = random.randint(0, len(game_path) - 1)

        if game_path[bonus_position] != 0:
            continue

        loss_position = random.randint(0, len(game_path) - 1)

        if game_path[loss_position] != 0:
            continue

        bonus_choice = _, _ = random.choice(list(data['bonus'].items()))
        loss_choice = _, _ = random.choice(list(data['loss'].items()))

        game_path[bonus_position] = bonus_choice
        game_path[loss_position] = loss_choice

        count += 1


def spin_roulette():
    return random.randint(1, P)


def remove_player(players, player):
    players.remove(player)


def check_winner(players):
    winner = players[0]
    for player in players:
        if (player.money > winner.money or (player.money >= winner.money and player.position > winner.position)):
            winner = player

    return winner


def start_game(game_path, players):
    while True:
        for i in range(len(players)):
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
                remove_player(players, players[i])
                confirmation_print()

                if len(players) == 1:
                    end_match_print(players[0])
                    confirmation_print()
                    return players
                else:
                    break

            status_update_print(players[i])
            confirmation_print()


def main():
    while True:
        players = init_players()
        sort_players(players)
        game_path = init_path()
        start_game(game_path, players)
        winner = check_winner(players)
        results_print(players, winner)

        decision = input('Deseja jogar outra partida? [S/n]: ')

        if decision.strip().lower() == 'n':
            print('Finalizando jogo...')
            break


if __name__ == "__main__":
    main()
