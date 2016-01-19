# -*- coding: utf-8 -*-
import pygame
import os.path
from random import randint, sample
main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
    def __init__(self):
        self.fps_cap = 120
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1600, 900))
        self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.running = True
        self.difficulty = 1

        self.used_upgrades = []
        self.taxnames = ["Beard Tax", "Luxury Tax", "Window Tax"]
        self.bar_amounts = [0, 0, 0, 0]
        self.taxes = [0, 0, 0]

        self.houses = [[], [], [], [], []]
        self.houses_states = [[], [], [], [], []]
        self.houses_properties = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        self.right_button_names = ["Dwelling", "Low-end", "High-end", "Luxury", "Skyscraper"]
        self.right_button_prices_fixed = [0, 0, 0, 0, 0]
        self.right_button_prices = [0, 0, 0, 0, 0]
        self.right_button_amounts = [0, 0, 0, 0, 0]

        # houses_types = sizetype(randtype[xbase, randtype[x laius/+vahe]], randtype[y from bottom])
        self.houses_types = [([-15, [190, 125, 240, 125]], [432, 347, 427, 347]),
                             ([5, [90, 96, 242]], [340, 335, 328]),
                             ([-30, [103, 96, 170]], [255, 255, 250]),
                             ([-10, [128, 180, 223]], [115, 130, 130]),
                             ([-40, [170, 135, 150]], [73, 59, 41])]

        # upgrades = name{box}, cost{box}, (reward type{box}, amount/reward), (unlock type{priv}, amount{priv})
        self.upgrades = [("Electricity", 300000, ("unlock", "Power"), ("incometotal", 100)),
                         ("Plumbing", 400712, ("unlock", "Pipe"), ("incometotal", 160)),
                         ("Water Supply", 618584, ("unlock", "Water"), ("incometotal", 243)),
                         ("Metro", 1103622, ("unlock", "Metro"), ("incometotal", 341)),
                         ("Santa Claus", 2275607, ("income", 761), ("incometotal", 449)),
                         ("Wi-Fi", 5422875, ("income", 1813), ("incometotal", 567)),
                         ("Google Fiber", 14935416, ("unlock", "Fiber"), ("incometotal", 692)),
                         ("5G", 47540139, ("income", 15893), ("incometotal", 822)),
                         ("Li-Fi", 174887578, ("income", 58466), ("incometotal", 959)),
                         ("World Peace", 743554611, ("income", 248575), ("incometotal", 1100))]

        self.houses_properties = [
            (200, 0.2, 0), (900, 0.4, 600), (2560, 1, 3500), (7200, 1.8, 10800), (13500, 6, 27000)]
        self.right_button_prices_fixed = [750, 9000, 40000, 486000, 2531250]

        self.images = self.sounds = self.background = self.cursor = self.cloud = self.metro = self.pipe = self.fiber = \
            self.power = self.watersupply = self.bar = self.right_drawer = self.left_drawer = self.quick_menu = \
            self.clock = self.menu = None
        self.allsprites = pygame.sprite.LayeredDirty()
        self.allsprites.set_timing_treshold(10000)
        self.activeclouds = []

    def initialize(self):
        self.images = Images()
        self.sounds = Sounds()
        self.background = Background()
        self.quick_menu = QuickMenu()
        self.cursor = Cursor()
        self.cloud = Cloud(10)
        # self.metro = Metro(game)
        self.fiber = Fiber()
        self.watersupply = Watersupply()
        self.pipe = Pipe()
        self.power = Power()
        self.left_drawer = LeftDrawer(self.used_upgrades)
        self.right_drawer = RightDrawer()
        self.bar = Bar()
        for sizetype in range(5):
            game.right_drawer.right_buttons.append(RightButton(sizetype))
        for sizetype in range(3):
            game.left_drawer.tax_buttons.append(TaxButton(sizetype))
        self.menu = Menu()

    def add_new_renderable(self, obj, layer):
        self.allsprites.add(obj, layer = layer)

    def run(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        self.initialize()

        while self.running:
            self.clock.tick(self.fps_cap)
            self.process_events()
            self.allsprites.update()
            dirtyrects = self.allsprites.draw(self.screen)
            pygame.display.update(dirtyrects)
            pygame.display.set_caption(
                "FPS: " + str(round(self.clock.get_fps(), 2)) + ", Redrawing: " + str(len(dirtyrects)))
            if self.running:
                pass

                # todo 1. new layereddirty, get displaysurface, blur it, use as background
                # todo fps läheb üliaeglaseks?

                # http://stackoverflow.com/questions/30723253/blurring-in-pygame

                # todo 2. or make superclass, blur all objects when game.menu_running
                # menu buttons n stuff on higher layers

        pygame.time.wait(50)
        pygame.quit()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 4:
                if game.metro is not None:
                    game.metro.update_metro_counter()
            elif event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quick_menu.toggle()
                    if not game.menu.visible:
                        pass
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game.quick_menu.mouse_click_check():
                    self.sounds.click.play()
                for button in game.right_drawer.right_buttons + game.left_drawer.tax_buttons + \
                        game.left_drawer.upgrade_buttons + game.menu.buttons:
                    if button.mouse_click_check():
                        self.sounds.click.play()

    def toggle_interactables(self):
        self.left_drawer.toggle()
        self.bar.toggle()
        self.right_drawer.toggle()


class Images:
    def __init__(self):
        self.background = self.load_image("Background.png")
        self.cursor = self.load_image("Cursor.png")
        self.right_button = [self.load_image("Button_available.png"), self.load_image("Button_available_hover.png"),
                             self.load_image("Button_unavailable.png")]
        self.right_button_logos = [self.load_image("House_1_logo.png"), self.load_image("House_2_logo.png"),
                                   self.load_image("House_3_logo.png"), self.load_image("House_4_logo.png"),
                                   self.load_image("House_5_logo.png")]
        self.left_button = [self.load_image("Tax.png"), self.load_image("Tax_hover_minus.png"),
                            self.load_image("Tax_hover_plus.png")]
        self.upgrade_button = [self.load_image("Upgrade_available.png"), self.load_image("Upgrade_unavailable.png"),
                               self.load_image("Upgrade_available_hover.png")]
        self.bar = self.load_image("Bar.png")
        self.misc = [self.load_image("Cloud.png"), self.load_image("Breaking_news.png"),
                     self.load_image("Pipe.png"), self.load_image("Google_Fiber.png"),
                     self.load_image("Electricity.png"), self.load_image("Water.png")]
        self.houses = [
            [self.load_image("House_11.png"), self.load_image("House_12.png"), self.load_image("House_13.png"),
             self.load_image("House_14.png")],
            [self.load_image("House_21.png"), self.load_image("House_22.png"), self.load_image("House_23.png")],
            [self.load_image("House_31.png"), self.load_image("House_32.png"), self.load_image("House_33.png")],
            [self.load_image("House_41.png"), self.load_image("House_42.png"), self.load_image("House_43.png")],
            [self.load_image("House_51.png"), self.load_image("House_52.png"), self.load_image("House_53.png")]]
        self.metro = [self.load_image("Metro.png"), self.load_image("Metro_train.png")]
        self.menu = [[self.load_image("Urbancity_logo.png")],
                     [self.load_image("Menu_big_button.png"), self.load_image("Menu_big_button_hover.png"),
                      self.load_image("Menu_small_button.png"), self.load_image("Menu_small_button_hover.png")]]
        self.quick_menu = [self.load_image("Quick_menu_normal.png"), self.load_image("Quick_menu_hover_mute.png"),
                           self.load_image("Quick_menu_hover_main_menu.png"),
                           self.load_image("Quick_menu_hover_quit.png")]

    @staticmethod
    def load_image(file):
        file = os.path.join(main_dir, 'data', file)
        try:
            loaded_image = pygame.image.load(file).convert_alpha()
        except:
            raise SystemExit("Could not load image " + file + ", " + pygame.get_error())
        return loaded_image, loaded_image.get_rect()


class Sounds:
    def __init__(self):
        Sounds.load_sound("house_lo.ogg", "music")
        self.click = Sounds.load_sound("Mouse_press.ogg", "sound")

    @staticmethod
    def toggle_mute():
        if pygame.mixer.get_num_channels() > 0:
            pygame.mixer.set_num_channels(0)
            pygame.mixer.music.pause()
        else:
            pygame.mixer.set_num_channels(8)
            pygame.mixer.music.unpause()

    @staticmethod
    def load_sound(file, soundtype):
        file = os.path.join(main_dir, 'data\\test_helid', file)
        if soundtype == "music":
            pygame.mixer.music.load(file)
            # pygame.mixer.music.play(-1)
            # pygame.mixer.music.set_volume(0.1)
        else:
            try:
                loaded_sound = pygame.mixer.Sound(file)
                loaded_sound.set_volume(0.5)
            except pygame.error:
                raise SystemExit("Could not load sound " + file + ", " + pygame.get_error())
            return loaded_sound


class Background:
    def __init__(self):
        # noinspection PyArgumentList
        self.surface = pygame.Surface(game.resolution).convert()
        self.image, self.rect = game.images.background
        self.skyarearect = pygame.Rect(0, 0, game.resolution[0], game.resolution[1] - self.rect.h)
        self.surface.fill((125, 196, 255), self.skyarearect)
        self.timesx = game.resolution[0] // self.rect.w + 1
        for column in range(int(self.timesx)):
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
        self.dirty = 1
        self.layer = 5
        self.image, rect = game.images.metro[0]

        self.rect = pygame.Rect((game.resolution[0] - rect.w) / 2, game.resolution[1] - 111, rect.w, rect.h)

        self.arearect = pygame.Rect(self.trainw, 0, self.trainw, self.trainh)
        self.speed = 4
        self.time_from_beginning = 0
        self.drawnoutarea = pygame.Rect(0, self.metroh, self.metrow, self.metroh)
        self.drawnout = False
        self.waiting = False
        self.trainstopwaiting = True
        self.terroristevent = False
        self.terroristcounter = 0

        self.train_obj = MetroTrain(self.layer + 1, self.rect.topleft)

    def draw(self):
        self.draw_metro_background()
        if self.drawnout:
            self.update_metro()
            self.draw_moving_metro()

    def draw_metro_background(self):
        if self.drawnout:
            self.surface.blit(self.image_metro, self.metrorect)
        else:
            if self.drawnoutarea.y > 0:
                self.drawnoutarea.y -= 5
                self.metrorect.y -= 5
                self.surface.blit(self.image_metro, self.metrorect, self.drawnoutarea)
            else:
                self.drawnout = True
                self.metrorect.y = self.metroy
                self.surface.blit(self.image_metro, self.metrorect)

    def update_metro(self):
        if self.terroristevent:
            if self.terroristcounter == 0:
                self.metrow -= 15
                self.speed = 18
            elif self.terroristcounter == 450:
                pass
                # game.news.present("metro")
            elif self.terroristcounter == 1250:
                self.metrow += 15
                self.speed = 4
                self.terroristcounter = -1
                self.terroristevent = False
            self.terroristcounter += 1
        if not self.waiting:
            if self.trainrect.x + self.trainrect.w < self.metrorect.x + self.metrow:
                if self.arearect.x > 0:
                    self.arearect.x -= self.speed
                else:
                    if self.trainrect.x > self.trainstop and self.trainstopwaiting and not self.terroristevent:
                        pygame.time.set_timer(pygame.USEREVENT + 4, 4000)
                        self.waiting = True
                    self.trainrect.x += self.speed
            elif self.arearect.x > -self.trainw:
                self.arearect.x -= self.speed
            else:
                if self.terroristevent:
                    pygame.time.set_timer(pygame.USEREVENT + 4, randint(100, 500))
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 4, randint(6000, 9000))
                self.waiting = True

    def update_metro_counter(self):
        if self.trainstopwaiting:
            self.trainstopwaiting = False
        else:
            self.trainrect.x = self.metrox
            self.arearect.x = self.trainw
            self.arearect.w = self.trainw
            if randint(1, 10) < 4:
                self.trainstopwaiting = True
            if randint(1, 3000) == 500:
                self.terroristevent = True
        self.waiting = False
        pygame.time.set_timer(pygame.USEREVENT + 4, 0)

    def draw_moving_metro(self):
        self.surface.blit(self.image_train, self.trainrect, self.arearect)


