import pygame
import Methods
import os.path
import shelve
from random import randint
main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
    def __init__(self):
        self.fps_cap = 60
        # self.screen_final = pygame.display.set_mode((640, 360), pygame.FULLSCREEN)
        self.screen_final = pygame.display.set_mode((1280, 720))
        self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        # noinspection PyArgumentList
        self.screen = pygame.Surface(self.resolution)
        self.running = True
        self.menu_running = True
        self.difficulty = 1
        self.tick = 0
        self.house_multiplier = 1.15
        self.left_buttons = []
        self.right_buttons = []
        self.houses = [[], [], [], [], []]
        self.houses_states = [[], [], [], [], []]
        self.right_button_names = ["Tüüp 1", "Tüüp 2", "Tüüp 3", "Tüüp 4", "Tüüp 5"]
        # houses_types = sizetype(randtype[xbase, randtype[x laius/+vahe]], randtype[y from bottom])
        self.houses_types = [([-15, [190, 125, 240, 125]], [432, 347, 427, 347]),
                             ([5, [90, 96, 0]], [340, 335, 0]),
                             ([-30, [103, 96, 0]], [255, 255, 0]),
                             ([-10, [130, 0, 0]], [115, 0, 0]),
                             ([-40, [170, 0, 0]], [73, 0, 0])]
        self.houses_properties = None
        self.right_button_prices_fixed = None
        self.right_button_prices = [0, 0, 0, 0, 0]
        self.right_button_peopletotal = [0, 0, 0, 0, 0]
        self.right_button_amounts = [0, 0, 0, 0, 0]
        self.bar_amounts = [0, 0, 0]
        self.images = None
        self.background = None
        self.cloud = None
        self.bar = None
        self.right_drawer = None
        self.left_drawer = None
        self.metro = None
        self.menu = None

    def initialize_menu(self, game):
        self.images = Images()
        self.filesystem_do(game, "load_state")
        self.set_difficulty(self.difficulty)
        self.background = Background(game)
        self.cloud = Cloud(game)
        self.bar = Bar(game)
        self.right_drawer = RightDrawer(game)
        self.left_drawer = LeftDrawer(game)
        self.metro = Metro(game)
        self.menu = Menu(game)

    def initialize_game(self, game):
        self.set_difficulty(self.difficulty)
        self.right_buttons = []
        self.left_buttons = []
        self.houses = [[], [], [], [], []]
        self.houses_states = [[], [], [], [], []]
        self.right_button_peopletotal = [0, 0, 0, 0, 0]
        self.right_button_amounts = [0, 0, 0, 0, 0]
        self.bar_amounts = [0, 0, 0]
        self.bar = Bar(game)
        for sizetype in range(5):
            self.right_buttons.append(RightButton(game, sizetype))
            self.left_buttons.append(LeftButton(game, sizetype))

    def set_difficulty(self, difficulty):
        # houses_properties = sizetype(people, per people modifier, minpeople)
        if difficulty == 0:  # easy
            self.houses_properties = [
                (200, 0.2, 0), (900, 0.4, 1200), (2560, 1, 7680), (7200, 1.8, 32400), (13500, 6, 90000)]
            self.right_button_prices_fixed = [750, 9000, 40000, 486000, 2531250]
        elif difficulty == 1:  # normal
            self.houses_properties = [
                (100, 0.1, 0), (450, 0.2, 600), (1280, 0.5, 2560), (3600, 0.9, 108000), (6750, 3, 180000)]
            self.right_button_prices_fixed = [1500, 18000, 80000, 972000, 5062500]
        elif difficulty == 2:  # insane
            self.houses_properties = [
                (50, 0.1, 0), (220, 0.2, 2000), (640, 0.3, 7000), (1800, 0.5, 30000), (3300, 1.5, 46000)]
            self.right_button_prices_fixed = [3000, 36000, 160000, 1944000, 10125000]

    def filesystem_do(self, game, action):
        file = os.path.join(main_dir, 'data', "save_game")
        if action == "load_state":
            d = shelve.open(file)
            keylist = d.keys()
            if len(keylist) != 0:
                for a in keylist:
                    print("key: " + a + ", data: " + str(d[a]))
                self.difficulty = d["difficulty"]
                self.houses_states = d["houses_states"]
                self.right_button_amounts = d["right_button_amounts"]
                self.right_button_prices = d["right_button_prices"]
                self.right_button_peopletotal = d["right_button_peopletotal"]
                self.bar_amounts = [d["people"], d["money"], d["income"]]
            d.close()
            self.set_loaded_states(game)
        elif action == "save_state":
            self.get_current_states()
            d = shelve.open(file)
            d["houses_states"] = self.houses_states
            d["right_button_amounts"] = self.right_button_amounts
            d["right_button_prices"] = self.right_button_prices
            d["right_button_peopletotal"] = self.right_button_peopletotal
            d["people"] = self.bar.people
            d["money"] = self.bar.money
            d["income"] = self.bar.income
            d["difficulty"] = self.difficulty
            d.close()

    def get_current_states(self):
        for button in range(len(self.right_buttons)):
            self.right_button_amounts[button] = self.right_buttons[button].amount
            self.right_button_prices[button] = self.right_buttons[button].price
            self.right_button_peopletotal[button] = self.right_buttons[button].peopletotal
        self.houses_states = [[], [], [], [], []]
        for sizetype in self.houses:
            for house in sizetype:
                self.houses_states[house.sizetype].append([house.sizetype, house.randtype])

    def set_loaded_states(self, game):
        for sizetype in self.houses_states:
            for house in sizetype:
                Methods.create_house(game, house[0], house[1])


