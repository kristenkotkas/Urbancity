# -*- coding: utf-8 -*-
import pygame
from Methods import update_events
from Classes import Game


def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mouse.set_visible(0)
    game = Game()
    game.initialize_all(game)
    clock = pygame.time.Clock()

    while game.running:
        clock.tick(game.fps_cap)
        pygame.display.set_caption("FPS: " + str(round(clock.get_fps(), 2)))
        update_events(game)
        game.allsprites.update(game)
        dirtyrects = game.allsprites.draw(game.screen)
        pygame.display.update(dirtyrects)
        if game.menu_running:
            pass

            # todo 1. new layereddirty, get displaysurface, blur it, use as background
            # todo fps läheb üliaeglaseks?

            # http://stackoverflow.com/questions/30723253/blurring-in-pygame

            # todo 2. or make superclass, blur all objects when game.menu_running
            # menu buttons n stuff on higher layers

    pygame.time.wait(50)
    pygame.quit()

if __name__ == '__main__':
    main()
