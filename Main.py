# -*- coding: utf-8 -*-
import pygame
from Methods import update_all, update_menu
from Classes import Game


def main():
    pygame.init()
    game = Game()
    game.initialize_all(game)
    # pygame.display.set_caption("Super Mäng 3000")

    clock = pygame.time.Clock()
    # update_all(game)
    # pygame.display.flip()

    while game.running:
        game.tick = clock.tick(game.fps_cap)
        pygame.display.set_caption("FPS: " + str(round(clock.get_fps(), 2)))
        if game.menu_running:
            update_menu(game)
        else:
            update_all(game)
        pygame.display.update(game.updatelist)
        game.updatelist = []

    game.filesystem_do(game, "save_state")
    pygame.time.wait(50)
    pygame.quit()

if __name__ == '__main__':
    main()
