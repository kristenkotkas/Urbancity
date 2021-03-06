# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
import pygame
import os.path
import shelve
from random import randint, sample, shuffle

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game(object):
    def __init__(self):
        pygame.mixer.pre_init(48000, -16, 2, 2048)
        pygame.init()
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        self.fps_cap = 120
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.running = True
        self.tutorial_mode = True
        self.difficulty = 1
        self.activeclouds = self.houses = self.houses_states = self.upgrades = self.money_bonuses = self.taxes = \
            self.notifications = self.unused_upgrades = []
        self.images = self.sounds = self.background = self.cursor = self.cloud = self.metro = self.pipe = self.fiber = \
            self.power = self.watersupply = self.bar = self.right_drawer = self.left_drawer = self.quick_menu = \
            self.tick = self.menu = self.houses_properties = self.right_button_prices_fixed = self.fonts = \
            self.tutorial = self.used_upgrades = self.bar_amounts = self.houses_properties = self.used_bonuses = \
            self.houses_types = self.right_button_prices = self.right_button_prices_fixed = self.used_notifications = \
            self.right_button_amounts = self.wifi_tower = self.fiveg_tower = self.lifi_tower = None
        self.allsprites = pygame.sprite.LayeredDirty()
        self.allsprites.set_timing_treshold(10000)
        self.interactables_visible = True

    def init_loadconfig(self, difficulty):
        self.taxes = [0, 0, 0]
        self.used_upgrades = set()
        self.unused_upgrades = []
        self.used_bonuses = []
        self.used_notifications = []
        # upgrades = (name{public}, type{private}, cost amount{public},
        #            unlock amount{private}, income reward amount{public})
        self.upgrades = [(u"Electricity", 1, 84000, 2400, 84),
                         (u"Water Supply", 1, 121500, 2400, 140),
                         (u"Plumbing", 1, 178000, 2400, 160),
                         (u"Wi-Fi", 1, 411000, 12000, 480),
                         (u"Metro", 1, 2095000, 50000, 2440),
                         (u"Santa Claus", 1, 3672500, 50000, 4280),
                         (u"Moogle Fiber", 1, 5128000, 50000, 5980),
                         (u"Wireless electricity", 1, 10890000, 100000, 12700),
                         (u"5G", 1, 17786500, 100000, 20720),
                         (u"Li-Fi", 1, 50120000, 225000, 57750),
                         (u"World Peace", 1, 500000000, 750000, 583333)]
        # money_bonus = (name{private}, reward{public}, unlock amount{private})
        self.money_bonuses = [(0, 20000, 1000),
                              (1, 75000, 2400),
                              (2, 175000, 10000),
                              (3, 325000, 12000),
                              (4, 2500000, 25000),
                              (5, 5000000, 42000),
                              (6, 12000000, 50000),
                              (7, 24000000, 75000),
                              (8, 48000000, 100000),
                              (9, 84000000, 150000),
                              (10, 140000000, 225000),
                              (11, 176000000, 250000),
                              (12, 360000000, 400000),
                              (13, 495000000, 500000),
                              (14, 810000000, 750000),
                              (15, 1000000000, 1000000)]
        self.bar_amounts = [0, 0]
        self.houses = [[], [], [], [], []]
        self.houses_states = [[], [], [], [], []]
        self.houses_properties = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        # houses_types = sizetype(randtype[x base, randtype[x width + gap]], randtype[y from bottom])
        self.houses_types = [([-15, [190, 125, 240, 125]], [432, 347, 427, 347]),
                             ([5, [90, 96, 242]], [340, 335, 328]),
                             ([-30, [103, 96, 170]], [255, 255, 250]),
                             ([-10, [128, 180, 223]], [115, 130, 130]),
                             ([-40, [170, 135, 150]], [73, 59, 41])]
        self.right_button_prices_fixed = [0, 0, 0, 0, 0]
        self.right_button_prices = [0, 0, 0, 0, 0]
        self.right_button_amounts = [0, 0, 0, 0, 0]
        # houses_properties = sizetype(maxpeople in type, per people modifier, minpeople for type unlock)
        if difficulty == 0:
            self.houses_properties = [
                (200, 0.2, 0), (900, 0.4, 600), (2560, 1, 3500), (7200, 1.8, 10800), (13500, 6, 27000)]
            self.right_button_prices_fixed = [750, 9000, 40000, 486000, 2531250]
        elif difficulty == 1:
            self.houses_properties = [
                (100, 0.1, 0), (450, 0.2, 700), (1280, 0.5, 4000), (3600, 0.9, 18000), (6750, 3, 40000)]
            self.right_button_prices_fixed = [1500, 18000, 80000, 972000, 5062500]
        elif difficulty == 2:
            self.houses_properties = [
                (50, 0.1, 0), (220, 0.2, 1000), (640, 0.3, 6000), (1800, 0.5, 24000), (3300, 1.5, 54000)]
            self.right_button_prices_fixed = [3000, 36000, 160000, 1944000, 10125000]
        # notifications = (index{private}, name{public}, unlock{private}, city name{public})
        self.notifications = [
            (0, u"First people are moving in.", 10, u"Village"),
            (1, u"Bigger houses means more people. Low-end unlocked.", self.houses_properties[1][2], 0),
            (2, u"Let’s make it even bigger. High-end unlocked.", self.houses_properties[2][2], 0),
            (3, u"You are one step closer to Urbancity. Status update: Town.", 2400, u"Town"),
            (4, u"Your city is growing. Luxury unlocked.", self.houses_properties[3][2], 0),
            (5, u"You are one step closer to Urbancity. Status update: City.", 12000, u"City"),
            (6, u"Finally a skyscraper, let the world domination begin. Skyscrapers unlocked.",
             self.houses_properties[4][2], 0),
            (7, u"You are one step closer to Urbancity. Status update: Urban area.", 42000, u"Urban area"),
            (8, u"You are one step closer to Urbancity. Status update: Metropolis.", 100000, u"Metropolis"),
            (9, u"Only few steps to Urbancity. Status update: Megacity.", 225000, u"Megacity"),
            (10, u"Only one step left to Urbancity. Status update: Megapolis.", 400000, u"Megapolis"),
            (11, u"You have reached to the top. Status update: Urbancity.", 750000, u"Urbancity"),
            (12, u"With great power comes great responsibility.", self.upgrades[0], 0),
            (13, u"How did we manage to live without water before?", self.upgrades[1], 0),
            (14, u"Does anybody know a good plumber? Cause I really need one from now on?", self.upgrades[2], 0),
            (15, u"Faster Internet means happier people.", self.upgrades[3], 0),
            (16, u"Metro transports people faster through city.", self.upgrades[4], 0),
            (17, u"Santa is real! I told you Santa was real!", self.upgrades[5], 0),
            (18, u"Now we can finally get rid of the dial-up. Thanks Moogle.", self.upgrades[6], 0),
            (19, u"What’s better than wireless Internet? Wireless electricity of course.", self.upgrades[7], 0),
            (20, u"Looks like we are the first city to use 5G technology.", self.upgrades[8], 0),
            (21, u"Now you can surf at the speed of light.", self.upgrades[9], 0),
            (22, u"You have conquered the terrorists. Now, try to build your city as big as possible.",
             self.upgrades[10], 0),
            (23, u"Your people have found a pot of gold worth " + unicode(format(self.money_bonuses[0][1], u",d")) +
             u" €.", 1000, 0),
            (24, u"Your colonies overseas have generated " + unicode(format(self.money_bonuses[2][1], u",d")) +
             u" € profit.", 10000, 0),
            (25, u"The " + self.generate_name() + u" association awards you with a " +
             unicode(format(self.money_bonuses[4][1], u",d")) + u" € bonus.", 25000, 0),
            (26, u"The United States of " + self.generate_name() + u" have donated you " +
             unicode(format(self.money_bonuses[7][1], u",d")) + u" €.", 75000, 0),
            (27, u"The people from the planet of " + self.generate_name() + u" have sent you " +
             unicode(format(self.money_bonuses[9][1], u",d")) + u" €.", 150000, 0),
            (28, u"The " + self.generate_name() + u" company has donated you " +
             unicode(format(self.money_bonuses[11][1], u",d")) + u" €.", 250000, 0),
            (29, u"The Kingdom of " + self.generate_name() + u" have donated you " +
             unicode(format(self.money_bonuses[13][1], u",d")) + u" €.", 500000, 0),
            (30, u"The " + self.generate_name() + u" Union have donated you " +
             unicode(format(self.money_bonuses[15][1], u",d")) + u" €.", 1000000, 0)]

    def initialize(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 10)
        pygame.time.set_timer(pygame.USEREVENT + 2, 100)
        pygame.time.set_timer(pygame.USEREVENT + 3, 500)
        pygame.time.set_timer(pygame.USEREVENT + 4, 10000)
        self.images = Images()
        self.fonts = Fonts()
        self.sounds = Sounds()
        self.background = Background()
        self.cursor = Cursor()
        self.quick_menu = QuickMenu()
        self.menu = Menu()
        self.init_load(u"load_state")

    def init_new(self):
        self.init_load(u"new_state")
        game.toggle_interactables()
        if self.tutorial_mode:
            game.tutorial.toggle()

    def init_load(self, state):
        self.init_purge()
        self.init_loadconfig(self.difficulty)
        self.filesystem_do(state, self.difficulty)
        self.cloud = Cloud(10)
        self.left_drawer = LeftDrawer(self.used_upgrades)
        self.right_drawer = RightDrawer()
        for upgrade in self.left_drawer.used_upgrades:
            game.left_drawer.init_unlock(upgrade)
        self.bar = Bar(self.used_bonuses, self.used_notifications)
        for sizetype in xrange(3):
            self.left_drawer.tax_buttons.append(TaxButton(sizetype))
        for sizetype in xrange(5):
            self.right_drawer.right_buttons.append(RightButton(sizetype))
        game.toggle_interactables()
        self.tutorial = Tutorial()
        self.set_loaded_states()

    def init_purge(self):
        if self.bar is not None:
            game.toggle_interactables()
        for i in xrange(20):
            sprites = self.allsprites.remove_sprites_of_layer(i)
            for sprite in sprites:
                sprite.kill()
        self.activeclouds = self.houses = self.houses_states = self.upgrades = self.money_bonuses = self.taxes = \
            self.notifications = self.unused_upgrades = []
        self.cloud = self.metro = self.pipe = self.fiber = self.power = self.watersupply = self.bar = \
            self.right_drawer = self.left_drawer = self.houses_properties = self.right_button_prices_fixed = \
            self.tutorial = self.used_upgrades = self.bar_amounts = self.houses_properties = self.used_bonuses = \
            self.houses_types = self.right_button_prices = self.right_button_prices_fixed = self.used_notifications = \
            self.right_button_amounts = self.wifi_tower = self.fiveg_tower = self.lifi_tower = None

    def run(self):
        self.initialize()
        while self.running:
            self.tick = self.clock.tick(self.fps_cap)
            self.process_events()
            self.allsprites.update()
            dirtyrects = self.allsprites.draw(self.screen)
            pygame.display.update(dirtyrects)
            # pygame.display.set_caption(
            #     u"FPS: " + unicode(round(self.clock.get_fps(), 2)) + u", Redrawing: " + unicode(len(dirtyrects)))
        self.filesystem_do(u"save_state", self.difficulty)
        pygame.time.wait(50)
        pygame.quit()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                # 10ms timer
                game.bar.process_income()
                game.right_drawer.process_tap_pad()
                for sizetype in game.houses:
                    for house in sizetype:
                        house.calculate_currentpeople()
            elif event.type == pygame.USEREVENT + 2:
                # 100ms timer
                game.bar.calculate_manual_income()
                game.bar.process_money_bonuses()
                game.bar.process_notifications()
                game.left_drawer.news_obj.count()
                if game.metro is not None:
                    game.metro.train_obj.count()
            elif event.type == pygame.USEREVENT + 3:
                # 500ms timer
                for sizetype in game.houses:
                    for house in sizetype:
                        house.calculate_min_people()
            elif event.type == pygame.USEREVENT + 4:
                # 10s timer
                for sizetype in self.houses:
                    for house in sizetype:
                        house.calculate_taxmax()
            elif event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game.tutorial is not None and game.tutorial.visible:
                        game.tutorial.toggle()
                    elif not game.menu.visible:
                        self.quick_menu.toggle()
                elif event.key == pygame.K_SPACE:
                    game.bar.add_manual_money()
                elif event.key == pygame.K_LEFT:
                    game.tutorial.guide_obj.switch_tutorial(-1)
                elif event.key == pygame.K_RIGHT:
                    game.tutorial.guide_obj.switch_tutorial(1)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.right_drawer.tap_pad_click_check()
                if game.quick_menu.mouse_click_check() or game.quick_menu.sounds_obj.mouse_click_check() or \
                        game.tutorial.mouse_click_check() or game.bar.mouse_click_check():
                    self.sounds.play(u"click")
                for button in game.right_drawer.right_buttons + game.left_drawer.tax_buttons + \
                        game.left_drawer.upgrade_buttons + game.menu.buttons:
                    if button.mouse_click_check():
                        self.sounds.play(u"click")
                        break

    def toggle_interactables(self):
        if self.interactables_visible:
            self.interactables_visible = False
        else:
            self.interactables_visible = True
        self.left_drawer.toggle()
        self.bar.toggle()
        self.right_drawer.toggle()
        if self.right_drawer.tap_pad_global_visible:
            self.right_drawer.tap_pad_toggle()

    def add_new_renderable(self, obj, layer):
        self.allsprites.add(obj, layer = layer)

    @staticmethod
    def toggle_tutorial_layer(obj, mylayer, mylayermod, tutscreen):
        if game.tutorial.visible and game.tutorial.guide_obj.tutscreen == tutscreen:
            layer = game.tutorial.layer + 1
            game.allsprites.remove(obj)
            game.add_new_renderable(obj, layer)
            return layer + 1
        else:
            if game.allsprites.get_layer_of_sprite(obj) == game.tutorial.layer + 1:
                game.allsprites.remove(obj)
                game.add_new_renderable(obj, mylayer)
                return mylayer + 1
            else:
                return mylayermod

    def filesystem_do(self, action, savetype):
        filename = os.path.join(main_dir, u'data', u"save_game" + unicode(savetype))
        if action == u"load_state":
            d = shelve.open(filename)
            keylist = d.keys()
            if len(keylist) != 0:
                self.difficulty = d["difficulty"]
                self.houses_states = d["houses_states"]
                self.right_button_amounts = d["right_button_amounts"]
                self.right_button_prices = d["right_button_prices"]
                self.bar_amounts = [d["money"], d["incomereward"]]
                self.used_upgrades = d["usedupgrades"]
                self.unused_upgrades = d["unusedupgrades"]
                self.used_bonuses = d["usedbonuses"]
                self.used_notifications = d["usednotifications"]
                self.taxes = d["taxes"]
            d.close()
        elif action == u"save_state":
            self.get_current_states()
            d = shelve.open(filename)
            d["houses_states"] = self.houses_states
            d["right_button_amounts"] = self.right_button_amounts
            d["right_button_prices"] = self.right_button_prices
            d["money"] = self.bar.money
            d["incomereward"] = self.bar.incomereward
            d["difficulty"] = self.difficulty
            d["usedupgrades"] = game.left_drawer.used_upgrades
            d["unusedupgrades"] = game.unused_upgrades
            d["usedbonuses"] = game.bar.used_bonuses
            d["usednotifications"] = game.bar.used_notifications
            d["taxes"] = self.taxes
            d.close()
        elif action == u"new_state":
            pass

    def get_current_states(self):
        for upgrade_button in self.left_drawer.upgrade_buttons:
            self.unused_upgrades.append(upgrade_button.upgrade)
        for button in xrange(len(game.right_drawer.right_buttons)):
            self.right_button_amounts[button] = game.right_drawer.right_buttons[button].amount
            self.right_button_prices[button] = game.right_drawer.right_buttons[button].price
        self.houses_states = [[], [], [], [], []]
        for sizetype in self.houses:
            for house in sizetype:
                self.houses_states[house.sizetype].append([house.sizetype, house.randtype, house.peoplecurrent])

    def set_loaded_states(self):
        for sizetype in self.houses_states:
            for house in sizetype:
                game.houses[house[0]].append(House(house[0], house[1], house[2]))

    @staticmethod
    def generate_name():
        letters = u"aeioubdgkpthlmnrsv"

        def forbidden(x, y):
            forbidden_set = {(letters[5:11], u"xvml"), (u"x", letters[5:11] + u"xhsm"), (u"hpsdlxkrvs", u"r"),
                             (letters[5:], letters[5:11]), (u"lhmvsrk", u"x"), (u"e", u"au"), (u"dms", u"h"),
                             (u"uia", u"o"), (u"m", u"lnv"), (u"kptgbdhnvlr", u"hnm")}
            for element in forbidden_set:
                if x in element[0] and y in element[1]:
                    return True

        name = u""
        name += letters[randint(0, 17)]
        if name[-1] in letters[5:]:
            name += letters[randint(0, 4)]
        else:
            name += letters[5:][randint(0, 12)]
        while len(name) != 7:
            letter = letters[randint(0, 17)]
            if name[-1] == name[-2] == letter:
                letter = u""
            if name[-1] in letters[5:] and name[-2] in letters[5:] and letter in letters[5:]:
                letter = u""
            if name[-1] in letters[0:5] and name[-2] in letters[0:5]:
                if name[-1] == name[-2]:
                    letter = u""
                if letter in letters[0:5]:
                    letter = letters[randint(5, 17)]
            if forbidden(name[-1], letter):
                letter = u""
            name += letter
        if not name[-1] in letters[0:4]:
            name += letters[randint(0, 4)]
        return name.title()


