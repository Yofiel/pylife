import tkinter as tk
from os.path import join
from sys import exit
from tkinter import messagebox

import pygame

from .service import *

# tamanhos
WIDTH = 800
HEIGHT = 600

# cores
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_DARK_GRAY = pygame.Color(51, 51, 51)
COLOR_GRAY = pygame.Color(82, 82, 82)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_GREEN = pygame.Color(1, 91, 32)
COLOR_RED = pygame.Color(240, 0, 0)
COLOR_BLUE = pygame.Color(0, 0, 255)
COLOR_YELLOW = pygame.Color(255, 255, 0)

# inicializando jogo
pygame.init()

# fps
FPS = 60

# propriedades da janela
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pylife")

# definindo fonte base
FONT = pygame.font.Font(None, 32)

# carregando background
BOARD = pygame.image.load(join("assets", "img", "map.png"))

# posicao caminho
POSITIONS = [
    (83, 538),
    (105, 489),
    (87, 431),
    (102, 382),
    (61, 342),
    (57, 285),
    (71, 230),
    (55, 187),
    (113, 179),
    (78, 130),
    (55, 82),
    (72, 40),
    (125, 14),
    (129, 63),
    (152, 97),
    (178, 144),
    (220, 117),
    (226, 74),
    (221, 30),
    (295, 32),
    (308, 72),
    (348, 42),
    (379, 82),
    (348, 119),
    (306, 154),
    (284, 196),
    (268, 243),
    (264, 290),
    (306, 333),
    (338, 369),
    (358, 407),
    (379, 446),
    (400, 482),
    (432, 450),
    (418, 412),
    (427, 380),
    (474, 367),
    (424, 336),
    (359, 308),
    (359, 273),
    (418, 264),
    (472, 256),
    (525, 244),
    (566, 212),
    (620, 230),
    (630, 265),
    (578, 283),
    (606, 320),
    (628, 358),
    (628, 402),
]


def create_text(text, color, font=None, size=24, style=None):
    if not font:
        font = pygame.font.Font(style, size)

    return font.render(text, True, color)


def create_text_box(x, y, width=100, height=30):
    return pygame.Rect(x, y, width, height)


def draw_text_box(window, text, rect, rect_color, border=0, border_radius=0):
    pygame.draw.rect(window, rect_color, rect, border, border_radius=border_radius)
    window.blit(text, (rect.x + 5, rect.y + 5))


def menu_view():
    new_game_text = create_text("NOVO JOGO", COLOR_WHITE, size=40)
    new_game_rect = create_text_box(315, 210, width=180, height=35)

    rank_text = create_text("TOP PLAYERS", COLOR_WHITE, size=40)
    rank_rect = create_text_box(300, 260, width=210, height=35)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_rect.collidepoint(event.pos):
                    # 1 indica novo jogo
                    return 1

                if rank_rect.collidepoint(event.pos):
                    # 2 indica rank
                    return 2

        WIN.fill(COLOR_BLACK)

        # desenhando botao do new_game
        draw_text_box(WIN, new_game_text, new_game_rect, COLOR_BLUE, border_radius=2)

        # desenhando botao do rank
        draw_text_box(WIN, rank_text, rank_rect, COLOR_DARK_GRAY, border_radius=2)

        # atualizando tela
        pygame.display.update()


def rank_view():
    return_text = create_text("VOLTAR PARA MENU", COLOR_WHITE)
    return_rect = create_text_box(305, 100, width=180)

    rank_rect = create_text_box(230, 210, width=345, height=100)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        WIN.fill(COLOR_BLACK)

        # desenhando botao de voltar para menu
        draw_text_box(WIN, return_text, return_rect, COLOR_RED, border_radius=2)

        # desenhando retangulo e texto do live rank na tela
        players = get_best_players()

        rank_text = ""
        for player in players:
            rank_text += (
                f"Jogador(a) {player[0]} - Quantidade de vitórias: {player[1]}" + "\n"
            )

        pygame.draw.rect(WIN, COLOR_GRAY, rank_rect, border_radius=8)
        blit_multiline_text(rank_rect, rank_text)

        # atualizando tela
        pygame.display.update()

        event_happened = False
        while not event_happened:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if return_rect.collidepoint(event.pos):
                        return


