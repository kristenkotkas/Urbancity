import pygame
import Methods
import os.path
import shelve
from random import randint
main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
    def __init__(self):
        self.fps_cap = 60
        # self.screen_final = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_final = pygame.display.set_mode((1280, 720))
        self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        # noinspection PyArgumentList
        self.screen = pygame.Surface(self.resolution)
        self.running = True
        self.menu_running = True
        self.difficulty = 1
        self.tick = 0
        self.tax_buttons = []
        self.upgrade_buttons = []
        self.right_buttons = []
        self.houses = [[], [], [], [], []]
        self.houses_states = [[], [], [], [], []]
        self.taxes = [["Beard Tax", 0], ["Goat Tax", 0], ["Weed Tax", 0]]
        self.right_button_names = ["Dwelling", "Low-end", "High-end", "Luxury", "Skyscraper"]
        # houses_types = sizetype(randtype[xbase, randtype[x laius/+vahe]], randtype[y from bottom])
        self.houses_types = [([-15, [190, 125, 240, 125]], [432, 347, 427, 347]),
                             ([5, [90, 96, 242]], [340, 335, 328]),
                             ([-30, [103, 96, 170]], [255, 255, 250]),
                             ([-10, [130, 180, 0]], [115, 130, 0]),
                             ([-40, [170, 135, 0]], [73, 59, 0])]
        # upgrades = name{box}, cost{box}, (reward type{box}, amount/reward), (unlock type{priv}, amount{priv})
        self.upgrades = [("Google Fiber", 400000, ("perspecial", 100), ("people", 2000)),
                         ("Santa Claus", 800000, ("special", 666), ("houses", 20)),
                         ("Metro", 200000, ("unlock", "Metro"), ("income", 3000)),
                         ("Plumbing", 20000, ("unlock", "Pipe"), ("houses", 10))]
        self.usedupgrades = []
        self.houses_properties = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.right_button_prices_fixed = [0, 0, 0, 0, 0]
        self.right_button_prices = [0, 0, 0, 0, 0]
        self.right_button_peopletotal = [0, 0, 0, 0, 0]
        self.right_button_amounts = [0, 0, 0, 0, 0]
        self.bar_amounts = [0, 0, 0, 0, 1]
        self.images = None
        self.background = None
        self.cloud = None
        self.bar = None
        self.right_drawer = None
        self.left_drawer = None
        self.metro = None
        self.menu = None
        self.news = None
        self.pipe = None

    def initialize_menu(self, game):
        self.images = Images()
        self.filesystem_do(game, "load_state")
        self.background = Background(game)
        self.cloud = Cloud(game)
        for upgrade in self.usedupgrades:
            if upgrade == "Metro":
                self.metro = Metro(game)
            elif upgrade == "Plumbing":
                self.pipe = Pipe(game)
        self.menu = Menu(game)

    def initialize_game(self, game, state):
        if state == "new":
            self.difficulty = game.menu.is_highlighted_button - 2
            self.right_buttons = []
            self.tax_buttons = []
            self.upgrade_buttons = []
            self.houses = [[], [], [], [], []]
            self.houses_states = [[], [], [], [], []]
            self.right_button_peopletotal = [0, 0, 0, 0, 0]
            self.right_button_amounts = [0, 0, 0, 0, 0]
            self.bar_amounts = [0, 0, 0, 0, 1]
            self.usedupgrades = []
            self.metro = None
            self.pipe = None
        self.set_difficulty(self.difficulty)
        self.right_drawer = RightDrawer(game)
        self.left_drawer = LeftDrawer(game)
        self.bar = Bar(game)
        self.news = News(game)
        for sizetype in range(5):
            self.right_buttons.append(RightButton(game, sizetype))
        for sizetype in range(3):
            self.tax_buttons.append(TaxButton(game, sizetype))

    def initialize_unlock(self, game, unlocktype):
        if unlocktype == "Metro":
            self.metro = Metro(game)
        elif unlocktype == "Pipe":
            self.pipe = Pipe(game)

    def set_difficulty(self, difficulty):
        # houses_properties = sizetype(people, per people modifier, minpeople)
        if difficulty == 0:  # easy
            self.houses_properties = [
                (200, 0.2, 0), (900, 0.4, 600), (2560, 1, 3500), (7200, 1.8, 10800), (13500, 6, 27000)]
            self.right_button_prices_fixed = [750, 9000, 40000, 486000, 2531250]
        elif difficulty == 1:  # normal
            self.houses_properties = [
                (100, 0.1, 0), (450, 0.2, 700), (1280, 0.5, 4000), (3600, 0.9, 18000), (6750, 3, 40000)]
            self.right_button_prices_fixed = [1500, 18000, 80000, 972000, 5062500]
        elif difficulty == 2:  # insane
            self.houses_properties = [
                (50, 0.1, 0), (220, 0.2, 1000), (640, 0.3, 6000), (1800, 0.5, 24000), (3300, 1.5, 54000)]
            self.right_button_prices_fixed = [3000, 36000, 160000, 1944000, 10125000]

    def filesystem_do(self, game, action):
        file = os.path.join(main_dir, 'data', "save_game")
        if action == "load_state":
            d = shelve.open(file)
            keylist = d.keys()
            for key in keylist:
                print("key:", key + ", data:", d[key])
            if len(keylist) != 0:
                self.difficulty = d["difficulty"]
                self.houses_states = d["houses_states"]
                self.right_button_amounts = d["right_button_amounts"]
                self.right_button_prices = d["right_button_prices"]
                self.right_button_peopletotal = d["right_button_peopletotal"]
                self.bar_amounts = [d["people"], d["money"], d["income"], d["special"], d["perspecial"]]
                self.usedupgrades = d["usedupgrades"]
                self.taxes = d["taxes"]
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
            d["special"] = self.bar.special
            d["perspecial"] = self.bar.perspecial
            d["difficulty"] = self.difficulty
            d["usedupgrades"] = self.usedupgrades
            d["taxes"] = self.taxes
            d.close()

    def get_current_states(self):
        for button in range(len(self.right_buttons)):
            self.right_button_amounts[button] = self.right_buttons[button].amount
            self.right_button_prices[button] = self.right_buttons[button].price
            self.right_button_peopletotal[button] = self.right_buttons[button].peopletotal
        self.houses_states = [[], [], [], [], []]
        for sizetype in self.houses:
            for house in sizetype:
                self.houses_states[house.sizetype].append([house.sizetype, house.randtype, house.people])

    def set_loaded_states(self, game):
        for sizetype in self.houses_states:
            for house in sizetype:
                game.houses[house[0]].append(House(game, house[0], house[1], house[2]))