class Images(object):
    def __init__(self):
        self.background = self.load_image(u"Background.png")
        self.cursor = self.load_image(u"Cursor.png")
        self.right_button = [self.load_image(u"Button_available.png"), self.load_image(u"Button_available_hover.png"),
                             self.load_image(u"Button_unavailable.png")]
        self.right_button_logos = [self.load_image(u"House_1_logo.png"), self.load_image(u"House_2_logo.png"),
                                   self.load_image(u"House_3_logo.png"), self.load_image(u"House_4_logo.png"),
                                   self.load_image(u"House_5_logo.png")]
        self.right_drawer = [self.load_image(u"Tap_pad.png")]
        self.left_button = [self.load_image(u"Tax.png"), self.load_image(u"Tax_hover_minus.png"),
                            self.load_image(u"Tax_hover_plus.png")]
        self.upgrade_button = [self.load_image(u"Upgrade_available.png"), self.load_image(u"Upgrade_unavailable.png"),
                               self.load_image(u"Upgrade_available_hover.png"), self.load_image(u"Law_available.png"),
                               self.load_image(u"Law_unavailable.png"), self.load_image(u"Law_available_hover.png")]
        self.bar = [self.load_image(u"Bar.png"), self.load_image(u"Bar_hover.png")]
        self.misc = [self.load_image(u"Cloud.png"), self.load_image(u"Breaking_news.png"),
                     self.load_image(u"Pipe.png"), self.load_image(u"Google_Fiber.png"),
                     self.load_image(u"Electricity.png"), self.load_image(u"Water.png"),
                     self.load_image(u"Wifi_tower.png"), self.load_image(u"5G_tower.png"),
                     self.load_image(u"Lifi_tower.png")]
        self.houses = [
            [self.load_image(u"House_11.png"), self.load_image(u"House_12.png"), self.load_image(u"House_13.png"),
             self.load_image(u"House_14.png")],
            [self.load_image(u"House_21.png"), self.load_image(u"House_22.png"), self.load_image(u"House_23.png")],
            [self.load_image(u"House_31.png"), self.load_image(u"House_32.png"), self.load_image(u"House_33.png")],
            [self.load_image(u"House_41.png"), self.load_image(u"House_42.png"), self.load_image(u"House_43.png")],
            [self.load_image(u"House_51.png"), self.load_image(u"House_52.png"), self.load_image(u"House_53.png")]]
        self.metro = [self.load_image(u"Metro.png"), self.load_image(u"Metro_train.png"),
                      self.load_image(u"Metro_terror.png")]
        self.menu = [[self.load_image(u"Urbancity_logo.png")],
                     [self.load_image(u"Menu_big_button.png"), self.load_image(u"Menu_big_button_hover.png"),
                      self.load_image(u"Menu_small_button.png"), self.load_image(u"Menu_small_button_hover.png")]]
        self.quick_menu = [self.load_image(u"Quick_menu.png"), self.load_image(u"Quick_menu_highlighted.png"),
                           self.load_image(u"Quick_menu_sounds.png"), self.load_image(u"Quick_menu_sounds_hover.png"),
                           self.load_image(u"Quick_menu_sounds_check.png")]
        self.tutorial = [self.load_image(u"Tutorial_space.png"), self.load_image(u"Tutorial_bar.png"),
                         self.load_image(u"Tutorial_right_button.png"), self.load_image(u"Tutorial_tax.png"),
                         self.load_image(u"Tutorial_upgrade.png"), self.load_image(u"Tutorial_buttons.png"),
                         self.load_image(u"Tutorial_buttons_hover.png")]

    @staticmethod
    def load_image(filename):
        filename = os.path.join(main_dir, u'data', filename)
        try:
            loaded_image = pygame.image.load(filename).convert_alpha()
        except:
            raise SystemExit(u"Could not load image " + filename + u", " + pygame.get_error())
        return loaded_image, loaded_image.get_rect()


class Fonts(object):
    @staticmethod
    def load_font(filename, size):
        filename = os.path.join(main_dir, u'data', filename)
        try:
            loaded_font = pygame.font.Font(filename, size)
        except:
            raise SystemExit(u"Could not load font " + filename + u", " + pygame.get_error())
        return loaded_font