class MetroTrain(pygame.sprite.DirtySprite):
    def __init__(self, layer, xy):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = layer
        self.image, rect = game.images.metro[1]
        self.rect = pygame.Rect(xy[0], xy[1] + 50, rect.w - 2, rect.h)

        self.trainstop = self.metrox + 20


class Pipe(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 4
        self.drawnout = False
        self.surface, self.rect = game.images.misc[2]
        self.fixedy = game.resolution[1] - self.rect.h + 30
        self.rect.y = self.fixedy + self.rect.h
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
        self.surface, self.rect = game.images.misc[3]
        self.rect.y = game.resolution[1] - self.rect.h - 90
        self.timesx = game.resolution[0] // self.rect.w + 1
        # noinspection PyArgumentList
        self.image = pygame.Surface((game.resolution[0], self.rect.h), pygame.SRCALPHA).convert_alpha()
        for column in range(int(self.timesx)):
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
        self.surface, self.rect = game.images.misc[5]
        self.shift = 6
        self.rect.y = game.resolution[1] - self.rect.h + 5
        self.timesx = game.resolution[0] // self.rect.w + 1
        # noinspection PyArgumentList
        self.image = pygame.Surface((game.resolution[0], self.rect.h), pygame.SRCALPHA).convert_alpha()
        for column in range(int(self.timesx)):
            rect = pygame.Rect(self.rect.w * column - self.shift * (column + 1), 0, self.rect.w, self.rect.h)
            arearect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            if column == self.timesx - 1:
                arearect.w = game.resolution[0] - self.rect.w * column + self.shift * self.timesx
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


class Power(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 6
        self.drawnout = False
        self.surface, self.rect = game.images.misc[4]
        self.fixedy = game.resolution[1] - self.rect.h - game.background.rect.h + 10
        self.rect.y = self.fixedy + self.rect.h
        self.offset = 20
        self.timesx = round(game.resolution[0] / (self.rect.w - self.offset)) + 1
        # noinspection PyArgumentList
        self.image = pygame.Surface((game.resolution[0], self.rect.h), pygame.SRCALPHA).convert_alpha()
        for column in range(int(self.timesx)):
            rect = pygame.Rect(self.rect.w * column - self.offset * (column + 2), 0, self.rect.w, self.rect.h)
            arearect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            if column == self.timesx - 1:
                arearect.w = game.resolution[0] - self.rect.w * column
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
        self.rect = pygame.Rect(self.x, game.resolution[1] - 630 + randint(1, 60), rect.w, rect.h)
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
                    sprite.speed = randint(1, 2) ** 1.15  # todo speed algorithm
                    game.activeclouds.append(sprite)
                game.add_new_renderable(sprite, sample(value, len(value))[0])


class House(pygame.sprite.DirtySprite):
    def __init__(self, sizetype, randtype, people):
        pygame.sprite.DirtySprite.__init__(self)
        self.sizetype = sizetype
        if self.sizetype == 4:
            self.layer = game.cloud.randomize_layers(sizetype)
        elif self.sizetype == 0:
            self.layer = randint(5, 6)
            if len(game.houses[sizetype]) > 1:
                if self.layer == game.houses[sizetype][-1].layer == game.houses[sizetype][-2].layer:
                    self.layer = randint(5, 6)
        else:
            self.layer = 5 - self.sizetype
        self.dirty = 2
        self.visible = True
        self.drawnout = False
        self.peoplemax = people
        self.peoplecurrent = self.peoplemax
        self.taxmax1 = randint(15, 70)
        self.taxmax2 = randint(10, 60)
        self.taxmax3 = randint(20, 80)
        if randtype is None:
            game.bar.calculate_peopletotal(self.peoplemax)
            game.bar.calculate_incometotal(self.peoplemax, self.sizetype)
            # ajutine randtype määramine
            if self.sizetype == 0:  # 1 tüüpi on 4 maja
                self.randtype = randint(0, 3)
            else:
                self.randtype = randint(0, 2)
            if len(game.houses[sizetype]) > 1:  # kiire fix erinevate t22pide genereerimisele
                self.last_randtype = game.houses[sizetype][-1].randtype
                self.last2_randtype = game.houses[sizetype][-2].randtype
                if self.randtype == self.last_randtype == self.last2_randtype:
                    if self.sizetype == 0:  # 1 tüüpi on 4 maja
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
        # self.rect.y = self.y + self.rect.h
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

    def calculate_current_people(self):
        if game.taxes[0] > self.taxmax1 or game.taxes[1] > self.taxmax2 or game.taxes[2] > self.taxmax3:
            self.peoplecurrent -= randint(0, 1) + game.difficulty
        else:
            fillrate = randint(0, 3) - game.difficulty
            if fillrate < 0:
                fillrate = 0
            self.peoplecurrent += fillrate
        if self.peoplecurrent < 0:
            self.peoplecurrent = 0
        elif self.peoplecurrent > self.peoplemax:
            self.peoplecurrent = self.peoplemax
        return self.peoplecurrent

    def calculate_taxmax(self):
        self.taxmax1 = randint(15, 70)
        self.taxmax2 = randint(10, 60)
        self.taxmax3 = randint(20, 80)


class LeftDrawer(pygame.sprite.DirtySprite):
    def __init__(self, used_upgrades):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.visible = False
        self.layer = 10
        self.drawer_visible = True
        self.rect = pygame.Rect(0, 0, 280, game.resolution[1])
        self.startupcounter = 0
        self.tax_buttons = []
        self.upgrade_buttons = []
        self.used_upgrades = used_upgrades
        self.unlocked_upgrades = []
        for name in self.used_upgrades:
            for upgrade in game.upgrades:
                if upgrade[0] == name:
                    game.upgrades.remove(upgrade)
        game.add_new_renderable(self, self.layer)

    @staticmethod
    def initialize_unlock(unlocktype):
        pass
        """if unlocktype == "Metro":
            game.metro = Metro()
        elif unlocktype == "Pipe":
            game.pipe = Pipe()
        elif unlocktype == "Fiber":
            game.fiber = Fiber()
        elif unlocktype == "Power":
            game.power = Power()
        elif unlocktype == "Water":
            game.watersupply = Watersupply()"""

    def process_upgrades(self):
        if self.startupcounter > 0:
            self.startupcounter -= 1
        for button in self.upgrade_buttons:
            if not button.active:
                self.used_upgrades.append(button.name)
                self.upgrade_buttons.remove(button)
            else:
                button.process_location()
        for upgrade in game.upgrades:
            if upgrade[3][0] == "peopletotal":
                if game.bar.peopletotal >= upgrade[3][1]:
                    self.upgrade_buttons.append(UpgradeButton(upgrade[0], len(self.upgrade_buttons)))
                    self.unlocked_upgrades.append(upgrade)
                    break
            elif upgrade[3][0] == "houses":
                houses = 0
                for sizetype in game.houses:
                    houses += len(sizetype)
                if houses >= upgrade[3][1]:
                    self.upgrade_buttons.append(UpgradeButton(upgrade[0], len(self.upgrade_buttons)))
                    self.unlocked_upgrades.append(upgrade)
                    break
            elif upgrade[3][0] == "incometotal":
                if game.bar.income >= upgrade[3][1]:
                    self.upgrade_buttons.append(UpgradeButton(upgrade[0], len(self.upgrade_buttons)))
                    self.unlocked_upgrades.append(upgrade)
                    break
        for upgrade in game.upgrades:
            if upgrade in self.unlocked_upgrades:
                game.upgrades.remove(upgrade)

    def update(self):
        self.process_upgrades()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
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
        for button in self.tax_buttons + self.upgrade_buttons:
            button.visible = self.drawer_visible


class TaxButton(pygame.sprite.DirtySprite):
    def __init__(self, sizetype):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = 10
        self.visible = True
        self.sizetype = sizetype
        self.drawdata = [(255, 255, 255), 14]
        self.image = self.old_image = None
        self.image_regular, rect = game.images.left_button[0]
        self.rect = pygame.Rect(-rect.w, 15 + 45 * self.sizetype, rect.w, rect.h)
        self.image_minus = game.images.left_button[1][0]
        self.image_plus = game.images.left_button[2][0]
        self.taxtxt = game.taxnames[self.sizetype]
        self.minx = 135 - self.rect.w
        self.maxx = 10
        self.clickable_rects = [pygame.Rect(self.minx + 206, self.rect.y + 7, 25, 20),
                                pygame.Rect(self.minx + 234, self.rect.y + 7, 25, 20)]
        self.active = True
        self.animatein = True
        self.animateout = False
        self.animatecounter = 0
        self.name_obj = RenderObject(self.layer + 1, self.visible, True, self.taxtxt, self.rect.topleft,
                                     (10, 7), (132, 20), self.drawdata, False)
        self.tax_obj = RenderObject(self.layer + 1, self.visible, True, str(game.taxes[self.sizetype]) + "%",
                                    self.rect.topleft, (149, 7), (52, 20), self.drawdata, False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.name_obj.process_update(self.visible, self.taxtxt, self.rect.topleft)
        self.tax_obj.process_update(self.visible, str(game.taxes[self.sizetype]) + "%", self.rect.topleft)
        if self.animatein:
            if self.rect.x < self.minx - 20:
                self.dirty = 1
                self.rect.x += 4
            else:
                self.rect.x = self.minx
                self.animatein = False
                self.dirty = 1
        is_highlighted = self.mouse_hover_check()
        if is_highlighted == "minus":
            self.image = self.image_minus
        elif is_highlighted == "plus":
            self.image = self.image_plus
        else:
            self.image = self.image_regular
        if self.old_image != self.image:
            self.old_image = self.image
            self.dirty = 1

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
                    return "minus"
                else:
                    return "plus"

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
    def __init__(self, name, index):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = 10
        if game.left_drawer.drawer_visible:
            self.visible = True
        else:
            self.visible = False
        self.active = True
        self.name = name
        self.index = index
        self.drawdata = [(255, 255, 255), 14, " €", " €/s"]
        self.image = self.old_image = self.rect = None
        self.image_available, rect = game.images.upgrade_button[0]
        self.image_unavailable = game.images.upgrade_button[1][0]
        self.image_highlighted = game.images.upgrade_button[2][0]
        self.miny = 155 + 75 * index
        self.rect = pygame.Rect(-rect.w, self.miny, rect.w, rect.h)
        self.minx = 20 - self.rect.w
        self.maxx = 10
        self.animatein = True
        self.animatemove = False
        self.animateout = False
        self.animatecounter = 150
        for item in game.upgrades:
            if item[0] == self.name:
                multiplier = game.difficulty
                if multiplier == 0:
                    multiplier = 0.5
                self.cost = int(item[1] * multiplier)
                self.rewardtype = item[2][0]
                if self.rewardtype == "income":
                    self.end = self.drawdata[2]
                else:
                    self.end = 0
                self.reward = item[2][1]
        self.name_obj = RenderObject(self.layer + 1, self.visible, True, self.name, self.rect.topleft,
                                     (10, 7), (192, 20), self.drawdata, False)
        self.cost_obj = RenderObject(self.layer + 1, self.visible, True, self.cost, self.rect.topleft,
                                     (12, 35), (98, 20), self.drawdata, self.drawdata[2])
        self.reward_obj = RenderObject(self.layer + 1, self.visible, True, self.reward, self.rect.topleft,
                                       (117, 35), (87, 20), self.drawdata, self.drawdata[3])
        game.add_new_renderable(self, self.layer)
        self.update()

    def update(self):
        self.name_obj.process_update(self.visible, self.name, self.rect.topleft)
        self.cost_obj.process_update(self.visible, self.cost, self.rect.topleft)
        self.reward_obj.process_update(self.visible, self.reward, self.rect.topleft)
        if self.animatemove:
            self.dirty = 1
            if self.rect.y > self.miny:
                self.rect.y -= 10
            else:
                self.animatemove = False
        elif self.animatein:
            self.dirty = 1
            if game.left_drawer.startupcounter > 0:
                self.startcounter -= 1
                if self.rect.x < self.minx:
                    self.rect.x += 2
                else:
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
                self.active = False
                self.kill()
        if game.bar.money >= self.cost:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image = self.image_highlighted
            else:
                self.image = self.image_available
        else:
            breakpoint = self.rect.w / 100 * game.bar.calculate_percentage(self.cost)
            # noinspection PyArgumentList
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
            self.image.blit(self.image_available, pygame.Rect(0, 0, self.rect.w + breakpoint, self.rect.h),
                            pygame.Rect(0, 0, breakpoint, self.rect.h))
            self.image.blit(self.image_unavailable, pygame.Rect(breakpoint, 0, self.rect.w, self.rect.h),
                            pygame.Rect(breakpoint, 0, self.rect.w, self.rect.h))
        if self.old_image != self.image:
            self.old_image = self.image
            self.dirty = 1

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

    def process_location(self):
        for upgrade in game.left_drawer.upgrade_buttons:
            if upgrade.name == self.name:
                if game.left_drawer.upgrade_buttons.index(upgrade) < self.index:
                    self.index -= 1
                    self.miny = 155 + 75 * self.index
                    self.animatemove = True

    def mouse_click_check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if game.bar.money >= self.cost:
                game.bar.money -= self.cost
                self.process_rewards()
                self.animateout = True
                self.animatecounter = 0
                return True

    def process_rewards(self):
        if self.rewardtype == "income":
            game.bar.incomereward += self.reward
        elif self.rewardtype == "unlock":
            game.left_drawer.initialize_unlock(self.reward)


class RightDrawer(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.visible = False
        self.drawer_visible = True
        self.layer = 10
        self.x = game.resolution[0] - 220
        self.rect = pygame.Rect(self.x, 0, game.resolution[0] - self.x, game.resolution[1])
        self.right_buttons = []
        game.add_new_renderable(self, self.layer)

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for button in self.right_buttons:
                button.slide(-5)
        else:
            for button in self.right_buttons:
                button.slide(5)

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
        self.visible = self.global_visible = False
        self.sizetype = sizetype
        self.old_image = self.old_x = None
        self.drawdata = [(255, 255, 255), 14, " €"]
        self.image_available, rect = game.images.right_button[0]
        self.image_available_highlighted = game.images.right_button[1][0]
        self.image_unavailable = game.images.right_button[2][0]
        self.logo = game.images.right_button_logos[self.sizetype][0]
        self.name = game.right_button_names[self.sizetype]
        self.amount = game.right_button_amounts[self.sizetype]
        if self.amount > 0:
            self.price = game.right_button_prices[self.sizetype]
        else:
            self.price = game.right_button_prices_fixed[self.sizetype]
        self.people = game.houses_properties[self.sizetype][0]
        self.image = self.image_available
        self.rect = pygame.Rect(game.resolution[0], 15 + 100 * self.sizetype, rect.w, rect.h)
        self.minx = game.resolution[0] - 220
        self.maxx = game.resolution[0] - 20
        self.animatein = True
        self.logo_obj = RenderObject(self.layer + 1, self.visible, True, self.logo, self.rect.topleft,
                                     (7, 7), (47, 48), self.drawdata, False)
        self.amount_obj = RenderObject(self.layer + 1, self.visible, True, self.amount, self.rect.topleft,
                                       (7, 62), (47, 19), self.drawdata, False)
        self.name_obj = RenderObject(self.layer + 1, self.visible, True, self.name, self.rect.topleft,
                                     (62, 7), (132, 19), self.drawdata, False)
        self.people_obj = RenderObject(self.layer + 1, self.visible, True, self.people, self.rect.topleft,
                                       (77, 35), (44, 19), self.drawdata, False)
        self.peopletotal_obj = RenderObject(self.layer + 1, self.visible, True, self.calculate_peopletotal(),
                                            self.rect.topleft, (132, 34), (63, 19), self.drawdata, False)
        self.price_obj = RenderObject(self.layer + 1, self.visible, True, self.price, self.rect.topleft,
                                      (62, 62), (132, 19), self.drawdata, self.drawdata[2])
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.logo_obj.process_update(self.visible, self.logo, self.rect.topleft)
        self.amount_obj.process_update(self.visible, self.amount, self.rect.topleft)
        self.name_obj.process_update(self.visible, self.name, self.rect.topleft)
        self.people_obj.process_update(self.visible, self.people, self.rect.topleft)
        self.peopletotal_obj.process_update(self.visible, self.calculate_peopletotal(), self.rect.topleft)
        self.price_obj.process_update(self.visible, self.price, self.rect.topleft)
        if self.visible:
            if self.animatein:
                self.dirty = 1
                if self.rect.x > self.maxx:
                    self.rect.x -= 2
                else:
                    self.rect.x = self.maxx
                    self.animatein = False
            if game.bar.money >= self.price:
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.image = self.image_available_highlighted
                else:
                    self.image = self.image_available
            else:
                breakpoint = self.rect.w / 100 * game.bar.calculate_percentage(self.price)
                # noinspection PyArgumentList
                self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
                self.image.blit(self.image_available, pygame.Rect(0, 0, self.rect.w + breakpoint, self.rect.h),
                                pygame.Rect(0, 0, breakpoint, self.rect.h))
                self.image.blit(self.image_unavailable, pygame.Rect(breakpoint, 0, self.rect.w, self.rect.h),
                                pygame.Rect(breakpoint, 0, self.rect.w, self.rect.h))
            if self.old_image != self.image:
                self.old_image = self.image
                self.dirty = 1
        elif not self.global_visible:
            # if game.bar.peopletotal >= game.houses_properties[self.sizetype][2]:
            if game.bar.people >= game.houses_properties[self.sizetype][2]:
                self.global_visible = True
                if game.right_drawer.drawer_visible:
                    self.visible = True

    def calculate_peopletotal(self):
        people = 0
        if len(game.houses) >= self.sizetype:
            for house in game.houses[self.sizetype]:
                people += house.peoplecurrent
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
        self.names = ["new game", "continue", "easy", "normal", "insane"]
        self.xmod = [-20, 20, -92, 0, 92]
        self.ymod = [-65, -65, 15, 15, 15]
        self.sizetype = [0, 0, 2, 2, 2]
        self.buttons = []
        self.is_highlighted_button = game.difficulty + 2
        for i in range(5):
            self.buttons.append(MenuButton((self.xmod[i], game.resolution[1] / 2 + self.ymod[i]), self.sizetype[i],
                                           i, self.names[i]))
        self.logo, rect = game.images.menu[0][0]
        self.rect = game.screen.get_rect()
        # noinspection PyArgumentList
        self.image = pygame.Surface(game.resolution, pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 89))
        self.image.blit(self.logo, ((game.resolution[0] - rect.w) / 2, game.resolution[1] / 2 - 275))
        game.toggle_interactables()
        game.add_new_renderable(self, self.layer)

    def update(self):
        pass

    def toggle(self, full):  # todo toggle function which toggles blur for all objects
        if self.visible:
            self.visible = False
        else:
            self.visible = True
        for button in self.buttons:
            button.toggle()
        if full:
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
                                     (0, 0), (rect.w, rect.h), self.drawdata, 0)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.name_obj.process_update(self.visible, self.name, (self.rect.x, self.rect.y - 3))
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
                    # game.initialize_game("new")
                    game.menu_running = False
                elif self.stype == 1:
                    game.menu.toggle(True)
                    if game.bar_amounts[0] == 0 and game.bar_amounts[0] == 0:
                        return False
                    else:
                        # game.initialize_game("load")
                        print("yes")
                        game.menu_running = False
                else:
                    game.difficulty = self.stype - 2
                    game.menu.is_highlighted_button = self.stype
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
        self.layer = 18
        # noinspection PyArgumentList
        self.image = pygame.Surface(game.resolution, pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 127))
        self.images = [game.images.quick_menu[0][0], game.images.quick_menu[1][0], game.images.quick_menu[2][0],
                       game.images.quick_menu[3][0]]
        self.rect = game.screen.get_rect()
        rect = game.images.quick_menu[0][1]
        self.innerxy = [(self.rect.w - rect.w) / 2, (self.rect.h - rect.h) / 2]
        self.rects = [pygame.Rect(self.innerxy[0] + 14, self.innerxy[1] + 9, 267, 42),
                      pygame.Rect(self.innerxy[0] + 14, self.innerxy[1] + 62, 267, 42),
                      pygame.Rect(self.innerxy[0] + 14, self.innerxy[1] + 115, 267, 42)]
        self.quick_menu_obj = RenderObject(self.layer + 1, self.visible, True, self.images[0], self.innerxy,
                                           (0, 0), (298, 170), 0, 0)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.quick_menu_obj.process_update(self.visible, self.mouse_hover_check(), self.innerxy)

    def mouse_hover_check(self):
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                return self.images[self.rects.index(rect) + 1]
        return self.images[0]

    def mouse_click_check(self):
        if self.visible:
            for rect in self.rects:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    if rect == self.rects[0]:
                        game.sounds.toggle_mute()
                    elif rect == self.rects[1]:
                        self.visible = False
                        game.menu.toggle(False)
                    elif rect == self.rects[2]:
                        game.running = False
                    return True

    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True
        game.toggle_interactables()


class Bar(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.visible = True
        self.layer = 10
        self.animatein = True
        self.image, self.rect = game.images.bar
        self.rect.x = (game.resolution[0] - self.rect.w) / 2 + 25
        self.rect.y = -self.rect.h
        self.maxy = 6

        self.people = 0
        self.peopletotal = 0
        self.money = 99999999999999
        self.income = 0
        self.incometotal = 0
        self.incomereward = 0

        self.house_multiplier = 1.15572735

        self.objxy = ([26, 204, 469], 7)
        self.objwh = ([170, 249, 239], 21.621)
        self.drawdata = [(255, 255, 255), 14, [" €", " €/s"]]

        self.peoplecounter = RenderObject(self.layer + 1, self.visible, True, self.people, self.rect.topleft,
                                          (self.objxy[0][0], self.objxy[1]), (self.objwh[0][0], self.objwh[1]),
                                          self.drawdata, False)
        self.moneycounter = RenderObject(self.layer + 1, self.visible, True, self.money, self.rect.topleft,
                                         (self.objxy[0][1], self.objxy[1]), (self.objwh[0][1], self.objwh[1]),
                                         self.drawdata, self.drawdata[2][0])
        self.incomecounter = RenderObject(self.layer + 1, self.visible, True, self.money, self.rect.topleft,
                                          (self.objxy[0][2], self.objxy[1]), (self.objwh[0][2], self.objwh[1]),
                                          self.drawdata, self.drawdata[2][1])
        self.fpscounter = RenderObject(self.layer + 1, self.visible, True, game.clock.get_fps(), self.rect.topleft,
                                       (670, 8), (44, 22), self.drawdata, False)
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.people += 10
        self.money += 10
        self.income += 1
        self.peoplecounter.process_update(self.visible, self.people, self.rect.topleft)
        self.moneycounter.process_update(self.visible, self.money, self.rect.topleft)
        self.incomecounter.process_update(self.visible, self.income, self.rect.topleft)
        self.fpscounter.process_update(self.visible, game.clock.get_fps(), self.rect.topleft)
        if self.animatein:
            self.dirty = 1
            if self.rect.y < self.maxy:
                self.rect.y += 2
            else:
                self.rect.y = self.maxy
                self.animatein = False

    def calculate_percentage(self, price):
        if self.money == 0:
            return 0
        return self.money / price * 100

    def calculate_incometotal(self, currentpeople, currentsizetype):
        self.incometotal = currentpeople * game.bar.house_multiplier * game.houses_properties[currentsizetype][1]
        for sizetype in game.houses:
            for house in sizetype:
                self.incometotal += \
                    house.peoplemax * game.bar.house_multiplier * game.houses_properties[house.sizetype][1]

    def calculate_peopletotal(self, currentpeople):
        self.peopletotal = currentpeople
        for sizetype in game.houses:
            for house in sizetype:
                self.peopletotal += house.peoplemax

    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True


class RenderObject(pygame.sprite.DirtySprite):
    def __init__(self, layer, visible, middle, obj, main_obj_xy, inner_relative_xy, inner_obj_wh, drawdata, end):
        # layer, nähtavus, keskel, tekst/pilt,
        # suure pildi xy, kasti xy pildi suhtes, kasti wh, teksti omadused, teksti lõpp
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = layer
        self.visible = self.global_visible = visible
        self.middle = middle
        self.end = end
        self.drawdata = drawdata
        if drawdata != 0:
            self.txt_font = pygame.font.SysFont("centurygothic", drawdata[1], True)
        self.image = self.rect = self.new_obj = self.old_obj = self.main_obj_xy = self.old_main_obj_xy = \
            self.innerrect = None
        self.inner_relative_xy = inner_relative_xy
        self.inner_obj_wh = inner_obj_wh
        self.process_update(visible, obj, main_obj_xy)
        self.update()
        game.add_new_renderable(self, self.layer)

    def process_string(self, obj):
        self.image = self.txt_font.render(obj, True, self.drawdata[0])

    def process_integer(self, obj):
        obj = str(format(obj, ",d"))
        if self.end:
            obj += self.end
        self.process_string(obj)

    def process_float(self, obj):
        self.process_integer(round(obj))

    def process_image(self, obj):
        self.image = obj

    def process_update(self, visible, obj, main_obj_xy):
        if self.global_visible != visible:
            self.global_visible = self.visible = visible
        self.new_obj = obj
        self.main_obj_xy = main_obj_xy

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
                if isinstance(self.new_obj, str):
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


if __name__ == '__main__':
    game = Game()
    game.run()