class Images:
    def __init__(self):
        self.background = Images.load_image("Background.png")
        self.right_button = [Images.load_image("Button_available.png"), Images.load_image("Button_available_hover.png"),
                             Images.load_image("Button_unavailable.png")]
        self.right_button_logos = [Images.load_image("House_1_logo.png"), Images.load_image("House_2_logo.png"),
                                   Images.load_image("House_3_logo.png"), Images.load_image("House_4_logo.png"),
                                   Images.load_image("House_5_logo.png")]
        self.left_button = [Images.load_image("Tax.png"), Images.load_image("Tax_hover_minus.png"),
                            Images.load_image("Tax_hover_plus.png")]
        self.upgrade_button = [Images.load_image("Upgrade_available.png"), Images.load_image("Upgrade_unavailable.png"),
                               Images.load_image("Upgrade_available_hover.png")]
        self.bar = Images.load_image("Bar.png")
        self.misc = [Images.load_image("Cloud.png"), Images.load_image("Breaking_news.png"),
                     Images.load_image("Pipe.png")]
        self.houses = [
            [Images.load_image("House_11.png"), Images.load_image("House_12.png"), Images.load_image("House_13.png"),
             Images.load_image("House_14.png")],
            [Images.load_image("House_21.png"), Images.load_image("House_22.png"), Images.load_image("House_23.png")],
            [Images.load_image("House_31.png"), Images.load_image("House_32.png"), Images.load_image("House_33.png")],
            [Images.load_image("House_41.png"), Images.load_image("House_42.png"),
             Images.load_image("PLACEHOLDER.png")],
            [Images.load_image("House_51.png"), Images.load_image("House_52.png"),
             Images.load_image("PLACEHOLDER.png")]]
        self.metro = [Images.load_image("Metro.png"), Images.load_image("Metro_train.png")]
        self.menu = [[Images.load_image("Urbancity_logo.png")],
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
        self.speed = 4  # 4
        self.time_from_beginning = 0
        pygame.time.set_timer(pygame.USEREVENT + 3, 100)

    def draw(self):
        self.draw_metro_background()
        self.update_metro()
        self.draw_moving_metro()

    def draw_metro_background(self):
        self.surface.blit(self.image_metro, self.metrorect)

    def update_metro(self):
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

    def draw_moving_metro(self):
        self.surface.blit(self.image_train, self.trainrect, self.arearect)


class News:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.misc[1]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = -self.w
        self.y = game.resolution[1] - game.resolution[1] / 3
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.presenttxt = "General txt"
        self.drawdata = [(0, 0, 0), 20]
        self.drawing = False
        self.counter = 1800
        self.speed = 10

    def present(self, eventtype):
        pygame.time.set_timer(pygame.USEREVENT + 2, 10)
        if eventtype == "bad":
            self.presenttxt = "Terrorists have blown up the city's money reserves!".upper()
        elif eventtype == "good":
            self.presenttxt = "A reindeer has been spotted by the local bank!".upper()
        self.drawing = True
        self.counter = 3000

    def update(self):
        if self.drawing:
            if self.x + self.w < self.w - 5:
                self.x += self.speed
            else:
                self.drawing = False
        else:
            if self.counter < 0:
                if self.x + self.w > 0:
                    self.x -= self.speed
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 2, 0)
                    self.counter = 1800
            else:
                self.counter -= self.speed

    def draw(self, game):
        if self.x + self.w > 0:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            self.surface.blit(self.image, self.rect)
            Methods.draw_obj(game, False, self.presenttxt, (self.x, self.y), (135, 60), 0, self.drawdata, 0)