class Images:
    def __init__(self):
        self.background = Images.load_image("Background.png")
        self.right_button = [Images.load_image("Button_available.png"), Images.load_image("Button_available_hover.png"),
                             Images.load_image("Button_unavailable.png")]
        self.right_button_logos = [Images.load_image("Maja_1_logo.png"), Images.load_image("Maja_2_logo.png"),
                                   Images.load_image("Maja_3_logo.png"), Images.load_image("Maja_4_logo.png"),
                                   Images.load_image("Maja_5_logo.png")]
        self.left_button = [Images.load_image("Upgrade.png"), Images.load_image("Upgrade_hover.png"),
                            Images.load_image("Maks.png"), Images.load_image("Maks_hover_minus.png"),
                            Images.load_image("Maks_hover_plus.png")]
        self.bar = Images.load_image("riba.png")
        self.cloud = Images.load_image("pilv.png")
        self.houses = [
            [Images.load_image("Maja_11.png"), Images.load_image("Maja_12.png"), Images.load_image("Maja_13.png"),
             Images.load_image("Maja_14.png")],
            [Images.load_image("Maja_21.png"), Images.load_image("Maja_22.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_31.png"), Images.load_image("Maja_32.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_41.png"), Images.load_image("kell.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_51.png"), Images.load_image("kell.png"), Images.load_image("kell.png")]]
        self.metro = [Images.load_image("Metro.png"), Images.load_image("Metro_train.png"),
                      Images.load_image("Metro_overlay.png")]
        self.menu = [[Images.load_image("urbancity_logo.png")],
                     [Images.load_image("Menu_big_button.png"), Images.load_image("Menu_big_button_hover.png"),
                     Images.load_image("Menu_small_button.png"), Images.load_image("Menu_small_button_hover.png")]]

    @staticmethod
    def load_image(file):
        file = os.path.join(main_dir, 'data', file)
        try:
            loaded_image = pygame.image.load(file)
        except:
            raise SystemExit("Could not load image " + file + ", " + pygame.get_error())
        return loaded_image.convert_alpha()


class Background:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.background
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.rect = None
        self.skysize = 540
        self.groundsize = 180
        self.timesy = (game.resolution[1] - self.groundsize) // self.skysize
        self.timesx = game.resolution[0] // self.w
        self.skyarearect = pygame.Rect(0, 0, self.w, self.skysize)
        self.skyendarearect = pygame.Rect(0, 0, game.resolution[0] - self.w * self.timesx, self.skysize)
        self.groundarearect = pygame.Rect(
            0, self.skysize - (game.resolution[1] - self.skysize * self.timesy - self.groundsize), self.w, self.h)
        self.groundendarearect = pygame.Rect(
            0, self.skysize - (game.resolution[1] - self.skysize * self.timesy - self.groundsize),
            game.resolution[0] - self.w * self.timesx, self.h)

    def draw(self, game):
        for row in range(int(self.timesy)):
            for column in range(int(self.timesx)):
                self.rect = pygame.Rect(self.w * column, self.skysize * row, self.w, self.skysize)
                self.surface.blit(self.image, self.rect, self.skyarearect)
            self.rect = pygame.Rect(self.w * self.timesx, self.skysize * row, self.w, self.skysize)
            self.surface.blit(self.image, self.rect, self.skyendarearect)
        for column in range(int(self.timesx)):
            self.rect = pygame.Rect(
                self.w * column, self.skysize * self.timesy, self.w, game.resolution[1] - self.skysize * self.timesy)
            self.surface.blit(self.image, self.rect, self.groundarearect)
        self.rect = pygame.Rect(self.w * self.timesx, self.skysize * self.timesy, self.w, self.groundsize)
        self.surface.blit(self.image, self.rect, self.groundendarearect)