class Sounds(object):
    def __init__(self):
        self.click = self.load_sound(u"Mouse.ogg")
        self.notification = self.load_sound(u"Notification.ogg")
        self.space = [self.load_sound(u"space_1.ogg"), self.load_sound(u"space_2.ogg"),
                      self.load_sound(u"space_3.ogg"), self.load_sound(u"space_4.ogg"),
                      self.load_sound(u"space_5.ogg"), self.load_sound(u"space_6.ogg"),
                      self.load_sound(u"space_8.ogg"), self.load_sound(u"space_9.ogg"),
                      self.load_sound(u"space_10.ogg"), self.load_sound(u"space_11.ogg")]

    def play(self, sound):
        if sound == u"space" and game.quick_menu.sounds_obj.checked_objs_visible[0]:
            self.space[randint(1, 9)].play()
        elif sound == u"click" and game.quick_menu.sounds_obj.checked_objs_visible[1]:
            self.click.play()
        elif sound == u"notification" and game.quick_menu.sounds_obj.checked_objs_visible[2]:
            self.notification.play()

    @staticmethod
    def load_sound(filename):
        filename = os.path.join(main_dir, u'data\\sounds', filename)
        try:
            loaded_sound = pygame.mixer.Sound(filename)
            loaded_sound.set_volume(0.5)
        except pygame.error:
            raise SystemExit(u"Could not load sound " + filename + u", " + pygame.get_error())
        return loaded_sound


class Background(object):
    def __init__(self):
        # noinspection PyArgumentList
        self.surface = pygame.Surface(game.resolution).convert()
        self.image, self.rect = game.images.background
        self.skyarearect = pygame.Rect(0, 0, game.resolution[0], game.resolution[1] - self.rect.h)
        self.surface.fill((125, 196, 255), self.skyarearect)
        self.timesx = game.resolution[0] // self.rect.w + 1
        for column in xrange(int(self.timesx)):
            rect = pygame.Rect(self.rect.w * column, game.resolution[1] - self.rect.h, self.rect.w, self.rect.h)
            arearect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            if column == self.timesx - 1:
                arearect.w = game.resolution[0] - self.rect.w * column
            self.surface.blit(self.image, rect, arearect)
        game.screen.blit(self.surface, (0, 0))
        pygame.display.flip()
        game.allsprites.clear(game.screen, self.surface)