class Pipe:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.misc[2]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = -10
        self.y = game.resolution[1] - self.h + 10
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        self.surface.blit(self.image, self.rect)


class House:
    def __init__(self, game, sizetype, randtype, people):
        self.surface = game.screen
        self.sizetype = sizetype
        self.peoplemax = game.houses_properties[self.sizetype][0]
        self.people = people
        if randtype is None:
            game.bar.people += self.people
            # ajutine randtype määramine
            if self.sizetype == 0:  # 1 tüüpi on 4 maja
                self.randtype = randint(0, 3)
            elif 2 < self.sizetype:  # 2,4,5 tüüpi on 1 puudu
                self.randtype = randint(0, 1)
            else:  # tüüp 2,3
                self.randtype = randint(0, 2)
            if len(game.houses[sizetype]) > 1:  # kiire fix erinevate t22pide genereerimisele
                self.last_randtype = game.houses[sizetype][-1].randtype
                self.last2_randtype = game.houses[sizetype][-2].randtype
                if self.randtype == self.last_randtype == self.last2_randtype:
                    if self.sizetype == 0:  # 1 tüüpi on 4 maja
                        self.randtype = randint(0, 3)
                    elif 2 < self.sizetype:  # 4,5 tüüpi on 1 puudu
                        self.randtype = randint(0, 1)
                    else:  # tüüp 2,3
                        self.randtype = randint(0, 2)
        else:
            self.randtype = randtype
        self.image = game.images.houses[self.sizetype][self.randtype]
        self.drawnout = False
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = game.houses_types[self.sizetype][0][0]
        for house in game.houses[self.sizetype]:
            self.x += game.houses_types[house.sizetype][0][1][house.randtype]
        self.y = game.houses_types[self.sizetype][1][self.randtype] + game.resolution[1] - 720
        self.rect = pygame.Rect(self.x, self.y + self.h, self.w, self.h)
        self.arearect = pygame.Rect(0, self.h, self.w, self.h)

    def draw(self, game):
        if self.x < game.resolution[0]:
            if self.drawnout:
                self.surface.blit(self.image, (self.x, self.y))
            else:
                if self.arearect.y > 0:
                    self.arearect.y -= 5
                    self.rect.y -= 5
                    self.surface.blit(self.image, self.rect, self.arearect)
                else:
                    self.drawnout = True
                    self.rect.y = self.y
                    self.surface.blit(self.image, (self.x, self.y))


