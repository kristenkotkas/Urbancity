import pygame
import Methods
import os.path
import shelve
from random import randint
main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
    def __init__(self):
        self.fps_cap = 60
        self.resolution = (1280, 720)
        self.screen_final = pygame.display.set_mode(self.resolution)
        # noinspection PyArgumentList
        self.screen = pygame.Surface(self.resolution)
        self.running = True
        self.menu_running = True
        self.tick = 0
        self.left_buttons = []
        self.right_buttons = []
        self.houses = [[], [], [], [], []]
        self.houses_states = [[], [], [], [], []]
        self.house_multiplier = 1.15
        """ houses_types struktuur [([a, [b, c, d]], [e, f, g], h, i, j, k), (sama), (sama), (sama), (sama)]
        sizetype(randtype[xbase, randtype[x laius/+vahe]], randtype[y], people, per people modifier, start price,
                                                                                                            minpeople)
        """
        self.houses_types = [([-15, [190, 125, 240]], [432, 347, 427], 10, 1, 1500, 0),
                             ([5, [90, 96, 0]], [340, 335, 0], 30, 3, 18000, 40),
                             ([-30, [103, 96, 0]], [255, 255, 0], 80, 8, 80000, 160),
                             ([-10, [130, 0, 0]], [115, 0, 0], 180, 18, 972000, 540),  # todo paika timmida kõik
                             ([-40, [180, 0, 0]], [15, 0, 0], 450, 45, 5062500, 1200)]  # todo 5 muuta
        self.bar_amounts = [0, 100, 0]
        self.right_button_names = ["Tüüp 1", "Tüüp 2", "Tüüp 3", "Tüüp 4", "Tüüp 5"]
        self.right_button_peopletotal = [0, 0, 0, 0, 0]
        self.right_button_amounts = [0, 0, 0, 0, 0]
        self.right_button_prices = [0, 0, 0, 0, 0]
        self.images = None
        self.cloud = None
        self.bar = None
        self.right_drawer = None
        self.left_drawer = None
        self.metro = None
        self.menu = None

    def initialize_all(self, game):
        self.images = Images()
        self.filesystem_do(game, "load_state")
        self.cloud = Cloud(game)
        self.bar = Bar(game)
        self.right_drawer = RightDrawer(game)
        # self.left_drawer = LeftDrawer(game)
        self.metro = Metro(game)
        self.menu = Menu(game)
        for sizetype in range(5):
            self.right_buttons.append(RightButton(game, sizetype))
            # self.left_buttons.append(LeftButton(game, sizetype))

    def filesystem_do(self, game, action):
        # file = os.path.join(main_dir, 'data\\test', "save_game")
        file = "C:\\save_game"
        if action == "load_state":
            # menüüs peaks load game vms olema kinni siis kui faili pole
            # https://docs.python.org/3.5/library/shelve.html
            d = shelve.open(file)
            keylist = d.keys()
            if len(keylist) != 0:
                for a in keylist:
                    print("key: " + a + ", data: " + str(d[a]))
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
        self.backgrounds = [Images.load_image("Background.png"), Images.load_image("Background_metro.png")]
        self.current_background = self.backgrounds[0]
        self.right_button = [Images.load_image("Button_available.png"), Images.load_image("Button_available_hover.png"),
                             Images.load_image("Button_unavailable.png")]
        self.right_button_logos = [Images.load_image("Maja_1_logo.png"), Images.load_image("Maja_2_logo.png"),
                                   Images.load_image("Maja_3_logo.png"), Images.load_image("Maja_4_logo.png"),
                                   Images.load_image("Maja_5_logo.png")]
        self.left_button = []
        self.bar = Images.load_image("riba.png")
        self.cloud = Images.load_image("pilv.png")
        self.houses = [
            [Images.load_image("Maja_11.png"), Images.load_image("Maja_12.png"), Images.load_image("Maja_13.png")],
            [Images.load_image("Maja_21.png"), Images.load_image("Maja_22.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_31.png"), Images.load_image("Maja_32.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_41.png"), Images.load_image("kell.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_51.png"), Images.load_image("kell.png"), Images.load_image("kell.png")]]
        self.metro = [Images.load_image("Metro.png"), Images.load_image("Metro_train.png"),
                      Images.load_image("Metro_overlay.png")]
        self.menu = [Images.load_image("kell.png"), Images.load_image("kell.png")]

    @staticmethod
    def load_image(file):
        file = os.path.join(main_dir, 'data', file)
        try:
            loaded_image = pygame.image.load(file)
        except:
            raise SystemExit("Could not load image " + file + ", " + pygame.get_error())
        return loaded_image.convert_alpha()


