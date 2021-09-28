from sys import exit

import pygame
from pygame.locals import QUIT

WIDTH = 800
HEIGHT = 600
BACKGROUND_COLOR = pygame.Color(0, 0, 0)

# inicializando jogo
pygame.init()
clock = pygame.time.Clock()
main_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pylife")

# definindo fonte base
base_font = pygame.font.Font(None, 32)


def init_players_view():
    user_text = ""

    # caixa do input de texto e cor do mesmo
    input_rect = pygame.Rect(200, 200, 140, 32)
    input_rect_active_color = pygame.Color(0, 0, 200)
    input_rect_inactive_color = pygame.Color(240, 240, 240)
    input_rect_current_color = input_rect_inactive_color
    active = False

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
            if event.type == pygame.KEYDOWN:
                # lendo o que é digitado
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        if len(user_text) < 25:
                            user_text += event.unicode

        # preenchendo background com cor
        main_surface.fill(BACKGROUND_COLOR)

        # atualizando cor do input
        if active:
            input_rect_current_color = input_rect_active_color
        else:
            input_rect_current_color = input_rect_inactive_color

        # desenhando retangulo do input na tela
        pygame.draw.rect(main_surface, input_rect_current_color, input_rect, 2)

        # criando camada para o texto
        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # desenhando camanda de texto na tela na posicao da caixa de input
        main_surface.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # caixa de input acompanha o tamanho da camada de texto
        input_rect.w = max(140, text_surface.get_width() + 10)

        # atualizando tela parcialmente
        pygame.display.flip()

        clock.tick(60)


# Game loop
init_players_view()

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

pygame.display.update()
clock.tick(15)
