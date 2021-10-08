import tkinter as tk
from sys import exit
from tkinter import messagebox

import pygame

from service import create_players, init_path, sort_players, spin_roulette, start_round

# tamanhos
WIDTH = 800
HEIGHT = 600

# cores
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
COLOR_GREEN = pygame.Color(1, 91, 32)
COLOR_RED = pygame.Color(240, 0, 0)

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
caminho = [
    (93, 558),
    (115, 509),
    (97, 451),
    (112, 402),
    (71, 362),
    (67, 305),
    (81, 250),
    (65, 207),
    (123, 199),
    (88, 150),
    (65, 102),
    (82, 60),
    (135, 34),
    (139, 83),
    (162, 117),
    (188, 164),
    (230, 137),
    (236, 94),
    (231, 50),
    (305, 52),
    (318, 92),
    (358, 62),
    (389, 102),
    (358, 139),
    (316, 174),
    (294, 216),
    (278, 263),
    (274, 310),
    (316, 353),
    (348, 389),
    (368, 427),
    (389, 466),
    (410, 502),
    (442, 470),
    (428, 432),
    (437, 400),
    (484, 387),
    (434, 356),
    (473, 328),
    (369, 293),
    (428, 284),
    (482, 276),
    (535, 264),
    (576, 232),
    (630, 250),
    (640, 285),
    (588, 303),
    (616, 340),
    (638, 378),
    (638, 422),
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
                        if len(user_text) < 25:
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

        # caixa de input acompanha o tamanho da camada de texto
        input_rect.w = max(140, input_text.get_width() + 10)

        # desenhando botao
        draw_text_box(WIN, button_text, button_rect, COLOR_GREEN)

        # atualizando tela
        pygame.display.update()


def send_message(message, title="Aviso"):
    root = tk.Tk()
    root.overrideredirect(1)
    root.withdraw()
    messagebox.showinfo(title, message)
    root.destroy()


def board_view(players, path, removed_players):
    # definicao do botao da roleta
    spin_roulette_text = create_text("SORTEAR NUMERO", COLOR_WHITE)
    spin_roulette_rect = create_text_box(300, 560)

    current_player = -1
    while True:
        if current_player == 3:
            current_player = -1

        current_player += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if spin_roulette_rect.collidepoint(event.pos):
                    drawn_number = spin_roulette()
                    send_message(f"NÚMERO SORTEADO: {drawn_number}")
                    start_round(
                        path, players[current_player], removed_players, drawn_number
                    )
                    print(players[current_player])

        # preenchendo background com imagem
        WIN.blit(BOARD, (0, 0))

        # desenhando retangulo e texto do input na tela
        spin_roulette_rect.w = spin_roulette_text.get_width() + 10
        draw_text_box(WIN, spin_roulette_text, spin_roulette_rect, COLOR_BLACK)

        # atualizando tela
        pygame.display.update()


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
        players = create_players(names)
        sort_players(players)
        path = init_path()
        removed_players = []

        board_view(players, path, removed_players)

        pygame.display.update()


if __name__ == "__main__":
    main()