class Metro:
    def __init__(self, game):
        self.surface = game.screen
        self.image_metro = game.images.metro[0]
        self.image_train = game.images.metro[1]
        self.metrox = 377
        self.metroy = 576.306
        self.metrow = self.image_metro.get_rect().w
        self.metroh = self.image_metro.get_rect().h
        self.metrorect = pygame.Rect(self.metrox, self.metroy, self.metrow, self.metroh)
        self.trainx = self.metrox
        self.trainy = self.metroy + 50
        self.trainw = self.image_train.get_rect().w
        self.trainh = self.image_train.get_rect().h
        self.trainminx = 0
        self.trainmaxx = game.resolution[0] * 2
        game.images.current_background = game.images.backgrounds[1]

    def draw(self):
        self.draw_image()
        self.draw_moving_metro()

    def draw_image(self):
        self.surface.blit(self.image_metro, (self.metrox, self.metroy))

    def draw_moving_metro(self):
        if self.trainx < self.trainmaxx:
            self.trainx += 5
        else:
            self.trainx = 0
        if self.trainx + self.trainw > self.metrox and self.trainx < self.metrox + self.metrow:
            self.surface.blit(self.image_train, (self.trainx, self.trainy))


class House:
    def __init__(self, game, sizetype, randtype):
        self.sizetype = sizetype
        if randtype is None:
            self.randtype = randint(0, 2)
            # kui esimene maja luuakse siis võetakse siit info
            self.people = game.houses_types[self.sizetype][2]
            game.bar.calculate_houses_income(game, self.sizetype, game.houses_types[self.sizetype][2], 0, 0)
            game.bar.people += self.people
            # ajutine randtype määramine
            if self.sizetype == 3 or self.sizetype == 4:  # 4,5 tüüpi on 2 puudu
                self.randtype = 0
            elif self.sizetype == 2 or self.sizetype == 1:  # 2 ja 3 tüüpi maju on 1 puudu
                self.randtype = randint(0, 1)
        else:
            self.randtype = randtype
        self.surface = game.screen
        self.image = game.images.houses[self.sizetype][self.randtype]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = game.houses_types[self.sizetype][0][0]
        for house in game.houses[self.sizetype]:
            self.x += game.houses_types[house.sizetype][0][1][house.randtype]
        self.y = game.houses_types[self.sizetype][1][self.randtype]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

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
        self.y = 60
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
        self.maxx = 220
        self.x = self.minx
        self.y = 0
        self.w = 220
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
        self.minx = 1060
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


