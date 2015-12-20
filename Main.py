# -*- coding: utf-8 -*-
import pygame
from Methods import update_game, update_menu
from Classes import Game


def main():
    pygame.init()
    game = Game()
    game.initialize_menu(game)
    clock = pygame.time.Clock()
    pygame.display.set_caption("Urbancity")

    while game.running:
        game.tick = clock.tick(game.fps_cap)
        # pygame.display.set_caption("FPS: " + str(round(clock.get_fps(), 2)))
        if game.menu_running:
            update_menu(game)
        else:
            update_game(game)
        pygame.display.flip()

    if not game.menu_running:
        game.filesystem_do(game, "save_state")
    pygame.time.wait(50)
    pygame.quit()

if __name__ == '__main__':
    main()