class Cloud:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.misc[0]
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
        self.x = 0
        self.y = 0
        self.w = 280
        self.h = game.resolution[1]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    @staticmethod
    def process_upgrade_buttons(game):
        for button in game.upgrade_buttons:
            if not button.active:
                game.usedupgrades.append(button.name)
                game.upgrade_buttons.remove(button)
            else:
                button.process_location(game)

    def mouse_hover_check(self, game, x, y):
        if self.rect.collidepoint(x, y):
            for button in game.tax_buttons + game.upgrade_buttons:
                if button.animatecounter > 0:
                    button.animatein = False
                if not button.animateout and not button.animatein:
                    if button.x < button.maxx:
                        button.x += 20
        else:
            for button in game.tax_buttons + game.upgrade_buttons:
                if not button.animateout and not button.animatein:
                    if button.x > button.minx:
                        button.x -= 20


class RightDrawer:
    def __init__(self, game):
        self.surface = game.screen
        self.x = game.resolution[0] - 220
        self.y = 0
        self.w = game.resolution[0] - self.x
        self.h = game.resolution[1]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def mouse_hover_check(self, game, x, y):
        if self.rect.collidepoint(x, y):
            for button in game.right_buttons:
                if not button.animatein:
                    if button.x > button.minx:
                        button.x -= 20
        else:
            for button in game.right_buttons:
                if not button.animatein:
                    if button.x < button.maxx:
                        button.x += 20


class UpgradeButton:
    def __init__(self, game, name, index):
        self.active = True
        self.index = index
        self.surface = game.screen
        self.drawdata = [(255, 255, 255), 14, " €"]
        self.image_available = game.images.upgrade_button[0]
        self.image_unavailable = game.images.upgrade_button[1]
        self.image_highlighted = game.images.upgrade_button[2]
        self.miny = 155 + 75 * index
        self.y = 155 + 75 * index
        self.w = self.image_available.get_rect().w
        self.h = self.image_available.get_rect().h
        self.x = -self.w
        self.minx = 20 - self.w
        self.maxx = 0
        self.animatein = True
        self.animatemove = False
        self.animateout = False
        self.animateminx = -self.w
        self.animatecounter = 150
        self.name = name
        for item in game.upgrades:
            if item[0] == self.name:
                multiplier = game.difficulty
                if multiplier == 0:
                    multiplier = 0.5
                self.cost = int(item[1] * multiplier)
                self.rewardtype = item[2][0]
                self.reward = item[2][1]

    def draw(self, game, is_highlighted):
        if self.animatemove:
            if self.y > self.miny:
                self.y -= 10
            else:
                self.animatemove = False
        elif self.animatein:
            if game.bar.startcounter > 0:
                if self.x < self.minx:
                    self.x += 2
                else:
                    self.animatein = False
            else:
                if self.x < self.maxx:
                    self.x += 10
                elif self.animatecounter > 0:
                    self.animatecounter -= 1
                else:
                    self.animatein = False
        elif self.animateout:
            if self.x > self.animateminx:
                self.x -= 10
            else:
                self.animateout = False
                self.active = False
        if game.bar.money >= self.cost:
            if is_highlighted:
                self.surface.blit(self.image_highlighted, (self.x, self.y))
            else:
                self.surface.blit(self.image_available, (self.x, self.y))
        else:
            percentage = Methods.calculate_percentage(game, self.cost)
            self.surface.blit(self.image_unavailable,
                              pygame.Rect(self.x + self.w / 100 * percentage, self.y, self.w, self.h),
                              pygame.Rect(self.w / 100 * percentage, 0, self.w, self.h))
            self.surface.blit(self.image_available, (self.x, self.y),
                              pygame.Rect(0, 0, self.w / 100 * percentage, self.h))
        Methods.draw_obj(game, True, self.name, (self.x, self.y), (10, 7), (132, 20), self.drawdata, 0)
        Methods.draw_obj(game, True, self.cost, (self.x, self.y), (12, 35), (77, 20), self.drawdata, self.drawdata[2])
        Methods.draw_obj(game, True, self.reward, (self.x, self.y), (97, 35), (48, 20), self.drawdata, 0)

    def process_location(self, game):
        for upgrade in game.upgrade_buttons:
            if upgrade.name == self.name:
                if game.upgrade_buttons.index(upgrade) < self.index:
                    self.index -= 1
                    self.miny = 155 + 75 * self.index
                    self.animatemove = True

    def mouse_click_check(self, game, x, y):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if rect.collidepoint(x, y):
            if game.bar.money >= self.cost:
                game.bar.money -= self.cost
                self.process_rewards(game)
                self.animateout = True
                self.animatecounter = 0

    def mouse_hover_check(self, x, y):
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if rect.collidepoint(x, y):
            return True

    def process_rewards(self, game):
        if self.rewardtype == "special":
            game.bar.special += self.reward
        elif self.rewardtype == "perspecial":
            game.bar.perspecial += self.reward
        elif self.rewardtype == "unlock":
            game.initialize_unlock(game, self.reward)


