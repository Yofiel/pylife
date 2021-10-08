from sys import exit

import pygame

from service import create_players, init_path, sort_players

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

# posicao caminho
caminho = [
    (0, 0),
    (100, 0),
    (200, 0),
    (300, 0),
    (400, 0),
    (500, 0),
    (600, 0),
    (700, 0),
    (0, 100),
    (100, 100),
    (200, 100),
    (300, 100),
    (400, 100),
    (500, 100),
    (600, 100),
    (700, 100),
    (0, 200),
    (100, 200),
    (200, 200),
    (300, 200),
    (400, 200),
    (500, 200),
    (600, 200),
    (700, 200),
    (0, 300),
    (100, 300),
    (200, 300),
    (300, 300),
    (400, 300),
    (500, 300),
    (600, 300),
    (700, 300),
    (0, 400),
    (100, 400),
    (200, 400),
    (300, 400),
    (400, 400),
    (500, 400),
    (600, 400),
    (700, 400),
    (0, 500),
    (100, 500),
    (200, 500),
    (300, 500),
    (400, 500),
    (500, 500),
    (600, 500),
    (700, 500),
    (0, 600),
    (100, 600),
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


def board_view(players, path):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        # preenchendo background com cor
        WIN.fill(COLOR_BLACK)

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

        board_view(players, path)

        pygame.display.update()


if __name__ == "__main__":
    main()
