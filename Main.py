# -*- coding: utf-8 -*-
import pygame
from Methods import update_all
from Classes import Andmed

pygame.init()
andmed = Andmed()
andmed.init_all(andmed)

clock = pygame.time.Clock()
update_all(andmed)
pygame.display.flip()

while andmed.running:
    andmed.tick = clock.tick(andmed.fps_cap)
    pygame.display.set_caption("FPS: " + str(round(clock.get_fps(), 2)))
    update_all(andmed)
    pygame.display.flip()

# andmed.filesystem_do(andmed, "save_state")
pygame.time.wait(50)
pygame.quit()
