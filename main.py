import tkinter as tk
from sys import exit
from tkinter import messagebox

import pygame

from service import (
    check_winner,
    create_players,
    init_path,
    is_over,
    sort_players,
    spin_roulette,
    start_round,
)

# tamanhos
WIDTH = 800
HEIGHT = 600

# cores
COLOR_BLACK = pygame.Color(0, 0, 0)
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
BOARD = pygame.image.load("assets/map.png")

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
    (463, 308),
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


def draw_text_box(window, text, rect, rect_color, border=0):
    pygame.draw.rect(window, rect_color, rect, border)
    window.blit(text, (rect.x + 5, rect.y + 5))


def name_input_view():
    user_text = ""
    names = []

    # definicao da caixa de texto para nome
    input_rect = pygame.Rect(200, 200, 140, 32)
    input_rect_active_color = pygame.Color(0, 0, 200)
    input_rect_inactive_color = pygame.Color(240, 240, 240)
    input_rect_error_color = pygame.Color(COLOR_RED)
    input_rect_current_color = input_rect_inactive_color

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
                    if not user_text or user_text.isspace() or not user_text.isalpha():
                        error = True
                        break
                    else:
                        error = False

                    names.append(user_text)
                    user_text = ""

                    if len(names) == 4:
                        return names

            if event.type == pygame.KEYDOWN:
                # lendo o que é digitado
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        if len(user_text) < 10:
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

        # criando camada para o texto
        input_text = create_text(user_text, COLOR_WHITE, FONT)

        # desenhando retangulo e texto do input na tela
        draw_text_box(WIN, input_text, input_rect, input_rect_current_color, 2)

        # desenhando botao
        draw_text_box(WIN, button_text, button_rect, COLOR_GREEN)

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
    root.overrideredirect(1)
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()


def init_players_sprites(players):
    players_sprites = []

    for player in players:
        player_sprite = pygame.sprite.Sprite()
        player_sprite.image = pygame.image.load(f"assets/{player.color}.svg")
        player_sprite.rect = player_sprite.image.get_rect()
        players_sprites.append(player_sprite)

    return players_sprites


def blit_players(players, players_sprites):
    for index, sprite in enumerate(players_sprites):
        sprite.rect.topleft = POSITIONS[players[index].position]

        if pygame.sprite.spritecollideany(sprite, players_sprites):
            sprite.rect.x += index * 5

        WIN.blit(sprite.image, sprite.rect)


def board_view(players, players_sprites, path, removed_players):
    # definicao do botao da roleta
    spin_roulette_text = create_text("SORTEAR NUMERO", COLOR_WHITE)
    spin_roulette_rect = create_text_box(300, 560)

    current_player = -1
    while True:
        if current_player == len(players) - 1:
            current_player = -1

        current_player += 1

        # preenchendo background com imagem
        WIN.blit(BOARD, (0, 0))

        # desenhando retangulo e texto do input na tela
        spin_roulette_rect.w = spin_roulette_text.get_width() + 10
        draw_text_box(WIN, spin_roulette_text, spin_roulette_rect, COLOR_BLACK)

        blit_players(players, players_sprites)

        # atualizando tela
        pygame.display.update()

        if is_over(players[current_player], removed_players):
            winner = check_winner(players)
            send_message("Jogo finalizado!", "Fim da jornada")
            send_message(f"{winner.name}, você é o vencedor", "Parabéns")

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
                    start_round(
                        path, players[current_player], removed_players, drawn_number
                    )
                    print(players[current_player])
                    event_happened = True

        if players[current_player] in removed_players:
            players.pop(current_player)
            players_sprites.pop(current_player)
            current_player -= 1


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        names = name_input_view()
        colors = color_input_view(names)
        players = create_players(names, colors)
        sort_players(players)
        players_sprites = init_players_sprites(players)
        path = init_path()
        removed_players = []

        board_view(players, players_sprites, path, removed_players)

        pygame.display.update()


if __name__ == "__main__":
    main()
