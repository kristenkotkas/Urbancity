# Comment out these two lines to go back to old Pygame version
import pygame_sdl2
pygame_sdl2.import_as_pygame()

import pygame
from pygame import QUIT
import sys


class TestObj(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        # noinspection PyArgumentList
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.x = 0
        self.rect = self.image.get_rect()

    def update(self):
        self.x += 1
        self.rect.topleft = (self.x, 0)


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 50))
    clock = pygame.time.Clock()
    allsprites = pygame.sprite.LayeredDirty()
    allsprites.add(TestObj())
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
