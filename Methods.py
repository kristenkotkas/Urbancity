import pygame
import os.path
from random import randint
main_dir = os.path.split(os.path.abspath(__file__))[0]


def update_common(game):
    x, y = pygame.mouse.get_pos()
    game.background.draw(game)
    if game.fiber is not None:
        game.fiber.draw()
    if game.watersupply is not None:
        game.watersupply.draw()
    if game.metro is not None:
        game.metro.draw(game)
    if game.pipe is not None:
        game.pipe.draw()
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
    if game.power is not None:
        game.power.draw()
    return x, y


def update_menu(game):
    x, y = update_common(game)
    blursurface(game, 2.2)
    game.menu.draw()
    for button in game.menu.buttons:
        button.draw(game, button.mouse_hover_check(x, y))
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT+4:
            if game.metro is not None:
                game.metro.update_metro_counter()
        elif event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in game.menu.buttons:
                button.mouse_click_check(game, x, y)
    game.cursor.draw((x, y))
    game.screen_final.blit(game.screen, (0, 0))


def update_game(game):
    x, y = update_common(game)
    game.right_drawer.mouse_hover_check(game, x, y)
    game.left_drawer.mouse_hover_check(game, x, y)
    for button in game.right_buttons + game.tax_buttons + game.upgrade_buttons:
        button.draw(game, button.mouse_hover_check(x, y))
    game.bar.update(game)
    game.news.draw(game)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT+1:
            game.bar.calculate_manual_income()
        elif event.type == pygame.USEREVENT+2:
            game.news.update()
        elif event.type == pygame.USEREVENT+3:
            for sizetype in game.houses:
                for house in sizetype:
                    house.calculate_taxmax()
        elif event.type == pygame.USEREVENT+4:
            if game.metro is not None:
                game.metro.update_metro_counter()
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
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in game.right_buttons + game.tax_buttons + game.upgrade_buttons:
                button.mouse_click_check(game, x, y)
    game.cursor.draw((x, y))
    game.screen_final.blit(game.screen, (0, 0))


def blursurface(game, amount):  # amount > 1.0
    scale = 1.0 / float(amount)
    screen_size = game.screen.get_size()
    scale_size = (int(screen_size[0] * scale), int(screen_size[1] * scale))
    screen = pygame.transform.smoothscale(game.screen, scale_size)
    screen = pygame.transform.smoothscale(screen, screen_size)
    game.screen.blit(screen, (0, 0))


def draw_obj(game, middle, obj, main_obj_xy, inner_relative_xy, inner_obj_wh, drawdata, end):
    # "game obj", keskel, tekst/pilt, suure pildi xy, kasti xy pildi suhtes, kasti wh, teksti omadused, teksti lõpp
    if inner_relative_xy == 0:
        inner_obj_xy = main_obj_xy
    else:
        inner_obj_xy = (main_obj_xy[0] + inner_relative_xy[0], main_obj_xy[1] + inner_relative_xy[1])
    if inner_obj_xy[0] > game.resolution[0] or inner_obj_wh != 0 and inner_obj_xy[0] + inner_obj_wh[0] < 0:
        return
    if isinstance(obj, str) or isinstance(obj, int):
        if isinstance(obj, int):
            obj = str(format(obj, ",d"))
            if end != 0:
                obj += end
        txt_font = pygame.font.SysFont("centurygothic", drawdata[1], True)
        final_obj = txt_font.render(obj, True, drawdata[0])
        final_obj_size = txt_font.size(obj)
    else:
        final_obj = obj
        final_obj_size = final_obj.get_rect().size
    if middle:
        final_obj_xy = (inner_obj_xy[0] + (inner_obj_wh[0] - final_obj_size[0]) / 2, inner_obj_xy[1] +
                        (inner_obj_wh[1] - final_obj_size[1]) / 2)
    else:
        final_obj_xy = (inner_obj_xy[0], inner_obj_xy[1])
    game.screen.blit(final_obj, final_obj_xy)
