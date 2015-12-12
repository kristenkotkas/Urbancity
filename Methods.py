import pygame
import os.path
from random import randint
from Classes import House
main_dir = os.path.split(os.path.abspath(__file__))[0]


def update_menu(game):
    x, y = pygame.mouse.get_pos()
    game.background.draw(game)
    game.metro.draw(game)
    game.cloud.drawable = True
    for sizetype in reversed(game.houses):
        for house in sizetype:
            house.draw(game)
        if game.cloud.drawable:
            if len(sizetype) != 0:
                if sizetype[0].sizetype == 4:
                    game.cloud.draw()
                    game.cloud.drawable = False
            else:
                game.cloud.draw()
                game.cloud.drawable = False
    blursurface(game, 2.2)
    game.menu.draw()
    for button in game.menu.buttons:
        button.draw(game, button.mouse_hover_check(x, y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in game.menu.buttons:
                button.mouse_click_check(game, x, y)
    game.screen_final.blit(game.screen, (0, 0))


def update_game(game):
    x, y = pygame.mouse.get_pos()
    game.background.draw(game)
    game.metro.draw(game)
    game.cloud.drawable = True
    for sizetype in reversed(game.houses):
        for house in sizetype:
            house.draw(game)
        if game.cloud.drawable:
            if len(sizetype) != 0:
                if sizetype[0].sizetype == 4:
                    game.cloud.draw()
                    game.cloud.drawable = False
            else:
                game.cloud.draw()
                game.cloud.drawable = False
    game.right_drawer.mouse_hover_check(game, x, y)
    game.left_drawer.mouse_hover_check(game, x, y)
    for button in game.right_buttons + game.left_buttons:
        button.draw(game, button.mouse_hover_check(x, y))
    game.bar.update(game)
    game.news.draw(game)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT+1:
            game.bar.calculate_manual_income()
        elif event.type == pygame.USEREVENT+2:
            game.news.update()
        elif event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
            elif event.key == pygame.K_SPACE:
                manual_income = 100 + (game.bar.income + game.bar.people) / 15
                game.bar.money += manual_income
                game.bar.income_manual_data.append((manual_income, game.bar.income_manual_time))
                a = randint(1, 800)
                if a == 1:
                    game.bar.money /= 50
                    game.news.present("bad")
                elif a == 800:
                    game.bar.money *= 10
                    game.news.present("good")
            elif event.key == pygame.K_k:  # cheating
                game.bar.money += game.bar.money * 133700
            elif event.key == pygame.K_l:  # cheating
                game.bar.money = 0
            elif event.key == pygame.K_n:  # cheating
                game.bar.money /= 50
                game.news.present("bad")
            elif event.key == pygame.K_m:  # cheating
                game.bar.money *= 10
                game.news.present("good")
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in game.right_buttons + game.left_buttons:
                button.mouse_click_check(game, x, y)
    game.screen_final.blit(game.screen, (0, 0))


def blursurface(game, amount):  # amount > 1.0
    scale = 1.0 / float(amount)
    screen_size = game.screen.get_size()
    scale_size = (int(screen_size[0] * scale), int(screen_size[1] * scale))
    screen = pygame.transform.smoothscale(game.screen, scale_size)
    screen = pygame.transform.smoothscale(screen, screen_size)
    game.screen.blit(screen, (0, 0))


def create_house(game, sizetype, randtype):
    game.houses[sizetype].append(House(game, sizetype, randtype))


def draw_obj_middle(game, obj, main_obj_xy, inner_relative_xy, inner_obj_wh, drawdata):
    # "game obj", tekst/pilt, suure pildi xy, kasti xy pildi suhtes, kasti wh, teksti omadused
    if inner_relative_xy == 0:
        inner_obj_xy = main_obj_xy
    else:
        inner_obj_xy = (main_obj_xy[0] + inner_relative_xy[0], main_obj_xy[1] + inner_relative_xy[1])
    if inner_obj_xy[0] > game.resolution[0]:
        return
    if isinstance(obj, str) or isinstance(obj, int):
        if isinstance(obj, int):
            obj = str(format(obj, ",d"))
        txt_font = pygame.font.SysFont("centurygothic", drawdata[1], True)
        final_obj = txt_font.render(obj, True, drawdata[0])
        final_obj_size = txt_font.size(obj)
    else:
        final_obj = obj
        final_obj_size = final_obj.get_rect().size
    final_obj_xy = (inner_obj_xy[0] + (inner_obj_wh[0] - final_obj_size[0]) / 2, inner_obj_xy[1] +
                    (inner_obj_wh[1] - final_obj_size[1]) / 2)
    game.screen.blit(final_obj, final_obj_xy)
