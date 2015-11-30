# -*- coding: utf-8 -*-
import pygame
from Methods import update_all
from Classes import Game

pygame.init()
game = Game()
game.initialize_all(game)

clock = pygame.time.Clock()
update_all(game)
pygame.display.flip()

while game.running:
    game.tick = clock.tick(game.fps_cap)
    pygame.display.set_caption("FPS: " + str(round(clock.get_fps(), 2)))
    update_all(game)
    pygame.display.flip()

# game.filesystem_do(game, "save_state")
pygame.time.wait(50)
pygame.quit()
