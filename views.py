def insert_players_number():
    value = input('Número de jogadores: ')
    return value


def insert_player_name():
    value = input('Nome do Player: ')
    return value


def invalid_players_quantity_print():
    print('Quantidade inválida. Tente novamente!')


def invalid_player_name_print():
    print('Nome inválido. Tente novamente!')


def confirmation_print():
    input('Pressione qualquer tecla para continuar.\n')


def bankruptcy_print(player):
    print(f'{player.name} faliu! Hora de dizer adeus...')
    print(f'{player.name} saiu do jogo!')


def end_match_print(player):
    print(f'Jogo finalizado! {player.name} chegou no fim da jornada, hora de contabilizar os saldos!')


def movement_print(drawn_number):
    print(f'Número sorteado: {drawn_number}. Andando {drawn_number} casas!')


def your_turn_print(player):
    print(f'Sua vez, {player.name}.')


def status_update_print(player):
    print(f'{player.name} está na casa {player.position} com saldo de R$ {player.money}')


def results_print(players, winner):
    print(f'Parabéns {winner.name}, você venceu com R$ {winner.money} e na posição {winner.position}!')

    print("\nRESULTADOS:")
    for player in players:
        print(player)
