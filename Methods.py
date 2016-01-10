import pygame
import os.path
main_dir = os.path.split(os.path.abspath(__file__))[0]


def update_events(game):
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT+4:
            if game.metro is not None:
                game.metro.update_metro_counter()
        elif event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.sounds.click.play()