class TaxButton:
    def __init__(self, game, sizetype):
        self.surface = game.screen
        self.sizetype = sizetype
        self.drawdata = [(255, 255, 255), 14]
        self.image_regular = game.images.left_button[0]
        self.image_minus = game.images.left_button[1]
        self.image_plus = game.images.left_button[2]
        self.y = 15 + 45 * self.sizetype
        self.taxtxt = game.taxes[self.sizetype][0]
        self.w = self.image_regular.get_rect().w
        self.h = self.image_regular.get_rect().h
        self.minx = 155 - self.w
        self.x = -self.w
        self.clickxminus = 206
        self.clickxplus = 234
        self.clicky = self.y + 7
        self.clickw = 25
        self.clickh = 20
        self.maxx = 0
        self.active = True
        self.animatein = True
        self.animateout = False
        self.animatecounter = 0

    def draw(self, game, is_highlighted):
        if self.animatein:
            if self.x < self.minx - 20:
                self.x += 4
            else:
                self.animatein = False
        if is_highlighted == "minus":
            self.surface.blit(self.image_minus, (self.x, self.y))
        elif is_highlighted == "plus":
            self.surface.blit(self.image_plus, (self.x, self.y))
        else:
            self.surface.blit(self.image_regular, (self.x, self.y))
        Methods.draw_obj(game, True, self.taxtxt, (self.x, self.y), (10, 7), (132, 20), self.drawdata, 0)
        Methods.draw_obj(game, True, str(game.taxes[self.sizetype][1]) + "%",
                         (self.x, self.y), (149, 7), (52, 20), self.drawdata, 0)

    def mouse_click_check(self, game, x, y):
        rects = [pygame.Rect(self.x + self.clickxminus, self.clicky, self.clickw, self.clickh),
                 pygame.Rect(self.x + self.clickxplus, self.clicky, self.clickw, self.clickh)]
        for rect in rects:
            if rect.collidepoint(x, y):
                if rects.index(rect) == 1:
                    if game.taxes[self.sizetype][1] < 100:
                        game.taxes[self.sizetype][1] += 5
                else:
                    if game.taxes[self.sizetype][1] > 0:
                        game.taxes[self.sizetype][1] -= 5

    def mouse_hover_check(self, x, y):
        rects = [pygame.Rect(self.x + self.clickxminus, self.clicky, self.clickw, self.clickh),
                 pygame.Rect(self.x + self.clickxplus, self.clicky, self.clickw, self.clickh)]
        for rect in rects:
            if rect.collidepoint(x, y):
                if rects.index(rect) == 0:
                    return "minus"
                elif rects.index(rect) == 1:
                    return "plus"