class Metro:
    def __init__(self, game):
        self.surface = game.screen
        self.image_metro = game.images.metro[0]
        self.image_train = game.images.metro[1]
        self.metrow = self.image_metro.get_rect().w
        self.metroh = self.image_metro.get_rect().h
        self.metrox = (game.resolution[0] - self.metrow) / 2
        self.metroy = game.resolution[1] - 144
        self.metrorect = pygame.Rect(self.metrox, self.metroy, self.metrow, self.metroh)
        self.trainx = self.metrox
        self.trainy = self.metroy + 50
        self.trainw = self.image_train.get_rect().w - 2
        self.trainh = self.image_train.get_rect().h
        self.trainrect = pygame.Rect(self.metrox, self.metroy + 50, self.trainw, self.trainh)
        self.arearect = pygame.Rect(self.trainw, 0, self.trainw, self.trainh)
        self.counter = 0
        self.speed = 0  # 4
        self.time_from_beginning = 0

    def draw(self, game):
        self.draw_metro_background()
        self.calculate_speed(game)
        self.draw_moving_metro()

    def draw_metro_background(self):
        self.surface.blit(self.image_metro, self.metrorect)

    # näiteks 1000ms jooksul peab edasi liikuma 100px ehk 1ms jooksul 0.1px
    # frame ajad 60 50 110 20 80 90 230 70 290
    # konstantselt peab edasi liikuma, kui eelmise frame peale l2ks kauem aega siis j2rgmine frame peab selle v2rra rohkem liikuma
    #
    def calculate_speed(self, game):
        self.speed = 0.1 * game.tick
        # print(game.tick)

    def draw_moving_metro(self):
        # kui rongi parem pool pole metro paremast poolest möödunud
        if self.trainrect.x + self.trainrect.w < self.metrorect.x + self.metrow:
            # kui rong pole välja joonistatud
            if self.arearect.x > 0:
                self.arearect.x -= self.speed  # joonistab rongi
            else:
                self.trainrect.x += self.speed  # liigutab tervet rongi edasi
        # kui rong on välja joonistatud
        elif self.arearect.x > -self.trainw:
            self.arearect.x -= self.speed  # kustutab rongi
        else:
            self.counter += 1
            if self.counter > 300:
                self.trainrect.x = self.metrox
                self.arearect.x = self.trainw
                self.arearect.w = self.trainw
                self.counter = 0
        self.surface.blit(self.image_train, self.trainrect, self.arearect)


class House:
    def __init__(self, game, sizetype, randtype):
        self.sizetype = sizetype
        if randtype is None:
            self.people = game.houses_properties[self.sizetype][0]
            game.bar.calculate_houses_income(game, self.sizetype, game.houses_properties[self.sizetype][0], 0, 0)
            game.bar.people += self.people
            # ajutine randtype määramine
            if self.sizetype == 0:  # 1 tüüpi on 4 maja
                self.randtype = randint(0, 3)
            elif self.sizetype == 3 or self.sizetype == 4:  # 4,5 tüüpi on 2 puudu
                self.randtype = 0
            elif self.sizetype == 2 or self.sizetype == 1:  # 2 ja 3 tüüpi maju on 1 puudu
                self.randtype = randint(0, 1)
                if len(game.houses[sizetype]) > 1:  # kiire fix erinevate t22pide genereerimisele
                    self.last_randtype = game.houses[sizetype][-1].randtype
                    self.last2_randtype = game.houses[sizetype][-2].randtype
                    if self.randtype == self.last_randtype and self.randtype == self.last2_randtype:
                        if self.randtype == 0:
                            self.randtype = 1
                        else:
                            self.randtype = 0
        else:
            self.randtype = randtype
        self.surface = game.screen
        self.image = game.images.houses[self.sizetype][self.randtype]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = game.houses_types[self.sizetype][0][0]
        for house in game.houses[self.sizetype]:
            self.x += game.houses_types[house.sizetype][0][1][house.randtype]
        self.y = game.houses_types[self.sizetype][1][self.randtype] + game.resolution[1] - 720
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        print(self.randtype, self.y)

    def draw(self, game):
        if self.x < game.resolution[0]:
            self.surface.blit(self.image, (self.x, self.y))