def name_input_view():
    user_text = ""
    names = []

    # definicao da caixa de texto para nome
    input_rect = pygame.Rect(200, 200, 140, 32)
    input_rect_active_color = pygame.Color(0, 0, 200)
    input_rect_inactive_color = pygame.Color(240, 240, 240)
    input_rect_error_color = pygame.Color(COLOR_RED)
    input_rect_current_color = input_rect_inactive_color

    # texto informativo
    info_text = create_text("Informe o nome do jogador", COLOR_WHITE)

    # definicao do botao de confirmacao do nome
    button_text = create_text("Confirmar", COLOR_WHITE)
    button_rect = create_text_box(200, 240)

    active = False
    error = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

                if button_rect.collidepoint(event.pos):
                    if (
                        not user_text
                        or user_text.isspace()
                        or not user_text.isalpha()
                        or user_text.upper() in names
                    ):
                        error = True
                        break
                    else:
                        error = False

                    names.append(user_text.upper())
                    user_text = ""

                    if len(names) == 4:
                        return names

            if event.type == pygame.KEYDOWN:
                # lendo o que é digitado
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        if len(user_text) < 8:
                            user_text += event.unicode

        # preenchendo background com cor
        WIN.fill(COLOR_BLACK)

        # atualizando cor do input
        if active:
            input_rect_current_color = input_rect_active_color
        else:
            input_rect_current_color = input_rect_inactive_color

        if error:
            input_rect_current_color = input_rect_error_color

        # desenhando texto informativo
        WIN.blit(info_text, (200, 180))

        # criando camada para o texto
        input_text = create_text(user_text, COLOR_WHITE, FONT)

        # desenhando retangulo e texto do input na tela
        draw_text_box(
            WIN, input_text, input_rect, input_rect_current_color, 2, border_radius=2
        )

        # desenhando botao
        draw_text_box(WIN, button_text, button_rect, COLOR_GREEN, border_radius=2)

        # atualizando tela
        pygame.display.update()


def color_input_view(players):
    colors = []

    blue_rect = create_text_box(200, 230, 40, 40)
    red_rect = create_text_box(250, 230, 40, 40)
    green_rect = create_text_box(300, 230, 40, 40)
    yellow_rect = create_text_box(350, 230, 40, 40)

    current_player = -1
    while True:
        if current_player == 3:
            return colors

        current_player += 1

        # preenchendo background com cor
        WIN.fill(COLOR_BLACK)

        info_text = create_text(
            f"{players[current_player]}, escolha uma cor", COLOR_WHITE
        )

        WIN.blit(info_text, (200, 200))

        pygame.draw.rect(WIN, COLOR_BLUE, blue_rect)
        pygame.draw.rect(WIN, COLOR_RED, red_rect)
        pygame.draw.rect(WIN, COLOR_GREEN, green_rect)
        pygame.draw.rect(WIN, COLOR_YELLOW, yellow_rect)

        # atualizando tela
        pygame.display.update()

        event_happened = False
        while not event_happened:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if blue_rect.collidepoint(event.pos):
                    color = "azul"
                elif red_rect.collidepoint(event.pos):
                    color = "vermelho"
                elif green_rect.collidepoint(event.pos):
                    color = "verde"
                elif yellow_rect.collidepoint(event.pos):
                    color = "amarelo"
                else:
                    continue

                if color in colors:
                    send_message("Essa cor já foi escolhida. Escolha outra!")
                else:
                    colors.append(color)
                    event_happened = True


def send_message(message, title="Aviso"):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()


def init_players_sprites(players):
    players_sprites = []

    for player in players:
        player_sprite = pygame.sprite.Sprite()
        player_sprite.image = pygame.image.load(
            join("assets", "img", f"{player.color}.svg")
        )
        player_sprite.rect = player_sprite.image.get_rect()
        players_sprites.append(player_sprite)

    return players_sprites