class RightButton:
    def __init__(self, game, sizetype):
        self.hidden = True
        self.surface = game.screen
        self.sizetype = sizetype
        self.image_available = game.images.right_button[0]
        self.image_available_highlighted = game.images.right_button[1]
        self.image_unavailable = game.images.right_button[2]
        self.drawdata = [(255, 255, 255), 14, " €"]
        self.w = self.image_available.get_rect().w
        self.h = self.image_available.get_rect().h
        self.x = game.resolution[0]
        self.minx = game.resolution[0] - 220
        self.maxx = game.resolution[0] - 20
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
        self.animatein = True
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, game, is_highlighted):
        if not self.hidden:
            if self.animatein:
                if self.x > self.maxx:
                    self.x -= 2
                else:
                    self.animatein = False
            if game.bar.money >= self.price:
                if is_highlighted:
                    self.surface.blit(self.image_available_highlighted, self.rect)
                else:
                    self.surface.blit(self.image_available, self.rect)
            else:
                percentage = Methods.calculate_percentage(game, self.price)
                self.surface.blit(self.image_unavailable,
                                  pygame.Rect(self.x + self.w / 100 * percentage, self.y, self.w, self.h),
                                  pygame.Rect(self.w / 100 * percentage, 0, self.w, self.h))
                self.surface.blit(self.image_available, self.rect, pygame.Rect(0, 0, self.w / 100 * percentage, self.h))
            Methods.draw_obj(game, True, self.logo, (self.x, self.y), (7, 6.653), (47.25, 47.603), self.drawdata, 0)
            Methods.draw_obj(
                game, True, self.amount, (self.x, self.y), (7, 62.178), (47.25, 19.256), self.drawdata, 0)
            Methods.draw_obj(
                game, True, self.name, (self.x, self.y), (62.013, 7.216), (132.25, 19.256), self.drawdata, 0)
            Methods.draw_obj(game, True, self.people, (self.x, self.y), (77, 35), (44, 19.256), self.drawdata, 0)
            Methods.draw_obj(
                game, True, self.peopletotal, (self.x, self.y), (132, 34.394), (63, 19.256), self.drawdata, 0)
            Methods.draw_obj(game, True, round(self.price), (self.x, self.y), (62.013, 62.178), (132.25, 19.256),
                             self.drawdata, self.drawdata[2])
        else:
            if game.bar.people >= game.houses_properties[self.sizetype][2]:
                self.hidden = False

    def calculate_percentage(self, game):
        if game.bar.money == 0:
            return 0
        percentage = game.bar.money / self.price * 100
        return percentage

    def mouse_click_check(self, game, x, y):
        if not self.hidden:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if self.rect.collidepoint(x, y):
                if game.bar.money >= self.price:
                    game.bar.money -= self.price
                    self.amount += 1
                    self.peopletotal += self.people
                    self.price = game.right_button_prices_fixed[
                                     self.sizetype] * game.bar.house_multiplier ** self.amount
                    game.houses[self.sizetype].append(
                        House(game, self.sizetype, None, game.houses_properties[self.sizetype][0]))

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
        self.is_highlighted_button = game.difficulty + 2
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
        Methods.draw_obj(
            game, True, self.name, (self.rect.x, self.rect.y - 3), 0, (self.w, self.h), self.drawdata, 0)

    def mouse_hover_check(self, x, y):
        if self.rect.collidepoint(x, y):
            return True

    def mouse_click_check(self, game, x, y):
        if self.rect.collidepoint(x, y):
            if self.stype == 0:
                game.initialize_game(game, "new")
                game.menu_running = False
            elif self.stype == 1:
                if game.bar_amounts[0] == 0 and game.bar_amounts[0] == 0:
                    pass
                else:
                    game.initialize_game(game, "load")
                    game.menu_running = False
            else:
                game.difficulty = self.stype - 2
                game.menu.is_highlighted_button = self.stype


