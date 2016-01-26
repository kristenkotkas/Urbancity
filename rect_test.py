# https://github.com/renpy/pygame_sdl2/issues/31

# Comment out these two lines to go back to old Pygame version
import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame import QUIT
import sys


class WhiteSquare(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        # noinspection PyArgumentList
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 1


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 50))
    clock = pygame.time.Clock()

    allsprites = pygame.sprite.LayeredDirty()
    allsprites.add(WhiteSquare())

    # noinspection PyArgumentList
    background = pygame.Surface((500, 50))
    screen.blit(background, (0, 0))
    pygame.display.flip()
    allsprites.clear(screen, background)

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

        allsprites.update()
        dirtyrects = allsprites.draw(screen)
        pygame.display.update(dirtyrects)

if __name__ == '__main__':
    main()
