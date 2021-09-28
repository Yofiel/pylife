def results_text(players, removed_players, winner):
    text = f"--- PARTIDA ---\nVencedor:\n{winner}\nJogadores finalistas:\n"
    for player in players:
        text += str(player) + "\n"

    text += "Jogadores falidos:\n"
    if removed_players:
        for player in removed_players:
            text += str(player) + "\n"
    else:
        text += "NINGUÉM FALIU NESSA PARTIDA!\n"

    return text


def insert_players_number():
    value = input("Número de jogadores: ")
    return value


def insert_player_name():
    value = input("Nome do Player: ")
    return value


def invalid_players_quantity_print():
    print("Quantidade inválida. Tente novamente!")


def invalid_player_name_print():
    print("Nome inválido. Tente novamente!")


def confirmation_print():
    input("Pressione qualquer tecla para continuar.\n")


def bankruptcy_print(player):
    print(f"{player.name} faliu! Hora de dizer adeus...")
    print(f"{player.name} saiu do jogo!")


def end_match_print(player):
    print(
        f"Jogo finalizado! {player.name} chegou no fim da jornada, hora de contabilizar"
        + " os saldos!"
    )


def movement_print(drawn_number):
    print(f"Número sorteado: {drawn_number}. Andando {drawn_number} casas!")


def your_turn_print(player):
    print(f"Sua vez, {player.name}.")


def status_update_print(player):
    print(
        f"{player.name} está na casa {player.position} com saldo de R$ {player.money}"
    )


def results_print(players, removed_players, winner):
    print(results_text(players, removed_players, winner))
