import pygame
import os.path
from random import randint
from Classes import Maja
main_dir = os.path.split(os.path.abspath(__file__))[0]


def update_all(andmed):
    x, y = pygame.mouse.get_pos()
    andmed.metro.draw()
    andmed.screen.blit(andmed.pildid.current_background, (0, 0))
    andmed.pilv.draw()
    for sizetype in reversed(andmed.majad):
        for maja in sizetype:
            maja.draw(andmed)
    pygame.draw.line(andmed.screen, (255, 255, 255), (x, 0), (x, andmed.resolution[1] - 1))  # ülevalt alla
    pygame.draw.line(andmed.screen, (255, 255, 255), (0, y), (andmed.resolution[0] - 1, y))  # vasakult paremale
    andmed.parem_sahtel.mouse_hover_check(andmed, x, y)
    # andmed.vasak_sahtel.mouse_hover_check(andmed, x, y)
    for nupp in andmed.parem_nupud + andmed.vasak_nupud:
        nupp.draw(andmed, nupp.mouse_hover_check(x, y))
    andmed.riba.update(andmed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            andmed.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                andmed.running = False
            elif event.key == pygame.K_SPACE:
                andmed.riba.money += 100 + (andmed.riba.income + andmed.riba.people) / 15
                # andmed.riba.income_data.append(100 + (andmed.riba.income + andmed.riba.people) / 15)
                a = randint(1, 800)
                if a == 1:
                    print("space event, cash / 50")
                    andmed.riba.money /= 50
                elif a == 800:
                    print("space event, cash * 10")
                    andmed.riba.money *= 10
            elif event.key == pygame.K_k:  # cheating
                andmed.riba.money += (andmed.riba.income + 100) * 1337
            elif event.key == pygame.K_l:  # cheating
                andmed.riba.money = 0
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print((x, y))
            for nupp in andmed.parem_nupud + andmed.vasak_nupud:
                nupp.mouse_click_check(andmed, x, y)
    # blursurface(andmed, 3.0)


def blursurface(andmed, amount):
    scale = 1.0 / float(amount)
    screen_size = andmed.screen.get_size()
    scale_size = (int(screen_size[0] * scale), int(screen_size[1] * scale))
    screen = pygame.transform.smoothscale(andmed.screen, scale_size)
    screen = pygame.transform.smoothscale(screen, screen_size)
    andmed.surface.blit(screen, (0, 0))


def create_house(andmed, sizetype, randtype):
    andmed.majad[sizetype].append(Maja(andmed, sizetype, randtype))


def kuva_obj_keskele(andmed, obj, main_obj_xy, inner_relative_xy, inner_obj_wh):
    # tekst/pilt, suure pildi xy, kasti xy pildi suhtes, kasti wh
    if inner_relative_xy == 0:
        inner_obj_xy = main_obj_xy
    else:
        inner_obj_xy = (main_obj_xy[0] + inner_relative_xy[0], main_obj_xy[1] + inner_relative_xy[1])
    if inner_obj_xy[0] > andmed.resolution[0]:
        return
    if isinstance(obj, str) or isinstance(obj, int):
        if isinstance(obj, int):
                obj = str(format(obj, ",d"))
        txt_font = pygame.font.SysFont("centurygothic", 14, True)
        final_obj = txt_font.render(obj, True, (255, 255, 255))
        final_obj_size = txt_font.size(obj)
    else:
        final_obj = obj
        final_obj_size = final_obj.get_rect().size
    final_obj_xy = (inner_obj_xy[0] + (inner_obj_wh[0] - final_obj_size[0]) / 2, inner_obj_xy[1] +
                    (inner_obj_wh[1] - final_obj_size[1]) / 2)
    andmed.screen.blit(final_obj, final_obj_xy)
