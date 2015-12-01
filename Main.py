# -*- coding: utf-8 -*-
import pygame
from Methods import update_all
from Classes import Game

pygame.init()
game = Game()
game.initialize_all(game)

clock = pygame.time.Clock()
# update_all(game)
pygame.display.flip()


while game.running:
    game.tick = clock.tick(game.fps_cap)
    pygame.display.set_caption("FPS: " + str(round(clock.get_fps(), 2)))
    # update_all(game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            print((x, y))
    game.metro.draw_moving_metro(game)
    pygame.display.update(game.updatelist)
    game.updatelist = []

game.filesystem_do(game, "save_state")
pygame.time.wait(50)
pygame.quit()