class Cloud:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.cloud
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = -self.w
        self.y = game.resolution[1] * 60 / 720
        self.minx = -self.w
        self.maxx = game.resolution[0]
        self.drawable = True

    def draw(self):
        if self.x < self.maxx:
            self.x += 1
        else:
            self.x = self.minx
        if self.minx < self.x < self.maxx:
            self.surface.blit(self.image, (self.x, self.y))


class LeftDrawer:
    def __init__(self, game):
        self.surface = game.screen
        self.minx = 20
        self.maxx = 160
        self.x = self.minx
        self.y = 0
        self.w = 170
        self.h = game.resolution[1]
        self.rect = pygame.Rect(0, self.y, self.w, self.h)

    def mouse_hover_check(self, game, x, y):
        if self.rect.collidepoint(x, y):
            if self.x < self.maxx:
                self.x += 20
                for button in game.left_buttons:
                    button.x += 20
        else:
            if self.x > self.minx:
                self.x -= 20
                for button in game.left_buttons:
                    button.x -= 20


class RightDrawer:
    def __init__(self, game):
        self.surface = game.screen
        self.minx = game.resolution[0] - 220
        self.maxx = game.resolution[0] - 20
        self.x = self.maxx
        self.y = 0
        self.w = game.resolution[0] - self.minx
        self.h = game.resolution[1]
        self.rect = pygame.Rect(self.minx, self.y, self.w, self.h)

    def mouse_hover_check(self, game, x, y):
        if self.rect.collidepoint(x, y):
            if self.x > self.minx:
                self.x -= 20
                for button in game.right_buttons:
                    button.x -= 20
        else:
            if self.x < self.maxx:
                self.x += 20
                for button in game.right_buttons:
                    button.x += 20