class Bar:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.bar
        self.time_from_beginning = 0
        self.drawdata = [(255, 255, 255), 14, [" €", " €/s"]]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = (game.resolution[0] - self.w) / 2
        self.y = -self.h
        self.maxy = 6
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.people = game.bar_amounts[0]
        self.money = game.bar_amounts[1]
        self.income = game.bar_amounts[2]
        self.special = game.bar_amounts[3]
        self.perspecial = game.bar_amounts[4]
        self.income_manual = 0
        self.income_manual_time = 0
        self.income_manual_data = []
        self.house_multiplier = 1.15
        self.unlockedupgrades = []
        for name in game.usedupgrades:
            for upgrade in game.upgrades:
                if upgrade[0] == name:
                    game.upgrades.remove(upgrade)
        self.startcounter = 50
        pygame.time.set_timer(pygame.USEREVENT + 1, 100)
        self.objxy = ([19, 204, 469], 7)
        self.objwh = ([170, 249], 21.621)

    def update(self, game):
        self.calculate_money(game)
        self.income_manual_time += game.tick
        self.process_upgrades(game)
        self.calculate_auto_income(game)
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

    def calculate_auto_income(self, game):
        special = self.special * self.perspecial
        income = 0
        tax = 0
        for taxtype in game.taxes:
            tax += taxtype[1]
        for sizetype in game.houses:
            for house in sizetype:
                income += house.people * game.bar.house_multiplier * game.houses_properties[house.sizetype][1]
        taxed_income = (income + special) * (1 + tax / 100)
        self.income = taxed_income

    def calculate_money(self, game):
        self.time_from_beginning += game.tick
        if self.time_from_beginning < 10:  # less than 10ms per frame
            game.bar.money += game.bar.income / 1000 * self.time_from_beginning / 1
        elif self.time_from_beginning < 100:  # less than 100ms per frame
            game.bar.money += game.bar.income / 100 * self.time_from_beginning / 10
        elif self.time_from_beginning < 1000:  # less than 1000ms per frame
            game.bar.money += game.bar.income / 10 * self.time_from_beginning / 100
        self.time_from_beginning = 0

    def process_upgrades(self, game):
        if self.startcounter > 0:
            self.startcounter -= 1
        game.left_drawer.process_upgrade_buttons(game)
        for upgrade in game.upgrades:
            if upgrade[3][0] == "people":
                if self.people >= upgrade[3][1]:
                    game.upgrade_buttons.append(UpgradeButton(game, upgrade[0], len(game.upgrade_buttons)))
                    self.unlockedupgrades.append(upgrade)
            elif upgrade[3][0] == "houses":
                houses = 0
                for sizetype in game.houses:
                    houses += len(sizetype)
                if houses >= upgrade[3][1]:
                    game.upgrade_buttons.append(UpgradeButton(game, upgrade[0], len(game.upgrade_buttons)))
                    self.unlockedupgrades.append(upgrade)
            elif upgrade[3][0] == "income":
                if self.income >= upgrade[3][1]:
                    game.upgrade_buttons.append(UpgradeButton(game, upgrade[0], len(game.upgrade_buttons)))
                    self.unlockedupgrades.append(upgrade)
            if upgrade in self.unlockedupgrades:
                game.upgrades.remove(upgrade)

    def draw(self, game):
        if self.y < self.maxy:
            self.y += 2
        self.surface.blit(self.image, (self.x, self.y))
        Methods.draw_obj(game, True, self.people, (self.x, self.y),
                         (self.objxy[0][0], self.objxy[1]), (self.objwh[0][0], self.objwh[1]), self.drawdata, 0)
        Methods.draw_obj(game, True, round(self.money), (self.x, self.y), (self.objxy[0][1], self.objxy[1]),
                         (self.objwh[0][1], self.objwh[1]), self.drawdata, self.drawdata[2][0])
        Methods.draw_obj(game, True, round(self.income + self.income_manual),
                         (self.x, self.y), (self.objxy[0][2], self.objxy[1]), (self.objwh[0][0], self.objwh[1]),
                         self.drawdata, self.drawdata[2][1])