def blit_players(players, players_sprites):
    for index, sprite in enumerate(players_sprites):
        sprite.rect.topleft = POSITIONS[players[index].position]

        if pygame.sprite.spritecollideany(sprite, players_sprites):
            sprite.rect.x += index * 5

        WIN.blit(sprite.image, sprite.rect)


def rank_text_formatter(players):
    text = ""
    for player in players:
        text += str(player) + "\n"

    return text


def blit_multiline_text(rect, text, color=COLOR_WHITE):
    max_width, _ = rect.size
    x, y = rect.x + 5, rect.y + 5

    for line in text.splitlines():
        line_surface = create_text(line, color, size=20)
        # line_surface = font.render(line, 0, color)
        line_width, line_height = line_surface.get_size()
        if x + line_width >= max_width:
            x = rect.x + 5
            y += line_height
        WIN.blit(line_surface, (x, y))


def board_view(players, players_sprites, path, removed_players):
    # definicao do botao da roleta
    spin_roulette_rect = create_text_box(300, 560)

    # definicao da caixa do placar
    live_rank_rect = create_text_box(450, 5, 345, 100)

    current_space = ()
    current_player = -1
    while True:
        if current_player == len(players) - 1:
            current_player = -1

        current_player += 1

        # preenchendo background com imagem
        WIN.blit(BOARD, (0, 0))

        # criando texto do botao de sorteio
        spin_roulette_text = create_text(
            f"{players[current_player].name} ({players[current_player].color}),"
            + " sorteie um número!",
            COLOR_WHITE,
        )

        # desenhando retangulo e texto do input na tela
        spin_roulette_rect.w = spin_roulette_text.get_width() + 10
        draw_text_box(
            WIN,
            spin_roulette_text,
            spin_roulette_rect,
            COLOR_DARK_GRAY,
            border_radius=3,
        )

        # desenhando retangulo e texto do live rank na tela
        live_rank_text = rank_text_formatter(players)
        pygame.draw.rect(WIN, COLOR_GRAY, live_rank_rect, border_radius=8)
        blit_multiline_text(live_rank_rect, live_rank_text)

        # desenha os jogadores
        blit_players(players, players_sprites)

        # atualizando tela
        pygame.display.update()

        event_happened = False
        while not event_happened:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if spin_roulette_rect.collidepoint(event.pos):
                    drawn_number = spin_roulette()
                    send_message(f"NÚMERO SORTEADO: {drawn_number}")
                    current_space = move_player(
                        path, players[current_player], removed_players, drawn_number
                    )
                    event_happened = True
                else:
                    send_message('Clique em "SORTEIE UM NÚMERO!"')

        if current_space:
            WIN.blit(BOARD, (0, 0))
            blit_players(players, players_sprites)
            pygame.display.update()
            send_message(f"{current_space[1]}", f"{players[current_player].name}")

        if players[current_player] in removed_players:
            send_message(f"Jogador(a) {players[current_player].name} faliu!", "Bye Bye")
            players.pop(current_player)
            players_sprites.pop(current_player)
            current_player -= 1

        if is_over(players[current_player], removed_players):
            WIN.blit(BOARD, (0, 0))
            blit_players(players, players_sprites)
            pygame.display.update()
            winner = check_winner(players)
            send_message("Jogo finalizado!", "Fim da jornada")
            send_message(
                f"{winner.name}, você GANHOU com R$ {winner.money}!", "Parabéns"
            )
            return winner


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # True significa que o jogador estara no menu
        while True:
            choice = menu_view()

            if choice == 1:
                break
            elif choice == 2:
                rank_view()

        names = name_input_view()
        colors = color_input_view(names)
        players = create_players(names, colors)
        sort_players(players)
        players_sprites = init_players_sprites(players)
        path = init_path()
        removed_players = []

        winner = board_view(players, players_sprites, path, removed_players)
        save_game_result(winner)

        pygame.display.update()