class LeftButton:
    def __init__(self, game, sizetype):
        self.surface = game.screen
        self.sizetype = sizetype
        self.drawdata = [(255, 255, 255), 14]
        if self.sizetype == 0:
            self.image_regular = game.images.left_button[2]
            self.image_minus = game.images.left_button[3]
            self.image_plus = game.images.left_button[4]
        else:
            self.image_regular = game.images.left_button[0]
            self.image_highlighted = game.images.left_button[1]
        self.w = self.image_regular.get_rect().w
        self.h = self.image_regular.get_rect().h
        self.x = 20 - self.w
        self.y = 15 + 75 * self.sizetype
        if self.sizetype == 0:
            self.minusrect = pygame.Rect(self.x + 30, self.y + 50, 20, 20)
            self.plusrect = pygame.Rect(self.x + 90, self.y + 50, 20, 20)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, game, is_highlighted):
        if self.sizetype != 0 and is_highlighted:
            self.surface.blit(self.image_highlighted, (self.x, self.y))
        elif self.sizetype == 0:
            if is_highlighted == "minus":
                self.surface.blit(self.image_minus, (self.x, self.y))
            elif is_highlighted == "plus":
                self.surface.blit(self.image_plus, (self.x, self.y))
            elif is_highlighted == 0:
                self.surface.blit(self.image_regular, (self.x, self.y))
        else:
            self.surface.blit(self.image_regular, (self.x, self.y))

    def mouse_click_check(self, game, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.rect.collidepoint(x, y):
            print("left button clicked", self.sizetype, self.w)

    def mouse_hover_check(self, x, y):
        if self.sizetype == 0:
            self.minusrect = pygame.Rect(self.x + 30, self.y + 40, 38, 20)
            self.plusrect = pygame.Rect(self.x + 90, self.y + 40, 38, 20)
            if self.minusrect.collidepoint(x, y):
                return "minus"
            elif self.plusrect.collidepoint(x, y):
                return "plus"
            else:
                return 0
        else:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if self.rect.collidepoint(x, y):
                return True


class RightButton:
    def __init__(self, game, sizetype):
        self.hidden = True
        self.surface = game.screen
        self.sizetype = sizetype
        self.image_available = game.images.right_button[0]
        self.image_available_highlighted = game.images.right_button[1]
        self.image_unavailable = game.images.right_button[2]
        self.drawdata = [(255, 255, 255), 14]
        self.w = self.image_available.get_rect().w
        self.h = self.image_available.get_rect().h
        self.x = game.resolution[0] - 20
        self.y = 15 + 100 * self.sizetype
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.logo = game.images.right_button_logos[self.sizetype]
        self.name = game.right_button_names[self.sizetype]
        self.amount = game.right_button_amounts[self.sizetype]
        self.peopletotal = game.right_button_peopletotal[self.sizetype]
        if self.amount > 0:
            self.price = game.right_button_prices[self.sizetype]
        else:
            self.price = game.right_button_prices_fixed[self.sizetype]
        self.people = game.houses_properties[self.sizetype][0]

    def draw(self, game, is_highlighted):
        if not self.hidden:
            if game.bar.money >= self.price:
                if is_highlighted:
                    self.surface.blit(self.image_available_highlighted, (self.x, self.y))
                else:
                    self.surface.blit(self.image_available, (self.x, self.y))
            else:
                self.surface.blit(self.image_unavailable, (self.x, self.y))
            Methods.draw_obj_middle(game, self.logo, (self.x, self.y), (7, 6.653), (47.25, 47.603), self.drawdata)
            Methods.draw_obj_middle(game, self.amount, (self.x, self.y), (7, 62.178), (47.25, 19.256), self.drawdata)
            Methods.draw_obj_middle(game, self.name, (self.x, self.y), (62.013, 7.216), (132.25, 19.256), self.drawdata)
            Methods.draw_obj_middle(game, self.people, (self.x, self.y), (71, 35), (47.25, 19.256), self.drawdata)
            Methods.draw_obj_middle(game, self.peopletotal, (self.x, self.y), (119, 34.394), (76, 19.256),
                                    self.drawdata)
            Methods.draw_obj_middle(game, round(self.price), (self.x, self.y), (62.013, 62.178), (132.25, 19.256),
                                    self.drawdata)
        else:
            if game.bar.people >= game.houses_properties[self.sizetype][2]:
                self.hidden = False

    def mouse_click_check(self, game, x, y):
        if not self.hidden:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if self.rect.collidepoint(x, y):
                if game.bar.money >= self.price:
                    game.bar.money -= self.price
                    self.amount += 1
                    self.peopletotal += self.people
                    self.price = game.right_button_prices_fixed[self.sizetype] * game.house_multiplier ** self.amount
                    Methods.create_house(game, self.sizetype, None)

    def mouse_hover_check(self, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.rect.collidepoint(x, y):
            return True


class Menu:
    def __init__(self, game):
        self.surface = game.screen
        self.button_amount = 5
        self.names = ["new game", "continue", "easy", "normal", "insane"]
        self.actions = []
        self.xmodifier = [-20, 20, -92, 0, 92]
        self.y = [200, 200, 280, 280, 280]
        self.sizetype = [0, 0, 2, 2, 2]
        self.buttons = []
        self.is_highlighted_button = 3
        for i in range(self.button_amount):
            self.buttons.append(MenuButton(
                game, (self.xmodifier[i], game.resolution[1] * self.y[i] / 720), self.sizetype[i], i, self.names[i]))
        self.image = game.images.menu[0][0]
        self.imagew = self.image.get_rect().w
        self.imageh = self.image.get_rect().h
        self.imagex = (game.resolution[0] - self.imagew) / 2
        self.imagey = game.resolution[1] * 90 / 720
        self.rect = pygame.Rect(self.imagex, self.imagey, self.imagew, self.imageh)

    def draw(self):
        self.surface.blit(self.image, self.rect)


class MenuButton:
    def __init__(self, game, xy, sizetype, stype, name):
        self.surface = game.screen
        self.sizetype = sizetype
        self.stype = stype
        self.drawdata = []
        if self.sizetype == 0:
            self.drawdata.append((61, 61, 61))
        else:
            self.drawdata.append((255, 255, 255))
        self.drawdata.append(26)
        self.name = name
        self.image = game.images.menu[1][self.sizetype]
        self.image_highlighted = game.images.menu[1][self.sizetype + 1]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        if xy[0] > 0:
            self.x = (game.resolution[0] / 2) + xy[0]
        elif xy[0] < 0:
            self.x = (game.resolution[0] / 2) - self.w + xy[0]
        else:
            self.x = (game.resolution[0] - self.w) / 2
        self.rect = pygame.Rect(self.x, xy[1], self.w, self.h)

    def draw(self, game, is_highlighted):
        if is_highlighted or self.stype == game.menu.is_highlighted_button:
            self.surface.blit(self.image_highlighted, self.rect)
        else:
            self.surface.blit(self.image, self.rect)
        Methods.draw_obj_middle(game, self.name, (self.rect.x, self.rect.y - 3), 0, (self.w, self.h), self.drawdata)

    def mouse_hover_check(self, x, y):
        if self.rect.collidepoint(x, y):
            return True

    def mouse_click_check(self, game, x, y):
        if self.rect.collidepoint(x, y):
            if self.stype == 0:
                game.initialize_game(game)
                game.menu_running = False
            elif self.stype == 1:
                if game.bar_amounts[0] == 0 and game.bar_amounts[0] == 0:
                    pass
                else:
                    game.menu_running = False
            else:
                game.difficulty = self.stype - 2
                game.menu.is_highlighted_button = self.stype


class Bar:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.bar
        self.time_from_beginning = 0
        self.drawdata = [(255, 255, 255), 14]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = (game.resolution[0] - self.w) / 2
        self.y = 6
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.people = game.bar_amounts[0]
        self.money = game.bar_amounts[1]
        self.income = game.bar_amounts[2]
        self.income_manual = 0
        self.income_manual_time = 0
        self.income_manual_data = []
        pygame.time.set_timer(pygame.USEREVENT+1, 100)
        self.objxy = ((19.591, 254.095, 488.6), 7.413)
        self.objwh = (148, 21.621)
        self.objh = 21.621

    def update(self, game):
        self.calculate_money(game)
        self.income_manual_time += game.tick
        self.draw(game)

    def calculate_manual_income(self):
        if len(self.income_manual_data) > 0:
            self.income_manual = 0
            temp_list = []
            for i in range(len(self.income_manual_data)):
                if not self.income_manual_time - self.income_manual_data[i][1] > 1000:
                    temp_list.append(self.income_manual_data[i])
            self.income_manual_data = temp_list
            for value in self.income_manual_data:
                self.income_manual += value[0]
        else:
            self.income_manual = 0

    @staticmethod
    def calculate_houses_income(game, sizetype, people, tax, special):
        per_people = 1.15 * game.houses_properties[sizetype][1]
        from_people = people * per_people
        per_special = 1
        from_special = special * per_special
        taxed_income = (from_people + from_special) * (1 + tax / 100)
        game.bar.income += taxed_income

    def calculate_money(self, game):
        self.time_from_beginning += game.tick
        if self.time_from_beginning < 10:  # less than 10ms per frame
            game.bar.money += game.bar.income / 1000 * self.time_from_beginning / 1
        elif self.time_from_beginning < 100:  # less than 100ms per frame
            game.bar.money += game.bar.income / 100 * self.time_from_beginning / 10
        elif self.time_from_beginning < 1000:  # less than 1000ms per frame
            game.bar.money += game.bar.income / 10 * self.time_from_beginning / 100
        self.time_from_beginning = 0

    def draw(self, game):
        self.surface.blit(self.image, (self.x, self.y))
        Methods.draw_obj_middle(game, self.people, (self.x, self.y),
                                (self.objxy[0][0], self.objxy[1]), self.objwh, self.drawdata)
        Methods.draw_obj_middle(game, round(self.money), (self.x, self.y),
                                (self.objxy[0][1], self.objxy[1]), self.objwh, self.drawdata)
        Methods.draw_obj_middle(game, round(self.income + self.income_manual), (self.x, self.y),
                                (self.objxy[0][2], self.objxy[1]), self.objwh, self.drawdata)
