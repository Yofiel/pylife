#!/usr/bin/env python3
import random
import json


N = 10
BR = 3
P = 4

class Player:
    def __init__(self, name):
        self._name = name
        self._money = 1000
        self._position = 0

    def __str__(self):
        return f'Player: {self.name}; Saldo: {self.money}; Posição: {self.position}'

    @property
    def name(self):
        return self._name

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money):
        self._money = money

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position


def init_players():
    num = int(input('number of players: '))

    if not 2 <= num <= 4:
        print('Invalid... try again!')
        return init_players()

    players = []
    while True:
        name = input('player name: ')

        if not name or name.isspace():
            print('Invalid')
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

    print(f'Parabéns {winner.name}, você venceu com R$ {winner.money} e na posição {winner.position}!')

    print("\nRESULTADOS:")
    for player in players:
        print(player)


def confirmation_print():
    input('Pressione qualquer tecla para continuar.\n')


def bankruptcy_print(player):
    print(f'{player.name} faliu! Hora de dizer adeus...')
    print(f'{player.name} saiu do jogo!')


def end_match_print(player):
    print(f'Jogo finalizado! {player.name} chegou no fim da jornada, hora de contabilizar os saldos!')


def start_game(game_path, players):
    while True:
        for i in range(len(players)):
            print(f'Sua vez, {players[i].name}.')
            confirmation_print()

            drawn_number = spin_roulette()

            print(f'Número sorteado: {drawn_number}. Andando {drawn_number} casas!')
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

            print(f'{players[i].name} está na casa {players[i].position} com saldo de R$ {players[i].money}')
            confirmation_print()


def main():
    while True:
        players = init_players()
        sort_players(players)
        game_path = init_path()
        start_game(game_path, players)
        check_winner(players)

        decision = input('Deseja jogar outra partida? [S/n]: ')

        if decision.strip().lower() == 'n':
            print('Finalizando jogo...')
            break


if __name__ == "__main__":
    main()