class LeftButton:  # right buttoni järgi tehtud, osad asjad puudu
    def __init__(self, game, sizetype):
        self.surface = game.screen
        self.sizetype = sizetype
        self.image_regular = game.images.right_button[0]
        self.image_highlighted = game.images.right_button[1]
        self.w = self.image_regular.get_rect().w
        self.h = self.image_regular.get_rect().h
        self.x = 20 - self.w
        self.y = 15 + 100 * self.sizetype
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.logo = game.images.right_button_logos[self.sizetype]
        self.name = game.right_button_names[self.sizetype]
        self.amount = game.right_button_amounts[self.sizetype]
        self.price = game.right_button_prices[self.sizetype]
        self.desc1 = game.right_button_desc1[self.sizetype]
        self.desc2 = game.right_button_desc2[self.sizetype]

    def draw(self, game, is_highlighted):
        if is_highlighted:
            self.surface.blit(self.image_highlighted, (self.x, self.y))
        else:
            self.surface.blit(self.image_regular, (self.x, self.y))
        Methods.draw_obj_middle(game, self.logo, (self.x, self.y), (7, 6.653), (47.25, 47.603))
        Methods.draw_obj_middle(game, self.amount, (self.x, self.y), (7, 62.178), (47.25, 19.256))
        Methods.draw_obj_middle(game, self.name, (self.x, self.y), (62.013, 7.216), (132.25, 19.256))
        Methods.draw_obj_middle(game, self.desc1, (self.x, self.y), (62.013, 34.394), (47.25, 19.256))
        Methods.draw_obj_middle(game, self.desc2, (self.x, self.y), (119, 34.394), (76, 19.256))
        Methods.draw_obj_middle(game, round(self.price), (self.x, self.y), (62.013, 62.178), (132.25, 19.256))

    def mouse_click_check(self, game, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.rect.collidepoint(x, y):
            self.amount += 1
            self.price = game.houses_types[self.sizetype][4] * game.house_multiplier ** self.amount
            Methods.create_house(game, self.sizetype, None)

    def mouse_hover_check(self, x, y):
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
        self.w = self.image_available.get_rect().w
        self.h = self.image_available.get_rect().h
        self.x = game.resolution[0] - 20
        self.y = 15 + 100 * self.sizetype
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.logo = game.images.right_button_logos[self.sizetype]
        self.name = game.right_button_names[self.sizetype]
        self.amount = game.right_button_amounts[self.sizetype]
        self.peopletotal = game.right_button_peopletotal[self.sizetype]
        self.price = game.houses_types[self.sizetype][4]
        self.people = game.houses_types[self.sizetype][2]

    def draw(self, game, is_highlighted):
        if not self.hidden:
            if game.bar.money >= self.price:
                if is_highlighted:
                    self.surface.blit(self.image_available_highlighted, (self.x, self.y))
                else:
                    self.surface.blit(self.image_available, (self.x, self.y))
            else:
                self.surface.blit(self.image_unavailable, (self.x, self.y))
            Methods.draw_obj_middle(game, self.logo, (self.x, self.y), (7, 6.653), (47.25, 47.603))
            Methods.draw_obj_middle(game, self.amount, (self.x, self.y), (7, 62.178), (47.25, 19.256))
            Methods.draw_obj_middle(game, self.name, (self.x, self.y), (62.013, 7.216), (132.25, 19.256))
            Methods.draw_obj_middle(game, self.people, (self.x, self.y), (69, 35), (47.25, 19.256))
            Methods.draw_obj_middle(game, self.peopletotal, (self.x, self.y), (119, 34.394), (76, 19.256))
            Methods.draw_obj_middle(game, round(self.price), (self.x, self.y), (62.013, 62.178), (132.25, 19.256))
        else:
            if game.bar.people >= game.houses_types[self.sizetype][5]:
                self.hidden = False

    def mouse_click_check(self, game, x, y):
        if not self.hidden:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if self.rect.collidepoint(x, y):
                if game.bar.money >= self.price:
                    game.bar.money -= self.price
                    self.amount += 1
                    self.peopletotal += self.people
                    self.price = game.houses_types[self.sizetype][4] * game.house_multiplier ** self.amount
                    Methods.create_house(game, self.sizetype, None)

    def mouse_hover_check(self, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.rect.collidepoint(x, y):
            return True


class Menu:
    def __init__(self, game):
        self.button_amount = 5
        self.x = [450, 650, 480, 595, 710]
        self.y = [200, 200, 300, 300, 300]
        self.w = [170, 170, 80, 80, 80]
        self.h = [80, 80, 50, 50, 50]
        self.rects = []
        self.buttons = []
        for i in range(self.button_amount):
            self.rects.append(pygame.Rect(self.x[i], self.y[i], self.w[i], self.h[i]))
            self.buttons.append(MenuButton(game, self.rects[i]))


class MenuButton:
    def __init__(self, game, rect):
        self.surface = game.screen
        self.rect = rect

    def draw(self, is_highlighted):
        if is_highlighted:
            self.surface.fill((255, 204, 0), self.rect)
        else:
            self.surface.fill((255, 153, 0), self.rect)

    def mouse_hover_check(self, x, y):
        if self.rect.collidepoint(x, y):
            return True

    def mouse_click_check(self, game, x, y):
        if self.rect.collidepoint(x, y):
            game.menu_running = False


class Bar:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.bar
        self.time_from_beginning = 0
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = 300
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
        per_people = 1.15 * game.houses_types[sizetype][3]
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
        Methods.draw_obj_middle(game, self.people, (self.x, self.y), (self.objxy[0][0], self.objxy[1]), self.objwh)
        Methods.draw_obj_middle(game, round(self.money), (self.x, self.y),
                                (self.objxy[0][1], self.objxy[1]), self.objwh)
        Methods.draw_obj_middle(game, round(self.income + self.income_manual), (self.x, self.y),
                                (self.objxy[0][2], self.objxy[1]), self.objwh)