class Cursor(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = 30
        self.image, self.rect = game.images.cursor
        game.add_new_renderable(self, self.layer)

    def update(self):
        pos = pygame.mouse.get_pos()
        if self.rect.topleft != pos:
            self.rect.topleft = pos
            self.dirty = 1


class Metro(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 5
        self.image, rect = game.images.metro[0]
        self.fixedy = game.resolution[1] - rect.h
        self.rect = pygame.Rect((game.resolution[0] - rect.w) / 2, game.resolution[1], rect.w, rect.h)
        self.source_rect = pygame.Rect(0, rect.h, rect.w, rect.h)
        self.drawnout = False
        self.train_obj = MetroTrain(self.layer + 1, self.rect.topleft)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.y > 0:
                self.source_rect.y -= 5
                self.rect.y -= 5
            else:
                self.source_rect.y = 0
                self.rect.y = self.fixedy
                self.dirty = 1
                self.drawnout = True


class MetroTrain(pygame.sprite.DirtySprite):
    def __init__(self, layer, xy):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = layer
        self.xy = xy
        self.trainimage, rect = game.images.metro[1]
        self.terrorimage = game.images.metro[2][0]
        self.image = self.trainimage
        self.rect = pygame.Rect(xy[0], xy[1] - rect.h, rect.w, rect.h)
        self.source_rect = pygame.Rect(rect.w, 0, rect.w, rect.h)
        self.speed = 3
        self.trainstop = xy[0] + 24
        self.waiting = 0
        self.counter = 0
        self.t_override = False
        self.t_event = False
        self.t_notification = u"You have reached to the top. Status update: Urbancity."
        self.t_counter = 0
        game.add_new_renderable(self, self.layer)

    def count(self):
        if self.waiting > 0:
            self.counter -= 1
            if self.counter < 0:
                self.counter = 0
                if self.waiting == 1:
                    self.rect.x += self.speed
                if self.waiting == 2:
                    if self.t_event:
                        self.t_counter -= 1
                        if self.t_counter < 0:
                            self.t_counter = 0
                            self.speed = 3
                            self.image = self.trainimage
                            self.t_event = False
                            if u"World Peace" in game.left_drawer.used_upgrades:
                                self.t_override = True
                    elif not self.t_override and not self.t_event and randint(1, 10) == 6:
                        for notification in game.bar.used_notifications:
                            if notification[1] == self.t_notification:
                                self.t_event = True
                                self.speed = 8
                                self.t_counter = randint(6, 20)
                                game.left_drawer.news_obj.present(2)
                                self.image = self.terrorimage
                self.waiting = 0

    def update(self):
        if game.metro.drawnout:
            if self.waiting == 0:
                if not self.t_event and self.rect.x == self.trainstop:
                    if randint(1, 10) < 5:
                        self.counter = randint(20, 40)
                        self.waiting = 1
                    else:
                        self.rect.x += self.speed
                elif self.rect.right < game.metro.rect.right:
                    if self.source_rect.x > 0:
                        self.source_rect.x -= self.speed
                    else:
                        self.rect.x += self.speed
                elif self.source_rect.x > -self.source_rect.w:
                    if self.rect.right != game.metro.rect.right:
                        self.rect.right = game.metro.rect.right
                    self.source_rect.x -= self.speed
                else:
                    self.source_rect.x = self.source_rect.w
                    self.rect.x = self.xy[0]
                    self.waiting = 2
                    if not self.t_event:
                        self.counter = randint(40, 80)
                    else:
                        self.counter = randint(4, 16)


class LifiTower(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 3
        self.drawnout = False
        self.image, rect = game.images.misc[8]
        self.fixedy = game.resolution[1] - rect.h - game.background.rect.h + 13
        self.rect = pygame.Rect((game.resolution[0] - rect.w) / 2, self.fixedy + rect.h, rect.w, rect.h)
        self.source_rect = pygame.Rect(0, rect.h, rect.w, rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.y > 0:
                self.source_rect.y -= 5
                self.rect.y -= 5
            else:
                self.drawnout = True
                self.source_rect.y = 0
                self.rect.y = self.fixedy
                self.dirty = 1


class FiveGTower(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 5
        self.drawnout = False
        self.image, rect = game.images.misc[7]
        self.fixedy = game.resolution[1] - rect.h - game.background.rect.h + 10
        self.rect = pygame.Rect((game.resolution[0] - rect.w) / 4, self.fixedy + rect.h, rect.w, rect.h)
        self.source_rect = pygame.Rect(0, rect.h, rect.w, rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.y > 0:
                self.source_rect.y -= 5
                self.rect.y -= 5
            else:
                self.drawnout = True
                self.source_rect.y = 0
                self.rect.y = self.fixedy
                self.dirty = 1


class WifiTower(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 7
        self.drawnout = False
        self.image, rect = game.images.misc[6]
        self.fixedy = game.resolution[1] - rect.h - game.background.rect.h + 12
        self.rect = pygame.Rect((game.resolution[0] - rect.w) / 4 * 3, self.fixedy + rect.h, rect.w, rect.h)
        self.source_rect = pygame.Rect(0, rect.h, rect.w, rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.y > 0:
                self.source_rect.y -= 5
                self.rect.y -= 5
            else:
                self.drawnout = True
                self.source_rect.y = 0
                self.rect.y = self.fixedy
                self.dirty = 1


class Pipe(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 4
        self.drawnout = False
        self.surface, rect = game.images.misc[2]
        self.fixedy = game.resolution[1] - rect.h + 30
        self.rect = pygame.Rect(0, self.fixedy + rect.h, rect.w, rect.h)
        # noinspection PyArgumentList
        self.image = pygame.Surface((game.resolution[0], self.rect.h), pygame.SRCALPHA).convert_alpha()
        rect = pygame.Rect(-10, 0, self.rect.w, self.rect.h)
        self.image.blit(self.surface, rect)
        rect = pygame.Rect(game.resolution[0] - self.rect.w + 10, 0, self.rect.w, self.rect.h)
        self.image.blit(pygame.transform.flip(self.surface, True, False), rect)
        self.rect.w = game.resolution[0]
        self.source_rect = pygame.Rect(0, self.rect.h, self.rect.w, self.rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.y > 0:
                self.source_rect.y -= 5
                self.rect.y -= 5
            else:
                self.drawnout = True
                self.source_rect.y = 0
                self.rect.y = self.fixedy
                self.dirty = 1


class Fiber(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 2
        self.drawnout = False
        self.surface, rect = game.images.misc[3]
        self.rect = pygame.Rect(0, game.resolution[1] - rect.h - 90, rect.w, rect.h)
        self.timesx = game.resolution[0] // self.rect.w + 1
        # noinspection PyArgumentList
        self.image = pygame.Surface((game.resolution[0], self.rect.h), pygame.SRCALPHA).convert_alpha()
        for column in xrange(int(self.timesx)):
            rect = pygame.Rect(self.rect.w * column, 0, self.rect.w, self.rect.h)
            arearect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            if column == self.timesx - 1:
                arearect.w = game.resolution[0] - self.rect.w * column
            self.image.blit(self.surface, rect, arearect)
        self.rect.w = game.resolution[0]
        self.source_rect = pygame.Rect(0, 0, 0, self.rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.w < self.rect.w:
                self.source_rect.w += 5
            else:
                self.drawnout = True
                self.source_rect.w = self.rect.w
                self.dirty = 1


class Watersupply(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 3
        self.drawnout = False
        self.surface, rect = game.images.misc[5]
        self.shift = 6
        self.fixedy = game.resolution[1] - rect.h + 5
        self.rect = pygame.Rect(0, self.fixedy + rect.h, rect.w, rect.h)
        self.timesx = game.resolution[0] // self.rect.w + 1
        # noinspection PyArgumentList
        self.image = pygame.Surface((game.resolution[0], self.rect.h), pygame.SRCALPHA).convert_alpha()
        for column in xrange(int(self.timesx)):
            rect = pygame.Rect(self.rect.w * column - self.shift * (column + 1), 0, self.rect.w, self.rect.h)
            arearect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            if column == self.timesx - 1:
                arearect.w = game.resolution[0] - self.rect.w * column + self.shift * self.timesx
            self.image.blit(self.surface, rect, arearect)
        self.rect.w = game.resolution[0]
        self.source_rect = pygame.Rect(0, self.rect.h, self.rect.w, self.rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.y > 0:
                self.source_rect.y -= 5
                self.rect.y -= 5
            else:
                self.drawnout = True
                self.source_rect.y = 0
                self.rect.y = self.fixedy
                self.dirty = 1


class Power(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 9
        self.drawnout = False
        self.surface, rect = game.images.misc[4]
        self.fixedy = game.resolution[1] - rect.h - game.background.rect.h + 10
        self.rect = pygame.Rect(0, self.fixedy + rect.h, rect.w, rect.h)
        self.offset = 20
        self.timesx = round(game.resolution[0] / (self.rect.w - self.offset)) + 1
        # noinspection PyArgumentList
        self.image = pygame.Surface((game.resolution[0], self.rect.h), pygame.SRCALPHA).convert_alpha()
        for column in xrange(int(self.timesx)):
            rect = pygame.Rect(self.rect.w * column - self.offset * (column + 2), 0, self.rect.w, self.rect.h)
            arearect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            if column == self.timesx - 1:
                arearect.w = game.resolution[0] - self.rect.w * column
            self.image.blit(self.surface, rect, arearect)
        self.rect.w = game.resolution[0]
        self.source_rect = pygame.Rect(0, self.rect.h, self.rect.w, self.rect.h)

    def shuffle_layer(self):
        if len(game.allsprites.get_sprites_from_layer(self.layer)) > 0:
            spriteslist = game.allsprites.remove_sprites_of_layer(self.layer)
            shuffle(spriteslist)
            spriteslist.insert(0, self)
            for sprite in spriteslist:
                game.add_new_renderable(sprite, sprite.layer)
        else:
            game.add_new_renderable(self, self.layer)

    def update(self):
        if not self.drawnout:
            if self.source_rect.y > 0:
                self.source_rect.y -= 5
                self.rect.y -= 5
            else:
                self.drawnout = True
                self.source_rect.y = 0
                self.rect.y = self.fixedy
                self.dirty = 1


class Cloud(pygame.sprite.DirtySprite):
    def __init__(self, cloudtype):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = randint(0, 1)
        self.cloudtype = cloudtype
        self.image, rect = game.images.misc[0]
        self.x = self.minx = -rect.w ** 1.15 * self.cloudtype
        self.maxx = game.resolution[0]
        self.speed = randint(1, 2) ** 1.15
        self.rect = pygame.Rect(self.x, game.resolution[1] - 700 + randint(1, 80), rect.w, rect.h)
        game.activeclouds.append(self)
        if self.cloudtype > 1:
            Cloud(cloudtype - 1)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if self.rect.x < self.maxx:
            self.rect.x += self.speed
        else:
            if self in game.activeclouds:
                game.activeclouds.remove(self)
                if len(game.activeclouds) == 0:
                    self.randomize_layers([0, 1])
        if self.rect.left < game.resolution[0] and self.rect.right > 0:
            self.dirty = 1

    @staticmethod
    def randomize_layers(value):
        if isinstance(value, int):
            layer = randint(0, 1)
            if len(game.houses[value]) > 1:
                if layer == game.houses[value][-1].layer == game.houses[value][-2].layer:
                    layer = randint(0, 1)
            return layer
        elif isinstance(value, list):
            spriteslist = game.allsprites.remove_sprites_of_layer(value[0])
            spriteslist.extend(game.allsprites.remove_sprites_of_layer(value[1]))
            for sprite in sample(spriteslist, len(spriteslist)):
                if isinstance(sprite, Cloud):
                    sprite.rect.x = sprite.minx
                    sprite.speed = randint(1, 2) ** 1.15
                    game.activeclouds.append(sprite)
                game.add_new_renderable(sprite, sample(value, len(value))[0])


class House(pygame.sprite.DirtySprite):
    def __init__(self, sizetype, randtype, people):
        pygame.sprite.DirtySprite.__init__(self)
        self.sizetype = sizetype
        if self.sizetype == 0:
            self.layer = randint(8, 9)
            if len(game.houses[sizetype]) > 1:
                if self.layer == game.houses[sizetype][-1].layer == game.houses[sizetype][-2].layer:
                    self.layer = randint(8, 9)
        elif self.sizetype == 1:
            self.layer = 6
        elif self.sizetype == 2:
            self.layer = 4
        elif self.sizetype == 3:
            self.layer = 2
        elif self.sizetype == 4:
            self.layer = game.cloud.randomize_layers(sizetype)
        self.dirty = 2
        self.visible = True
        self.drawnout = False
        self.peoplecurrent = people
        self.peoplemax = game.houses_properties[sizetype][0]
        self.min_people = people / 100 * randint(1, 4)
        game.bar.people_total += self.peoplemax
        game.bar.houses_income += self.peoplemax * game.bar.house_multiplier * game.houses_properties[sizetype][1]
        game.left_drawer.increase_max_buttons()
        self.taxes = []
        self.calculate_taxmax()
        if randtype is None:
            if self.sizetype == 0:
                self.randtype = randint(0, 3)
            else:
                self.randtype = randint(0, 2)
            if len(game.houses[sizetype]) > 1:
                if self.randtype == game.houses[sizetype][-1].randtype == game.houses[sizetype][-2].randtype:
                    if self.sizetype == 0:
                        self.randtype = randint(0, 3)
                    else:
                        self.randtype = randint(0, 2)
        else:
            self.randtype = randtype
        self.image, rect = game.images.houses[self.sizetype][self.randtype]
        self.x = game.houses_types[self.sizetype][0][0]
        for house in game.houses[self.sizetype]:
            self.x += game.houses_types[house.sizetype][0][1][house.randtype]
        self.y = game.houses_types[self.sizetype][1][self.randtype] + game.resolution[1] - 720
        if rect.x > game.resolution[0]:
            self.visible = False
            self.dirty = 0
        self.rect = pygame.Rect(self.x, self.y + rect.h, rect.w, rect.h)
        self.source_rect = pygame.Rect(0, self.rect.h, self.rect.w, self.rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if self.visible:
            if not self.drawnout:
                if self.source_rect.y > 0:
                    self.source_rect.y -= 5
                    self.rect.y -= 5
                else:
                    self.drawnout = True
                    self.rect.y = self.y
                    self.source_rect.y = 0
                    self.dirty = 1

    def calculate_currentpeople(self):
        if self.peoplecurrent < self.min_people:
            self.move_people(u"in", False)
        else:
            move_in = True
            for i in xrange(len(self.taxes)):
                if game.taxes[i] > self.taxes[i]:
                    move_in = False
                    self.move_people(u"out", game.taxes[i])
            if move_in:
                self.move_people(u"in", False)

    def move_people(self, direction, tax):
        if direction == u"out":
            if tax != 0:
                tax_out = tax / 20
            else:
                tax_out = 0
            self.peoplecurrent -= (randint(1, 5) // 5 + game.difficulty + tax_out) / 10
            if self.peoplecurrent < self.min_people:
                self.peoplecurrent = self.min_people
        else:
            if self.peoplecurrent < self.peoplemax:
                fillrate = randint(0, 3) - game.difficulty
                if fillrate < 0:
                    fillrate = 0
                self.peoplecurrent += fillrate
            else:
                self.peoplecurrent = self.peoplemax

    def calculate_min_people(self):
        self.min_people = self.peoplemax / 100 * randint(1, 4)

    def calculate_taxmax(self):
        self.taxes = [5 * randint(1, 16), 5 * randint(1, 14), 5 * randint(1, 19)]


class LeftDrawer(pygame.sprite.DirtySprite):
    def __init__(self, used_upgrades):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.visible = False
        self.layer = 10
        self.drawer_visible = True
        self.open = False
        self.rect = pygame.Rect(0, 0, 280, game.resolution[1])
        self.taxnames = [u"Beard Tax", u"Luxury Tax", u"Window Tax"]
        self.tax_buttons = []
        self.upgrade_buttons = []
        self.current_max_upgrade_buttons = 1
        self.max_screen_upgrade_buttons = round((game.resolution[1] - 170) / 70)
        self.used_upgrades = used_upgrades
        if game.bar_amounts[0] > 10:
            game.tutorial_mode = False
        for name in self.used_upgrades:
            for upgrade in game.upgrades:
                if upgrade[0] == name:
                    game.upgrades.remove(upgrade)
        self.news_obj = News(self.layer + 3)
        game.add_new_renderable(self, self.layer)

    def create_random_law(self, income, people_total):
        order = {u"Ban", u"Allow", u"Open", u"Close"}
        f_quantity = {u" some", u" all", u" many", u" most of the"}
        f_adjective = {u" weird", u" ugly", u" old", u" new", u" self-made", u" damaged", u" lovely"}
        f_noun = {u" cars", u" guns", u" books", u" boats"}
        s_order = {u"Open", u"Close"}
        s_quantity = {u" some", u" all", u" many"}
        s_adjective = {u" ugly", u" old", u" new", u" fancy"}
        s_noun = {u" hospitals", u" schools", u" factories", u" cinemas", u" banks", u" supermarkets", u" libraries",
                  u" cafes", u" theaters", u" gas stations", u" parks", u" shops"}
        all_results = (len(order - s_order) * len(f_quantity) * len(f_adjective) * len(f_noun)) + \
                      (len(s_order) * len(s_quantity) * len(s_adjective) * len(s_noun))
        first = sample(order, 1)[0]
        if first not in s_order:
            second = sample(f_quantity, 1)[0]
            third = sample(f_adjective, 1)[0]
            fourth = sample(f_noun, 1)[0]
        else:
            second = sample(s_quantity, 1)[0]
            third = sample(s_adjective, 1)[0]
            fourth = sample(s_noun, 1)[0]
        upgrade = first + second + third + fourth
        cost = round((60 * ((100 + (income + people_total) / 15) * 8.16 + income)) / 2)
        reward = round((cost / 1200) * 1.404)
        upgrade_obj = (upgrade, 0, cost, 0, reward)
        if len(self.used_upgrades) == all_results + 11:
            return
        else:
            if upgrade not in self.used_upgrades:
                return upgrade_obj
            else:
                return self.create_random_law(income, people_total)

    def create_new_law(self):
        new_law = self.create_random_law(game.bar.income + game.bar.calculate_incomereward(), game.bar.people_total)
        if new_law is not None:
            game.upgrades.append(new_law)

    def increase_max_buttons(self):
        if self.current_max_upgrade_buttons < self.max_screen_upgrade_buttons:
            self.current_max_upgrade_buttons += 1
            self.create_new_law()

    @staticmethod
    def init_unlock(unlockname):
        if unlockname == u"Metro":
            game.metro = Metro()
        elif unlockname == u"Plumbing":
            game.pipe = Pipe()
        elif unlockname == u"Moogle Fiber":
            game.fiber = Fiber()
        elif unlockname == u"Electricity":
            game.power = Power()
            game.power.shuffle_layer()
        elif unlockname == u"Water Supply":
            game.watersupply = Watersupply()
        elif unlockname == u"Wi-Fi":
            game.wifi_tower = WifiTower()
        elif unlockname == u"5G":
            game.fiveg_tower = FiveGTower()
        elif unlockname == u"Li-Fi":
            game.lifi_tower = LifiTower()

    def process_upgrades(self):
        if game.tutorial_mode and not game.menu.visible:
            if not game.tutorial.visible:
                game.tutorial.toggle()
            game.tutorial_mode = False
        for button in self.upgrade_buttons:
            button.process_location()
        if len(game.unused_upgrades) > 0:
            for unused_upgrade in game.unused_upgrades:
                self.upgrade_buttons.append(UpgradeButton(unused_upgrade, len(self.upgrade_buttons)))
                game.unused_upgrades.remove(unused_upgrade)
                for upgrade in game.upgrades:
                    if upgrade[0] == unused_upgrade[0]:
                        game.upgrades.remove(upgrade)
                        return
        else:
            for upgrade in game.upgrades:
                if game.bar.people_total >= upgrade[3]:
                    if upgrade[1] == 1:
                        priority_index = 0
                        for upgrade_button in self.upgrade_buttons:
                            if upgrade_button.upgrade[1] == 1:
                                priority_index += 1
                        self.upgrade_buttons.insert(priority_index, UpgradeButton(upgrade, priority_index))
                        game.upgrades.remove(upgrade)
                        return
                    elif self.current_max_upgrade_buttons > len(self.upgrade_buttons) < self.max_screen_upgrade_buttons:
                        self.upgrade_buttons.append(UpgradeButton(upgrade, len(self.upgrade_buttons)))
                        game.upgrades.remove(upgrade)
                        return

    def update(self):
        self.process_upgrades()
        if self.rect.collidepoint(pygame.mouse.get_pos()) or self.open:
            for button in self.tax_buttons + self.upgrade_buttons:
                if button.animatecounter > 0:
                    button.animatein = False
                if not button.animateout and not button.animatein:
                    button.slide(5)
        else:
            for button in self.tax_buttons + self.upgrade_buttons:
                if not button.animateout and not button.animatein:
                    button.slide(-5)

    def toggle(self):
        if self.drawer_visible:
            self.drawer_visible = False
        else:
            self.drawer_visible = True
        self.news_obj.global_visible = self.drawer_visible
        for button in self.tax_buttons + self.upgrade_buttons:
            button.visible = self.drawer_visible


class TaxButton(pygame.sprite.DirtySprite):
    def __init__(self, sizetype):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = 10
        self.layer_mod = self.layer + 1
        self.visible = True
        self.sizetype = sizetype
        self.drawdata = [(255, 255, 255), 14]
        self.image = self.old_image = None
        self.image_regular, rect = game.images.left_button[0]
        self.rect = pygame.Rect(-rect.w, 15 + 45 * self.sizetype, rect.w, rect.h)
        self.image_minus = game.images.left_button[1][0]
        self.image_plus = game.images.left_button[2][0]
        self.taxtxt = game.left_drawer.taxnames[self.sizetype]
        self.minx = 135 - self.rect.w
        self.maxx = 10
        self.clickable_rects = [pygame.Rect(self.minx + 206, self.rect.y + 7, 25, 20),
                                pygame.Rect(self.minx + 234, self.rect.y + 7, 25, 20)]
        self.active = True
        self.animatein = True
        self.animateout = False
        self.animatecounter = 0
        self.name_obj = RenderObject(self.layer_mod, self.visible, True, self.taxtxt, self.rect.topleft,
                                     (10, 7), (132, 20), self.drawdata, False, False)
        self.tax_obj = RenderObject(self.layer_mod, self.visible, True, unicode(game.taxes[self.sizetype]) + u"%",
                                    self.rect.topleft, (149, 7), (52, 20), self.drawdata, False, False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.check_layer_change()
        self.name_obj.process_update(False, self.visible, self.layer_mod, self.taxtxt, self.rect.topleft, False)
        self.tax_obj.process_update(False, self.visible, self.layer_mod, unicode(game.taxes[self.sizetype]) + u"%",
                                    self.rect.topleft, False)
        if self.animatein:
            if self.rect.x < self.minx - 20:
                self.dirty = 1
                self.rect.x += 4
            else:
                self.rect.x = self.minx
                self.animatein = False
                self.dirty = 1
        is_highlighted = self.mouse_hover_check()
        if is_highlighted == u"minus":
            self.image = self.image_minus
        elif is_highlighted == u"plus":
            self.image = self.image_plus
        else:
            self.image = self.image_regular
        if self.old_image != self.image:
            self.old_image = self.image
            self.dirty = 1

    def check_layer_change(self):
        if game.tutorial is not None and game.left_drawer.tax_buttons[2] == self:
            self.layer_mod = game.toggle_tutorial_layer(self, self.layer, self.layer_mod, 3)

    def mouse_click_check(self):
        for rect in self.clickable_rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                if self.clickable_rects.index(rect) == 1:
                    if game.taxes[self.sizetype] < 100:
                        game.taxes[self.sizetype] += 5
                        return True
                else:
                    if game.taxes[self.sizetype] > 0:
                        game.taxes[self.sizetype] -= 5
                        return True

    def mouse_hover_check(self):
        for rect in self.clickable_rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                if self.clickable_rects.index(rect) == 0:
                    return u"minus"
                else:
                    return u"plus"

    def slide(self, amount):
        if not self.animatein:
            if amount > 0:
                if self.rect.x < self.maxx:
                    self.rect.x += amount
                    for rect in self.clickable_rects:
                        rect.x += amount
                    self.dirty = 1
            else:
                if self.rect.x > self.minx:
                    self.rect.x += amount
                    for rect in self.clickable_rects:
                        rect.x += amount
                    self.dirty = 1


class UpgradeButton(pygame.sprite.DirtySprite):
    def __init__(self, upgrade, position):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = 10
        self.layer_mod = self.layer + 1
        if game.left_drawer.drawer_visible:
            self.visible = True
        else:
            self.visible = False
        self.upgrade = upgrade
        self.position = position
        self.name = self.upgrade[0]
        multiplier = game.difficulty
        if multiplier == 0:
            multiplier = 0.5
        self.cost = int(self.upgrade[2] * multiplier)
        self.reward = self.upgrade[4]
        self.drawdata = [(255, 255, 255), 14, u" €", u" €/s"]
        self.image = self.breakpoint = self.rect = None
        rect = game.images.upgrade_button[0][1]
        self.images = [[game.images.upgrade_button[3][0], game.images.upgrade_button[4][0],
                        game.images.upgrade_button[5][0]],
                       [game.images.upgrade_button[0][0], game.images.upgrade_button[1][0],
                        game.images.upgrade_button[2][0]]][self.upgrade[1]]
        self.miny = 155 + (rect.h + 7) * self.position
        self.rect = pygame.Rect(-rect.w, self.miny, rect.w, rect.h)
        self.source_rect = pygame.Rect(0, 0, rect.w, rect.h)
        self.minx = 20 - rect.w
        self.maxx = 10
        self.animatein = True
        self.animatemove = False
        self.animateout = False
        self.animatecounter = 280
        self.unavailable_obj = RenderObject(self.layer_mod, self.visible, False, self.images[1],
                                            self.rect.topleft, False, (rect.w, rect.h), False, False, False)
        self.name_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.name, self.rect.topleft,
                                     (12, 7), (252, 20), self.drawdata, False, False)
        self.cost_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.cost, self.rect.topleft,
                                     (12, 35), (118, 20), self.drawdata, self.drawdata[2], False)
        self.reward_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.reward, self.rect.topleft,
                                       (138, 35), (129, 20), self.drawdata, self.drawdata[3], False)
        game.add_new_renderable(self, self.layer)
        self.update()

    def update(self):
        self.check_layer_change()
        self.name_obj.process_update(False, self.visible, self.layer_mod + 1, self.name, self.rect.topleft, False)
        self.cost_obj.process_update(False, self.visible, self.layer_mod + 1, self.cost, self.rect.topleft, False)
        self.reward_obj.process_update(False, self.visible, self.layer_mod + 1, self.reward, self.rect.topleft, False)
        if self.animatemove:
            self.dirty = 1
            if self.rect.y > self.miny:
                if self.rect.y - self.miny < 10:
                    if self.rect.y - self.miny < 3:
                        self.rect.y = self.miny
                    else:
                        self.rect.y -= 3
                else:
                    self.rect.y -= 10
            elif self.miny > self.rect.y:
                if self.miny - self.rect.y < 10:
                    if self.miny - self.rect.y < 3:
                        self.rect.y = self.miny
                    else:
                        self.rect.y += 3
                else:
                    self.rect.y += 10
            else:
                self.animatemove = False
        elif self.animatein:
            self.dirty = 1
            if game.menu.visible:
                self.rect.x = self.minx
                self.animatein = False
            else:
                if self.rect.x < self.maxx:
                    self.rect.x += 10
                elif self.animatecounter > 0:
                    self.animatecounter -= 1
                else:
                    self.animatein = False
        elif self.animateout:
            self.dirty = 1
            if self.rect.right > 0:
                self.rect.x -= 10
            else:
                self.animateout = False
                self.remove()
        if game.bar.money >= self.cost:
            self.source_rect.w = self.rect.w
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.image != self.images[2]:
                    self.image = self.images[2]
                    self.dirty = 1
            else:
                if self.image != self.images[0]:
                    self.image = self.images[0]
                    self.dirty = 1
            self.unavailable_obj.process_update(False, False, self.layer_mod, self.images[1], self.rect.topleft, False)
        else:
            if self.image != self.images[0]:
                self.image = self.images[0]
                self.dirty = 1
            breakpoint = round(self.rect.w / 100 * game.bar.calculate_percentage(self.cost))
            if self.breakpoint != breakpoint:
                self.breakpoint = breakpoint
                self.source_rect.w = breakpoint
                self.dirty = 1
            self.unavailable_obj.process_update(
                1, self.visible, self.layer_mod, self.images[1], (self.rect.x + breakpoint, self.rect.y),
                pygame.Rect(breakpoint, 0, self.rect.w - breakpoint, self.rect.h))

    def check_layer_change(self):
        if game.tutorial is not None and (len(game.left_drawer.upgrade_buttons) > 0) and \
                        game.left_drawer.upgrade_buttons[0] == self:
            self.layer_mod = game.toggle_tutorial_layer(self, self.layer, self.layer_mod, 4)

    def slide(self, amount):
        if not self.animatein:
            if amount > 0:
                if self.rect.x < self.maxx:
                    self.rect.x += amount
                    self.dirty = 1
            else:
                if self.rect.x > self.minx:
                    self.rect.x += amount
                    self.dirty = 1

    def remove(self):
        game.left_drawer.used_upgrades.add(self.name)
        game.left_drawer.upgrade_buttons.remove(self)
        self.unavailable_obj.kill()
        self.kill()

    def process_location(self):
        new_pos = game.left_drawer.upgrade_buttons.index(self)
        if self.position != new_pos:
            self.position = new_pos
            self.miny = 155 + (self.rect.h + 7) * self.position
            self.animatemove = True

    def mouse_click_check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if game.bar.money >= self.cost:
                game.bar.money -= self.cost
                self.award_rewards()
                self.animateout = True
                self.animatecounter = 0
                return True

    def award_rewards(self):
        game.left_drawer.create_new_law()
        game.bar.incomereward += self.reward
        game.left_drawer.init_unlock(self.name)


class News(pygame.sprite.DirtySprite):
    def __init__(self, layer):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.visible = False
        self.global_visible = False
        self.layer = layer
        self.drawing = False
        self.counter = 0
        self.drawdata = [(0, 0, 0), 20]
        self.txt = u""
        self.image, rect = game.images.misc[1]
        self.rect = pygame.Rect(-rect.w, game.resolution[1] - 220, rect.w, rect.h)
        self.txt_obj = RenderObject(self.layer + 1, False, False, self.txt, self.rect.topleft, (70, 60), (670, 25),
                                    self.drawdata, False, False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.txt_obj.process_update(False, self.check_obj_visibility(), 0, self.txt, self.rect.topleft, False)
        if self.visible and self.global_visible:
            if self.drawing:
                if self.rect.x < -20:
                    self.dirty = 1
                    self.rect.x += 8
                else:
                    if self.counter > 50:
                        self.counter = 0
                        self.drawing = False
            else:
                if self.rect.x > -self.rect.w:
                    self.dirty = 1
                    self.rect.x -= 8
        else:
            if self.rect.x > -self.rect.w:
                self.dirty = 1
                self.visible = False
                self.rect.x = -self.rect.w

    def count(self):
        if self.rect.x > -20:
            self.counter += 1

    def check_obj_visibility(self):
        if self.visible and self.global_visible:
            return True
        else:
            return False

    @staticmethod
    def generate_news_statements(eventtype):
        news_statements = [(game.generate_name() + u" terrorists have sabotaged the city's money reserves!").upper(),
                           u"Santa Claus has been spotted by the local bank!".upper(),
                           (game.generate_name() + u" terrorists have hijacked the metro train!").upper()]
        return news_statements[eventtype]

    def present(self, eventtype):
        self.txt = self.generate_news_statements(eventtype)
        self.visible = True
        self.drawing = True


class RightDrawer(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.visible = False
        self.drawer_visible = True
        self.tap_pad_global_visible = False
        self.layer = 10
        self.x = game.resolution[0] - 220
        self.rect = pygame.Rect(self.x, 0, game.resolution[0] - self.x, game.resolution[1])
        self.right_button_names = [u"Dwelling", u"Low-end", u"High-end", u"Luxury", u"Skyscraper"]
        self.right_buttons = []
        self.open = False
        self.tapimage, rect = game.images.right_drawer[0]
        self.tapy = [game.resolution[1] - rect.h - 18, game.resolution[1] - rect.h - 13]
        self.taprect = pygame.Rect(game.resolution[0] - rect.w - 5, self.tapy[0], rect.w, rect.h)
        self.tap_pad_visible = False
        self.tapcounter = 0
        self.tap_pad_obj = RenderObject(self.layer, self.tap_pad_visible, False, self.tapimage, self.taprect.topleft,
                                        False, self.taprect.size, False, False, False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        if self.tapcounter > 0:
            tap_dirty = True
        else:
            tap_dirty = False
        self.tap_pad_obj.process_update(
            tap_dirty, self.tap_pad_visible, self.layer, self.tapimage, self.taprect.topleft, False)
        if self.rect.collidepoint(pygame.mouse.get_pos()) or self.open:
            for button in self.right_buttons:
                button.slide(-5)
        else:
            for button in self.right_buttons:
                button.slide(5)

    def process_tap_pad(self):
        if self.taprect.y == self.tapy[1]:
            self.tapcounter -= 1
            if self.tapcounter < 0:
                self.taprect.y = self.tapy[0]
                self.tapcounter = 10

    def tap_pad_click_check(self):
        if self.tap_pad_visible and self.taprect.collidepoint(pygame.mouse.get_pos()):
            game.bar.add_manual_money()
            if self.taprect.y != self.tapy[1]:
                self.taprect.y = self.tapy[1]
            return True

    def tap_pad_toggle(self):
        if self.tap_pad_visible:
            self.tap_pad_visible = False
        else:
            self.tap_pad_visible = True

    def tap_pad_global_toggle(self):
        if self.tap_pad_global_visible:
            self.tap_pad_global_visible = False
        else:
            self.tap_pad_global_visible = True

    def toggle(self):
        if self.drawer_visible:
            self.drawer_visible = False
        else:
            self.drawer_visible = True
        for button in self.right_buttons:
            if button.global_visible:
                button.visible = self.drawer_visible


class RightButton(pygame.sprite.DirtySprite):
    def __init__(self, sizetype):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.layer = 10
        self.layer_mod = self.layer + 1
        self.visible = self.global_visible = False
        self.sizetype = sizetype
        self.breakpoint = None
        self.drawdata = [(255, 255, 255), 14, u" €"]
        self.image_available, rect = game.images.right_button[0]
        self.image_available_highlighted = game.images.right_button[1][0]
        self.image_unavailable = game.images.right_button[2][0]
        self.logo = game.images.right_button_logos[self.sizetype][0]
        self.name = game.right_drawer.right_button_names[self.sizetype]
        self.amount = game.right_button_amounts[self.sizetype]
        if self.amount > 0:
            self.price = game.right_button_prices[self.sizetype]
        else:
            self.price = game.right_button_prices_fixed[self.sizetype]
        self.people = game.houses_properties[self.sizetype][0]
        self.image = self.image_available
        self.rect = pygame.Rect(game.resolution[0], 15 + 100 * self.sizetype, rect.w, rect.h)
        self.source_rect = pygame.Rect(0, 0, rect.w, rect.h)
        self.minx = game.resolution[0] - 220
        self.maxx = game.resolution[0] - 20
        self.animatein = True
        self.unavailable_obj = RenderObject(
            self.layer_mod, self.visible, False, self.image_unavailable, self.rect.topleft,
            False, (rect.w, rect.h), False, False, False)
        self.logo_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.logo, self.rect.topleft,
                                     (7, 7), (47, 48), self.drawdata, False, False)
        self.amount_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.amount, self.rect.topleft,
                                       (7, 62), (47, 19), self.drawdata, False, False)
        self.name_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.name, self.rect.topleft,
                                     (62, 7), (132, 19), self.drawdata, False, False)
        self.people_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.people, self.rect.topleft,
                                       (77, 35), (44, 19), self.drawdata, False, False)
        self.peopletotal_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.calculate_peopletotal(),
                                            self.rect.topleft, (132, 34), (63, 19), self.drawdata, False, False)
        self.price_obj = RenderObject(self.layer_mod + 1, self.visible, True, self.price, self.rect.topleft,
                                      (62, 62), (132, 19), self.drawdata, self.drawdata[2], False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.check_layer_change()
        self.logo_obj.process_update(False, self.visible, self.layer_mod + 1, self.logo, self.rect.topleft, False)
        self.amount_obj.process_update(False, self.visible, self.layer_mod + 1, self.amount, self.rect.topleft, False)
        self.name_obj.process_update(False, self.visible, self.layer_mod + 1, self.name, self.rect.topleft, False)
        self.people_obj.process_update(False, self.visible, self.layer_mod + 1, self.people, self.rect.topleft, False)
        self.peopletotal_obj.process_update(False, self.visible, self.layer_mod + 1, self.calculate_peopletotal(),
                                            self.rect.topleft, False)
        self.price_obj.process_update(False, self.visible, self.layer_mod + 1, self.price, self.rect.topleft, False)
        if self.visible:
            if self.animatein:
                self.dirty = 1
                if self.rect.x > self.maxx:
                    self.rect.x -= 2
                else:
                    self.rect.x = self.maxx
                    self.animatein = False
            if game.bar.money >= self.price:
                self.source_rect.w = self.rect.w
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.image != self.image_available_highlighted:
                        self.image = self.image_available_highlighted
                        self.dirty = 1
                else:
                    if self.image != self.image_available:
                        self.image = self.image_available
                        self.dirty = 1
                self.unavailable_obj.process_update(
                    False, False, self.layer_mod, self.image_unavailable, self.rect.topleft, False)
            else:
                if self.image != self.image_available:
                    self.image = self.image_available
                    self.dirty = 1
                breakpoint = round(self.rect.w / 100 * game.bar.calculate_percentage(self.price))
                if self.breakpoint != breakpoint:
                    self.breakpoint = breakpoint
                    self.dirty = 1
                    self.source_rect.w = breakpoint
                self.unavailable_obj.process_update(
                    1, self.visible, self.layer_mod, self.image_unavailable, (self.rect.x + breakpoint, self.rect.y),
                    pygame.Rect(breakpoint, 0, self.rect.w - breakpoint, self.rect.h))
        elif not self.global_visible:
            if game.bar.people_total >= game.houses_properties[self.sizetype][2]:
                self.global_visible = True
                if game.right_drawer.drawer_visible:
                    self.visible = True

    def check_layer_change(self):
        if game.tutorial is not None and game.right_drawer.right_buttons[0] == self:
            self.layer_mod = game.toggle_tutorial_layer(self, self.layer, self.layer_mod, 2)

    def calculate_peopletotal(self):
        people = 0
        if len(game.houses) >= self.sizetype:
            for house in game.houses[self.sizetype]:
                people += round(house.peoplecurrent)
        return people

    def mouse_click_check(self):
        if self.visible:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if game.bar.money >= self.price:
                    game.bar.money -= self.price
                    self.amount += 1
                    self.price = game.right_button_prices_fixed[
                                     self.sizetype] * game.bar.house_multiplier ** self.amount
                    game.houses[self.sizetype].append(
                        House(self.sizetype, None, game.houses_properties[self.sizetype][0]))
                    return True

    def slide(self, amount):
        if not self.animatein:
            if amount < 0:
                if self.rect.x > self.minx:
                    self.rect.x += amount
                    self.dirty = 1
            else:
                if self.rect.x < self.maxx:
                    self.rect.x += amount
                    self.dirty = 1


class Menu(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.visible = True
        self.layer = 25
        self.names = [u"new game", u"continue", u"easy", u"normal", u"insane"]
        self.xmod = [-20, 20, -92, 0, 92]
        self.ymod = [-65, -65, 15, 15, 15]
        self.sizetype = [0, 0, 2, 2, 2]
        self.buttons = []
        self.is_highlighted_button = game.difficulty + 2
        for i in xrange(5):
            self.buttons.append(MenuButton((self.xmod[i], game.resolution[1] / 2 + self.ymod[i]), self.sizetype[i],
                                           i, self.names[i]))
        self.logo, rect = game.images.menu[0][0]
        self.rect = game.screen.get_rect()
        # noinspection PyArgumentList
        self.image = pygame.Surface(game.resolution, pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 89))
        self.image.blit(self.logo, ((game.resolution[0] - rect.w) / 2, game.resolution[1] / 2 - 275))
        game.add_new_renderable(self, self.layer)

    def update(self):
        pass

    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True
        for button in self.buttons:
            button.toggle()
        game.toggle_interactables()


class MenuButton(pygame.sprite.DirtySprite):
    def __init__(self, xy, sizetype, stype, name):
        pygame.sprite.DirtySprite.__init__(self)
        self.visible = True
        self.dirty = 1
        self.layer = 26
        self.sizetype = sizetype
        self.stype = stype
        self.drawdata = []
        if self.sizetype == 0:
            self.drawdata.append((61, 61, 61))
        else:
            self.drawdata.append((255, 255, 255))
        self.drawdata.append(26)
        self.name = name
        self.image = self.old_image = None
        self.image_normal, rect = game.images.menu[1][self.sizetype]
        self.image_highlighted = game.images.menu[1][self.sizetype + 1][0]
        if xy[0] > 0:
            self.x = (game.resolution[0] / 2) + xy[0]
        elif xy[0] < 0:
            self.x = (game.resolution[0] / 2) - rect.w + xy[0]
        else:
            self.x = (game.resolution[0] - rect.w) / 2
        self.rect = pygame.Rect(self.x, xy[1], rect.w, rect.h)
        self.name_obj = RenderObject(self.layer + 1, self.visible, True, self.name, (self.rect.x, self.rect.y - 3),
                                     False, (rect.w, rect.h), self.drawdata, False, False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.name_obj.process_update(False, self.visible, 0, self.name, (self.rect.x, self.rect.y - 3), False)
        if self.rect.collidepoint(pygame.mouse.get_pos()) or self.stype == game.menu.is_highlighted_button:
            self.image = self.image_highlighted
        else:
            self.image = self.image_normal
        if self.old_image != self.image:
            self.old_image = self.image
            self.dirty = 1

    def mouse_click_check(self):
        if self.visible:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if self.stype == 0:
                    game.menu.toggle()
                    game.init_new()
                elif self.stype == 1:
                    if game.bar.money == 0:
                        return False
                    else:
                        game.menu.toggle()
                else:
                    game.filesystem_do(u"save_state", game.difficulty)
                    game.difficulty = self.stype - 2
                    game.menu.is_highlighted_button = self.stype
                    game.init_load(u"load_state")
                return True

    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True


class QuickMenu(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.visible = False
        self.layer = 21
        # noinspection PyArgumentList
        self.image = pygame.Surface(game.resolution, pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 127))
        self.rect = game.screen.get_rect()
        rect = game.images.quick_menu[0][1]
        self.innerxy = ((self.rect.w - rect.w) / 2, (self.rect.h - rect.h) / 2)
        self.rectsxy = (16, [15, 67, 119, 171, 223, 275])
        self.main_image, mainrect = game.images.quick_menu[0]
        self.quick_menu_obj = RenderObject(self.layer + 4, self.visible, True, self.main_image,
                                           self.innerxy, False, mainrect.size, False, False, False)
        self.h_image, h_rect = game.images.quick_menu[1]
        self.highlight_objs = []
        for i in xrange(6):
            self.highlight_objs.append(RenderObject(self.layer + 5, self.visible, False, self.h_image,
                                                    (self.innerxy[0] + self.rectsxy[0],
                                                     self.innerxy[1] + self.rectsxy[1][i]),
                                                    False, h_rect.size, False, False, False))
        self.sounds_obj = QuickSounds(self.layer + 1, self.innerxy, mainrect.w)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.quick_menu_obj.process_update(False, self.visible, 0, self.main_image, self.innerxy, False)
        self.mouse_hover_check()

    def mouse_hover_check(self):
        for obj in self.highlight_objs:
            if self.visible:
                if (obj == self.highlight_objs[0] and self.sounds_obj.global_visible) or \
                        (obj == self.highlight_objs[1] and game.right_drawer.tap_pad_global_visible):
                    visible = True
                else:
                    if obj.rect.collidepoint(pygame.mouse.get_pos()):
                        visible = True
                    else:
                        visible = False
            else:
                visible = False
            obj.process_update(False, visible, 0, self.h_image, False, False)

    def mouse_click_check(self):
        if self.visible:
            for obj in self.highlight_objs:
                if obj.rect.collidepoint(pygame.mouse.get_pos()):
                    if obj == self.highlight_objs[0]:
                        self.toggle_sounds()
                    elif obj == self.highlight_objs[1]:
                        game.right_drawer.tap_pad_global_toggle()
                    elif obj == self.highlight_objs[2]:
                        self.toggle()
                        game.tutorial.toggle()
                    elif obj == self.highlight_objs[3]:
                        self.toggle()
                    elif obj == self.highlight_objs[4]:
                        self.toggle()
                        game.menu.toggle()
                    elif obj == self.highlight_objs[5]:
                        game.running = False
                    return True

    def toggle_sounds(self):
        if self.sounds_obj.global_visible:
            self.sounds_obj.global_visible = False
        else:
            self.sounds_obj.global_visible = True

    def toggle(self):
        if self.visible:
            self.visible = False
            self.sounds_obj.global_visible = False
            self.sounds_obj.visible = False
        else:
            self.visible = True
        game.toggle_interactables()


class QuickSounds(pygame.sprite.DirtySprite):
    def __init__(self, layer, mainxy, main_w):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.visible = False
        self.global_visible = False
        self.layer = layer
        self.image, rect = game.images.quick_menu[2]
        self.minx = mainxy[0] + main_w - 18
        self.maxx = self.minx + 23
        self.rect = pygame.Rect(self.minx, mainxy[1], rect.w, rect.h)
        self.source_rect = pygame.Rect(rect.w, 0, rect.w, rect.h)
        self.speed = 6
        self.rectsxy = (19, [15, 67, 119])
        self.c_rectsxy = [27, [8, 60, 112]]
        self.h_image, h_rect = game.images.quick_menu[3]
        self.c_image, c_rect = game.images.quick_menu[4]
        self.checked_objs = []
        self.checked_objs_visible = [True, True, True]
        self.highlight_objs = []
        for i in xrange(3):
            self.highlight_objs.append(RenderObject(self.layer + 1, self.visible, False, self.h_image,
                                                    (self.maxx + self.rectsxy[0],
                                                     self.rect.y + self.rectsxy[1][i]),
                                                    False, h_rect.size, False, False, False))
            self.checked_objs.append(RenderObject(self.layer + 2, self.visible, False, self.c_image,
                                                  (self.rect.x + self.c_rectsxy[0] - self.source_rect.x,
                                                   self.rect.y + self.c_rectsxy[1][i]),
                                                  False, c_rect.size, False, False, False))
        game.add_new_renderable(self, self.layer)

    def mouse_hover_check(self):
        for obj in self.highlight_objs:
            if self.visible and self.rect.x == self.maxx:
                if obj.rect.collidepoint(pygame.mouse.get_pos()):
                    visible = True
                else:
                    visible = False
            else:
                visible = False
            obj.process_update(False, visible, 0, self.h_image, False, False)

    def mouse_click_check(self):
        if self.visible and self.rect.x == self.maxx:
            for i in xrange(3):
                if self.highlight_objs[i].rect.collidepoint(pygame.mouse.get_pos()):
                    if self.checked_objs_visible[i]:
                        self.checked_objs_visible[i] = False
                    else:
                        self.checked_objs_visible[i] = True
                    return True

    def update(self):
        self.mouse_hover_check()
        if self.global_visible:
            if self.rect.right < self.maxx + self.rect.w:
                self.visible = True
                if self.source_rect.x > 0:
                    self.source_rect.x -= self.speed
                    return
                else:
                    self.source_rect.x = 0
                self.rect.x += self.speed
            elif self.rect.x == self.maxx:
                self.dirty = 0
            else:
                self.dirty = 1
                self.rect.x = self.maxx
        else:
            if self.source_rect.x < self.source_rect.w:
                self.dirty = 1
                if self.rect.left > self.minx:
                    self.rect.x -= self.speed
                    return
                else:
                    self.rect.x = self.minx
                self.source_rect.x += self.speed
            elif self.source_rect.x == self.source_rect.w:
                self.visible = False
                self.global_visible = False
            else:
                self.dirty = 1
                self.source_rect.x = self.source_rect.w
        for i in xrange(3):
            self.checked_objs[i].process_update(
                False, self.check_obj_visibility(i), 0, self.c_image,
                (self.rect.x + self.c_rectsxy[0] - self.source_rect.x, self.rect.y + self.c_rectsxy[1][i]), False)

    def check_obj_visibility(self, index):
        if self.visible and self.checked_objs_visible[index]:
            return True
        else:
            return False


class Tutorial(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.visible = False
        self.layer = 13
        # noinspection PyArgumentList
        self.image = pygame.Surface(game.resolution, pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 127))
        self.rect = game.screen.get_rect()
        self.guide_obj = TutorialGuide(self.layer + 3)
        self.buttonsimage, rect = game.images.tutorial[5]
        self.h_image, h_rect = game.images.tutorial[6]
        self.innerxy = ((game.resolution[0] - rect.w) / 2, game.resolution[1] - 320)
        self.buttons_obj = RenderObject(self.layer + 1, self.visible, False, self.buttonsimage,
                                        self.innerxy, False, rect.size, False, False, False)
        self.rectsxy = ([9, 114, 219], 10)
        self.highlight_objs = []
        for i in xrange(3):
            self.highlight_objs.append(RenderObject(self.layer + 2, self.visible, False, self.h_image,
                                                    (self.innerxy[0] + self.rectsxy[0][i],
                                                     self.innerxy[1] + self.rectsxy[1]), False,
                                                    h_rect.size, False, False, False))
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.buttons_obj.process_update(False, self.visible, 0, self.buttonsimage, False, False)
        self.mouse_hover_check()

    def mouse_hover_check(self):
        for obj in self.highlight_objs:
            if self.visible:
                if obj.rect.collidepoint(pygame.mouse.get_pos()):
                    visible = True
                else:
                    visible = False
            else:
                visible = False
            obj.process_update(False, visible, 0, self.h_image, False, False)

    def mouse_click_check(self):
        if self.visible:
            for obj in self.highlight_objs:
                if obj.rect.collidepoint(pygame.mouse.get_pos()):
                    if obj == self.highlight_objs[0]:
                        self.guide_obj.switch_tutorial(-1)
                    elif obj == self.highlight_objs[1]:
                        self.guide_obj.switch_tutorial(1)
                    elif obj == self.highlight_objs[2]:
                        self.toggle()
                    return True

    def toggle(self):
        if self.visible:
            self.visible = False
            self.guide_obj.visible = False
        else:
            self.visible = True
            self.guide_obj.visible = True


class TutorialGuide(pygame.sprite.DirtySprite):
    def __init__(self, layer):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.visible = False
        self.layer = layer
        self.tutscreen = self.oldscreen = 0
        self.image = self.rect = None
        spaceimage, spacerect = game.images.tutorial[0]
        barimage, barrect = game.images.tutorial[1]
        rightimage, rightrect = game.images.tutorial[2]
        taximage, taxrect = game.images.tutorial[3]
        upgradeimage, upgraderect = game.images.tutorial[4]
        self.images = [spaceimage, barimage, rightimage, taximage, upgradeimage]
        self.objxy = [((game.resolution[0] - spacerect.w) / 2, game.resolution[1] - 248),
                      ((game.resolution[0] - barrect.w) / 2 - 25, 35), (game.right_drawer.x - 318, 22),
                      (133, 108), (95, 127)]
        self.objwh = [spacerect.size, barrect.size, rightrect.size, taxrect.size, upgraderect.size]
        self.update_screen()
        game.add_new_renderable(self, self.layer)

    def update(self):
        if self.visible:
            self.manage_drawers()
            if self.tutscreen > self.get_max_screens():
                self.switch_tutorial(-1)
        else:
            game.left_drawer.open = False
            game.right_drawer.open = False

    def switch_tutorial(self, direction):
        if self.visible:
            if direction > 0:
                if self.tutscreen < self.get_max_screens():
                    self.tutscreen += direction
                    self.update_screen()
            else:
                if self.tutscreen > 0:
                    self.tutscreen += direction
                    self.update_screen()

    def update_screen(self):
        self.dirty = 1
        self.image = self.images[self.tutscreen]
        self.rect = pygame.Rect(self.objxy[self.tutscreen], self.objwh[self.tutscreen])

    @staticmethod
    def get_max_screens():
        maxscreen = 3
        if len(game.left_drawer.upgrade_buttons) > 0:
            maxscreen = 4
        return maxscreen

    def manage_drawers(self):
        if self.tutscreen == 2:
            game.right_drawer.open = True
        elif self.oldscreen == 2:
            game.right_drawer.open = False
        if self.tutscreen == 3 or (self.tutscreen == 4 == self.get_max_screens()):
            game.left_drawer.open = True
        elif self.oldscreen >= 3:
            game.left_drawer.open = False
        self.oldscreen = self.tutscreen


class Bar(pygame.sprite.DirtySprite):
    def __init__(self, used_bonuses, used_notifications):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.visible = True
        self.layer = 10
        self.layer_mod = self.layer + 1
        self.animatein = True
        self.image, rect = game.images.bar[0]
        self.h_image, h_rect = game.images.bar[1]
        self.rect = pygame.Rect((game.resolution[0] - rect.w) / 2 + 25, -rect.h, rect.w, rect.h)
        self.maxy = 6
        self.people_total = self.income = self.houses_income = 0
        self.money = game.bar_amounts[0]
        self.incomereward = game.bar_amounts[1]
        self.income_manual = self.income_manual_time = 0
        self.income_manual_data = []
        self.house_multiplier = 1.15572735
        self.used_bonuses = used_bonuses
        for item in self.used_bonuses:
            for bonus in game.money_bonuses:
                if item[0] == bonus[0]:
                    game.money_bonuses.remove(item)
        self.city_txt = u"Nowhere"
        self.used_notifications = used_notifications
        self.notification_txt = u""
        self.notify_counter = 0
        if len(self.used_notifications) > 0:
            self.notification_txt = self.used_notifications[-1][1]
        for item in self.used_notifications:
            for notification in game.notifications:
                if item[0] == notification[0]:
                    if notification[3] != 0:
                        self.city_txt = notification[3]
                    game.notifications.remove(notification)
        self.objxy = ([7, 192, 456, 700, 593], [7, 33])
        self.objwh = ([181, 261, 239, 583, 147], 22)
        self.drawdata = [(255, 255, 255), 14, [u" €", u" €/s"]]
        self.people_obj = RenderObject(self.layer_mod, self.visible, True, self.get_people(u"total"),
                                       self.rect.topleft, (self.objxy[0][0], self.objxy[1][0]),
                                       (self.objwh[0][0], self.objwh[1]), self.drawdata, False, False)
        self.money_obj = RenderObject(self.layer_mod, self.visible, True, self.money, self.rect.topleft,
                                      (self.objxy[0][1], self.objxy[1][0]), (self.objwh[0][1], self.objwh[1]),
                                      self.drawdata, self.drawdata[2][0], False)
        self.income_obj = RenderObject(self.layer_mod, self.visible, True, self.get_income(u"total"),
                                       self.rect.topleft, (self.objxy[0][2], self.objxy[1][0]),
                                       (self.objwh[0][2], self.objwh[1]), self.drawdata, self.drawdata[2][1], False)
        self.highlight_obj = RenderObject(self.layer_mod, self.visible, False, self.h_image, self.rect.topleft,
                                          (self.objxy[0][3], self.objxy[1][0]), h_rect.size, False, False, False)
        self.notification_obj = RenderObject(self.layer, self.visible, True, self.notification_txt, self.rect.topleft,
                                             (self.objxy[0][0], self.objxy[1][1]), (self.objwh[0][3], self.objwh[1]),
                                             self.drawdata, False, False)
        self.city_obj = RenderObject(self.layer_mod, self.visible, True, self.city_txt, self.rect.topleft,
                                     (self.objxy[0][4], self.objxy[1][1]), (self.objwh[0][4], self.objwh[1]),
                                     self.drawdata, False, False)
        # self.fps_obj = RenderObject(self.layer_mod, self.visible, True, game.clock.get_fps(), self.rect.topleft,
        #                             (660, self.objxy[1][0]), (44, self.objwh[1]), self.drawdata, False, False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.income_manual_time += game.tick
        self.mouse_hover_check()
        self.check_layer_change()
        self.people_obj.process_update(
            False, self.visible, self.layer_mod, self.get_people(u"total"), self.rect.topleft, False)
        self.money_obj.process_update(
            False, self.visible, self.layer_mod, self.money, self.rect.topleft, False)
        self.income_obj.process_update(
            False, self.visible, self.layer_mod, self.get_income(u"total"), self.rect.topleft, False)
        self.notification_obj.process_update(
            False, self.visible, self.layer_mod, self.notification_txt, self.rect.topleft, False)
        self.city_obj.process_update(
            False, self.visible, self.layer_mod, self.city_txt, self.rect.topleft, False)
        # self.fps_obj.process_update(
        #     False, self.visible, self.layer_mod, game.clock.get_fps(), self.rect.topleft, False)
        if self.animatein:
            self.dirty = 1
            if self.rect.y < self.maxy:
                self.rect.y += 2
            else:
                self.rect.y = self.maxy
                self.animatein = False

    def check_layer_change(self):
        if game.tutorial is not None:
            self.layer_mod = game.toggle_tutorial_layer(self, self.layer, self.layer_mod, 1)

    def get_people(self, peopletype):
        if peopletype == u"current":
            people = 0
            for sizetype in game.houses:
                for house in sizetype:
                    people += round(house.peoplecurrent)
            return people
        elif peopletype == u"total":
            return unicode(format(int(self.get_people(u"current")), u",d")) + u"/" + unicode(
                format(int(self.people_total), u",d"))

    def add_manual_money(self):
        game.sounds.play(u"space")
        manual_income = 100 + (self.income + self.people_total) / 15
        self.money += manual_income
        self.income_manual_data.append((manual_income, self.income_manual_time))
        randomevent = randint(1, 1500)
        if randomevent == 1:
            self.money /= 300
            game.left_drawer.news_obj.present(0)
        elif randomevent == 800:
            self.money *= 10
            game.left_drawer.news_obj.present(1)

    def process_notifications(self):
        for notification in game.notifications:
            if isinstance(notification[2], int):
                if self.people_total >= notification[2]:
                    self.notify(notification)
                    self.notify_counter = 70
                    return
            else:
                if notification[2][0] in game.left_drawer.used_upgrades:
                    self.notify(notification)
                    self.notify_counter = 70
                    return
        if self.notify_counter < 0:
            self.notification_txt = u""
        else:
            self.notify_counter -= 1

    def notify(self, notification):
        game.sounds.play(u"notification")
        self.notification_txt = notification[1]
        if notification[3] != 0:
            self.city_txt = notification[3]
        self.used_notifications.append(notification)
        game.notifications.remove(notification)

    def process_money_bonuses(self):
        for bonus in game.money_bonuses:
            if self.people_total >= bonus[2]:
                self.money += bonus[1]
                self.used_bonuses.append(bonus)
                game.money_bonuses.remove(bonus)
                break

    def process_income(self):
        self.get_income(u"current")
        self.money += (self.income + self.calculate_incomereward()) / 100

    def calculate_manual_income(self):
        if len(self.income_manual_data) > 0:
            self.income_manual = 0
            temp_list = []
            for i in xrange(len(self.income_manual_data)):
                if not self.income_manual_time - self.income_manual_data[i][1] > 1000:
                    temp_list.append(self.income_manual_data[i])
            self.income_manual_data = temp_list
            for value in self.income_manual_data:
                self.income_manual += value[0]
        else:
            self.income_manual = 0

    def get_income(self, incometype):
        if incometype == u"current":
            income = 0
            tax = 0
            for taxtype in game.taxes:
                tax += taxtype
            for sizetype in game.houses:
                for house in sizetype:
                    income += round(house.peoplecurrent) * self.house_multiplier * \
                              game.houses_properties[house.sizetype][1]
            taxed_income = income * (1 + tax / 100)
            self.income = taxed_income
        elif incometype == u"total":
            return unicode(format(int(round(
                self.income + self.income_manual + self.calculate_incomereward())), u",d")) + u"/" + \
                   unicode(format(int(round(self.houses_income + self.incomereward)), u",d") + u" €/s")

    def calculate_incomereward(self):
        if self.people_total == 0:
            return 0
        percent = self.get_people(u"current") / self.people_total * 100
        if percent < 10:
            return self.incomereward * percent / 10
        else:
            return self.incomereward

    def calculate_percentage(self, price):
        if self.money == 0:
            return 0
        return self.money / price * 100

    def mouse_hover_check(self):
        if self.visible:
            if self.highlight_obj.rect.collidepoint(pygame.mouse.get_pos()):
                visible = True
            else:
                visible = False
        else:
            visible = False
        self.highlight_obj.process_update(False, visible, self.layer_mod, self.h_image, self.rect.topleft, False)

    def mouse_click_check(self):
        if self.visible:
            if self.highlight_obj.rect.collidepoint(pygame.mouse.get_pos()):
                if game.tutorial.visible:
                    game.tutorial.toggle()
                game.quick_menu.toggle()
                return True

    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True


class RenderObject(pygame.sprite.DirtySprite):
    def __init__(self, layer, visible, middle, obj, main_obj_xy, inner_relative_xy, inner_obj_wh, drawdata,
                 txt_end, source_rect):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = layer
        self.visible = self.global_visible = visible
        self.middle = middle
        self.txt_end = txt_end
        self.drawdata = drawdata
        if drawdata:
            self.txt_font = game.fonts.load_font(u"GOTHICB.TTF", drawdata[1])
        self.image = self.rect = self.new_obj = self.old_obj = self.main_obj_xy = self.old_main_obj_xy = \
            self.innerrect = self.source_rect = None
        if not inner_relative_xy:
            self.inner_relative_xy = (0, 0)
        else:
            self.inner_relative_xy = inner_relative_xy
        self.inner_obj_wh = inner_obj_wh
        if source_rect:
            self.source_rect = source_rect
        if not main_obj_xy:
            main_obj_xy = (0, 0)
        self.process_update(False, visible, layer, obj, main_obj_xy, source_rect)
        self.update()
        game.add_new_renderable(self, self.layer)

    def process_string(self, obj):
        self.image = self.txt_font.render(obj, True, self.drawdata[0])

    def process_integer(self, obj):
        obj = unicode(format(int(obj), u",d"))
        if self.txt_end:
            obj += self.txt_end
        self.process_string(obj)

    def process_float(self, obj):
        self.process_integer(round(obj))

    def process_image(self, obj):
        self.image = obj

    def process_update(self, force_dirty, visible, layer, obj, main_obj_xy, source_rect):
        self.dirty = force_dirty
        if self.global_visible != visible:
            self.global_visible = self.visible = visible
        self.new_obj = obj
        if main_obj_xy:
            self.main_obj_xy = main_obj_xy
        if source_rect:
            self.source_rect = source_rect
        if layer != 0 and self.layer != layer:
            game.allsprites.remove(self)
            game.add_new_renderable(self, layer)
            self.layer = layer

    def update(self):
        if self.old_main_obj_xy != self.main_obj_xy or self.old_obj != self.new_obj:
            self.dirty = 1
            if self.old_main_obj_xy != self.main_obj_xy:
                self.old_main_obj_xy = self.main_obj_xy
                self.innerrect = pygame.Rect(
                    self.main_obj_xy[0] + self.inner_relative_xy[0], self.main_obj_xy[1] + self.inner_relative_xy[1],
                    self.inner_obj_wh[0], self.inner_obj_wh[1])
            if self.old_obj != self.new_obj:
                self.old_obj = self.new_obj
                if isinstance(self.new_obj, unicode):
                    self.process_string(self.new_obj)
                elif isinstance(self.new_obj, int):
                    self.process_integer(self.new_obj)
                elif isinstance(self.new_obj, float):
                    self.process_float(self.new_obj)
                else:
                    self.process_image(self.new_obj)
            imagerect = self.image.get_rect()
            if self.middle:
                self.rect = pygame.Rect(self.innerrect.x + (self.inner_obj_wh[0] - imagerect.w) / 2,
                                        self.innerrect.y + (self.inner_obj_wh[1] - imagerect.h) / 2,
                                        imagerect.w, imagerect.h)
            else:
                self.rect = pygame.Rect(self.innerrect.x, self.innerrect.y, imagerect.w, imagerect.h)
            if self.rect.right < 0 or self.rect.left > game.resolution[0] or not self.global_visible:
                self.visible = False
            else:
                if not self.visible:
                    self.visible = True


if __name__ == u'__main__':
    game = Game()
    game.run()
