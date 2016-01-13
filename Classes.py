import pygame
import os.path
from random import randint, sample
main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
    def __init__(self):
        self.fps_cap = 120
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1366, 768))
        self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.running = True
        self.menu_running = True
        self.difficulty = 1

        self.tax_buttons = []
        self.right_buttons = []
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

        self.houses_types = [([-15, [190, 125, 240, 125]], [432, 347, 427, 347]),
                             ([5, [90, 96, 242]], [340, 335, 328]),
                             ([-30, [103, 96, 170]], [255, 255, 250]),
                             ([-10, [128, 180, 223]], [115, 130, 130]),
                             ([-40, [170, 135, 150]], [73, 59, 41])]

        self.houses_properties = [
            (200, 0.2, 0), (900, 0.4, 600), (2560, 1, 3500), (7200, 1.8, 10800), (13500, 6, 27000)]
        self.right_button_prices_fixed = [750, 9000, 40000, 486000, 2531250]

        self.images = self.sounds = self.background = self.cursor = self.cloud = self.metro = self.pipe = self.fiber = \
            self.power = self.watersupply = self.bar = self.right_drawer = self.left_drawer = None
        self.allsprites = pygame.sprite.LayeredDirty()

    def initialize_all(self, game):
        self.images = Images()
        self.sounds = Sounds()
        self.background = Background(game)
        self.cursor = Cursor(game)
        self.cloud = Cloud(game)
        # self.metro = Metro(game)
        self.fiber = Fiber(game)
        self.watersupply = Watersupply(game)
        self.pipe = Pipe(game)
        self.power = Power(game)
        self.left_drawer = LeftDrawer(game)
        self.right_drawer = RightDrawer(game)
        self.bar = Bar(game)
        for sizetype in range(5):
            self.right_buttons.append(RightButton(game, sizetype))

    def add_new_renderable(self, obj, layer):
        self.allsprites.add(obj, layer = layer)


class Images:
    def __init__(self):
        self.background = Images.load_image("Background_plain.png")
        self.cursor = Images.load_image("Cursor.png")
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
                     Images.load_image("Pipe.png"), Images.load_image("Google_Fiber.png"),
                     Images.load_image("Electricity.png"), Images.load_image("Water.png")]
        self.houses = [
            [Images.load_image("House_11.png"), Images.load_image("House_12.png"), Images.load_image("House_13.png"),
             Images.load_image("House_14.png")],
            [Images.load_image("House_21.png"), Images.load_image("House_22.png"), Images.load_image("House_23.png")],
            [Images.load_image("House_31.png"), Images.load_image("House_32.png"), Images.load_image("House_33.png")],
            [Images.load_image("House_41.png"), Images.load_image("House_42.png"), Images.load_image("House_43.png")],
            [Images.load_image("House_51.png"), Images.load_image("House_52.png"), Images.load_image("House_53.png")]]
        self.metro = [Images.load_image("Metro.png"), Images.load_image("Metro_train.png")]
        self.menu = [[Images.load_image("Urbancity_logo.png")],
                     [Images.load_image("Menu_big_button.png"), Images.load_image("Menu_big_button_hover.png"),
                      Images.load_image("Menu_small_button.png"), Images.load_image("Menu_small_button_hover.png")]]

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
    def load_sound(file, soundtype):
        file = os.path.join(main_dir, 'data\\test_helid', file)
        if soundtype == "music":
            pygame.mixer.music.load(file)
            # pygame.mixer.music.play(-1)
        else:
            try:
                loaded_sound = pygame.mixer.Sound(file)
            except pygame.error:
                raise SystemExit("Could not load sound " + file + ", " + pygame.get_error())
            return loaded_sound


class Background:
    def __init__(self, game):
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
    def __init__(self, game):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = 30
        self.image, self.rect = game.images.cursor
        game.add_new_renderable(self, self.layer)

        # todo fix
        # ei uuenda hiir piisavalt kiiresti?, või on mingi värk tausta ülekirjutamisega

    def update(self, game):
        pos = pygame.mouse.get_pos()
        if self.rect.topleft != pos:
            self.rect.topleft = pos
            self.dirty = 1


class Metro:
    def __init__(self, game):
        self.surface = game.screen
        self.image_metro = game.images.metro[0]
        self.image_train = game.images.metro[1]
        self.metrow = self.image_metro.get_rect().w
        self.metroh = self.image_metro.get_rect().h
        self.metrox = (game.resolution[0] - self.metrow) / 2
        self.metroy = game.resolution[1] - 111
        self.metrorect = pygame.Rect(self.metrox, self.metroy + self.metroh, self.metrow, self.metroh)
        self.trainx = self.metrox
        self.trainy = self.metroy + 50
        self.trainw = self.image_train.get_rect().w - 2
        self.trainh = self.image_train.get_rect().h
        self.trainstop = self.metrox + 20
        self.trainrect = pygame.Rect(self.metrox, self.metroy + 50, self.trainw, self.trainh)
        self.arearect = pygame.Rect(self.trainw, 0, self.trainw, self.trainh)
        self.speed = 4
        self.time_from_beginning = 0
        self.drawnoutarea = pygame.Rect(0, self.metroh, self.metrow, self.metroh)
        self.drawnout = False
        self.waiting = False
        self.trainstopwaiting = True
        self.terroristevent = False
        self.terroristcounter = 0

    def draw(self, game):
        self.draw_metro_background()
        if self.drawnout:
            self.update_metro(game)
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

    def update_metro(self, game):
        if self.terroristevent:
            if self.terroristcounter == 0:
                self.metrow -= 15
                self.speed = 18
            elif self.terroristcounter == 450:
                game.news.present("metro")
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


class Pipe(pygame.sprite.DirtySprite):
    def __init__(self, game):
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

    def update(self, game):
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
    def __init__(self, game):
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

    def update(self, game):
        if not self.drawnout:
            if self.source_rect.w < self.rect.w:
                self.source_rect.w += 5
            else:
                self.drawnout = True
                self.source_rect.w = self.rect.w
                self.dirty = 1


class Watersupply(pygame.sprite.DirtySprite):
    def __init__(self, game):
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

    def update(self, game):
        if not self.drawnout:
            if self.source_rect.w < self.rect.w:
                self.source_rect.w += 5
            else:
                self.drawnout = True
                self.source_rect.w = self.rect.w
                self.dirty = 1


class Power(pygame.sprite.DirtySprite):
    def __init__(self, game):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 6
        self.drawnout = False
        self.surface, self.rect = game.images.misc[4]
        self.fixedy = game.resolution[1] - self.rect.h - game.background.rect.h + 14
        self.rect.y = self.fixedy + self.rect.h
        self.offset = 20
        self.timesx = game.resolution[0] // (self.rect.w - self.offset) + 1
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

    def update(self, game):
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
    def __init__(self, game):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 1
        self.image, self.rect = game.images.misc[0]
        self.x = self.minx = self.rect.x = -self.rect.w
        self.maxx = game.resolution[0]
        self.rect.y = game.resolution[1] - 660
        game.add_new_renderable(self, self.layer)

    def update(self, game):
        if self.rect.x < self.maxx:
            self.rect.x += 1
        else:
            self.rect.x = self.minx
            self.randomize_layers(game, [0, 1])

    def randomize_layers(self, game, value):
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
                if sprite == self:
                    game.add_new_renderable(sprite, value[1])
                else:
                    game.add_new_renderable(sprite, sample(value, len(value))[0])


class House(pygame.sprite.DirtySprite):
    def __init__(self, game, sizetype, randtype, people):
        pygame.sprite.DirtySprite.__init__(self)
        self.sizetype = sizetype
        if self.sizetype == 4:
            self.layer = game.cloud.randomize_layers(game, sizetype)
        elif self.sizetype == 0:
            self.layer = randint(5, 6)
        else:
            self.layer = 5 - self.sizetype
        self.dirty = 2
        self.visible = 1
        self.drawnout = False
        self.peoplemax = people
        self.peoplecurrent = self.peoplemax
        self.taxmax1 = randint(15, 70)
        self.taxmax2 = randint(10, 60)
        self.taxmax3 = randint(20, 80)
        if randtype is None:
            game.bar.calculate_peopletotal(game, self.peoplemax)
            game.bar.calculate_incometotal(game, self.peoplemax, self.sizetype)
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
            self.visible = 0
            self.dirty = 0
        self.rect = pygame.Rect(self.x, self.y + rect.h, rect.w, rect.h)
        self.source_rect = pygame.Rect(0, self.rect.h, self.rect.w, self.rect.h)
        game.add_new_renderable(self, self.layer)

    def update(self, game):
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

    def calculate_current_people(self, game):
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
    def __init__(self, game):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.visible = 0
        self.layer = 10
        self.rect = pygame.Rect(0, 0, 280, game.resolution[1])
        game.add_new_renderable(self, self.layer)

    @staticmethod
    def process_upgrade_buttons(game):
        for button in game.upgrade_buttons:
            if not button.active:
                game.usedupgrades.append(button.name)
                game.upgrade_buttons.remove(button)
            else:
                button.process_location(game)

    def update(self, game):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            """for button in game.tax_buttons + game.upgrade_buttons:
                if button.animatecounter > 0:
                    button.animatein = False
                if not button.animateout and not button.animatein:
                    if button.x < button.maxx:
                        button.x += 20
        else:
            for button in game.tax_buttons + game.upgrade_buttons:
                if not button.animateout and not button.animatein:
                    if button.x > button.minx:
                        button.x -= 20"""


class RightDrawer(pygame.sprite.DirtySprite):
    def __init__(self, game):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.visible = 0
        self.layer = 10
        self.x = game.resolution[0] - 220
        self.rect = pygame.Rect(self.x, 0, game.resolution[0] - self.x, game.resolution[1])
        game.add_new_renderable(self, self.layer)

    def update(self, game):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            for button in game.right_buttons:
                button.slide(-5)
        else:
            for button in game.right_buttons:
                button.slide(5)


class RightButton(pygame.sprite.DirtySprite):
    def __init__(self, game, sizetype):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 0
        self.layer = 11
        self.sizetype = sizetype
        self.image = self.old_image = self.old_x = None
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
        self.rect = pygame.Rect(game.resolution[0], 15 + 100 * self.sizetype, rect.w, rect.h)
        self.minx = game.resolution[0] - 220
        self.maxx = game.resolution[0] - 20
        self.hidden = False
        self.animatein = True
        self.logo_obj = RenderObject(game, True, self.logo, self.rect.topleft, (7, 7), (47, 48), self.drawdata, False)
        self.amount_obj = RenderObject(game, True, self.amount, self.rect.topleft,
                                       (7, 62), (47, 19), self.drawdata, False)
        self.name_obj = RenderObject(game, True, self.name, self.rect.topleft, (62, 7), (132, 19), self.drawdata, False)
        self.people_obj = RenderObject(game, True, self.people, self.rect.topleft,
                                       (77, 35), (44, 19), self.drawdata, False)
        self.peopletotal_obj = RenderObject(game, True, self.calculate_peopletotal(game), self.rect.topleft,
                                            (132, 34), (63, 19), self.drawdata, False)
        self.price_obj = RenderObject(game, True, self.price, self.rect.topleft,
                                      (62, 62), (132, 19), self.drawdata, self.drawdata[2])
        game.add_new_renderable(self, self.layer)

    def update(self, game):
        self.logo_obj.process_update(self.logo, self.rect.topleft)
        self.amount_obj.process_update(self.amount, self.rect.topleft)
        self.name_obj.process_update(self.name, self.rect.topleft)
        self.people_obj.process_update(self.people, self.rect.topleft)
        self.peopletotal_obj.process_update(self.calculate_peopletotal(game), self.rect.topleft)
        self.price_obj.process_update(self.price, self.rect.topleft)
        if not self.hidden:
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
        else:
            # if game.bar.peopletotal >= game.houses_properties[self.sizetype][2]:
            if game.bar.people >= game.houses_properties[self.sizetype][2]:
                self.hidden = False

    def calculate_peopletotal(self, game):
        people = 0
        if len(game.houses) >= self.sizetype:
            for house in game.houses[self.sizetype]:
                people += house.peoplecurrent
        return people

    def mouse_click_check(self, game):
        if not self.hidden:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if game.bar.money >= self.price:
                    # game.sounds.click.play()
                    game.bar.money -= self.price
                    self.amount += 1
                    self.price = game.right_button_prices_fixed[
                                     self.sizetype] * game.bar.house_multiplier ** self.amount
                    game.houses[self.sizetype].append(
                        House(game, self.sizetype, None, game.houses_properties[self.sizetype][0]))

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


class Bar(pygame.sprite.DirtySprite):
    def __init__(self, game):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = 10
        self.image, self.rect = game.images.bar
        self.rect.x = (game.resolution[0] - self.rect.w) / 2 + 25
        self.rect.y = -self.rect.h
        self.maxy = 6

        self.people = 0
        self.peopletotal = 0
        self.money = 99999999999999
        self.income = 0
        self.incometotal = 0

        self.house_multiplier = 1.15572735

        self.objxy = ([26, 204, 469], 7)
        self.objwh = ([170, 249, 239], 21.621)
        self.drawdata = [(255, 255, 255), 14, [" €", " €/s"]]

        self.peoplecounter = RenderObject(game, True, self.people, self.rect.topleft, (self.objxy[0][0], self.objxy[1]),
                                          (self.objwh[0][0], self.objwh[1]), self.drawdata, False)
        self.moneycounter = RenderObject(game, True, self.money, self.rect.topleft, (self.objxy[0][1], self.objxy[1]),
                                         (self.objwh[0][1], self.objwh[1]), self.drawdata, self.drawdata[2][0])
        self.incomecounter = RenderObject(game, True, self.money, self.rect.topleft, (self.objxy[0][2], self.objxy[1]),
                                          (self.objwh[0][2], self.objwh[1]), self.drawdata, self.drawdata[2][1])
        game.add_new_renderable(self, self.layer)

    def update(self, game):
        self.people += 10
        self.money += 10
        self.income += 1
        self.peoplecounter.process_update(self.people, self.rect.topleft)
        self.moneycounter.process_update(self.money, self.rect.topleft)
        self.incomecounter.process_update(self.income, self.rect.topleft)
        if self.rect.y < self.maxy:
            self.rect.y += 2
        else:
            self.rect.y = self.maxy
            self.dirty = 1

    def calculate_percentage(self, price):
        if self.money == 0:
            return 0
        return self.money / price * 100

    def calculate_incometotal(self, game, currentpeople, currentsizetype):
        self.incometotal = currentpeople * game.bar.house_multiplier * game.houses_properties[currentsizetype][1]
        for sizetype in game.houses:
            for house in sizetype:
                self.incometotal += \
                    house.peoplemax * game.bar.house_multiplier * game.houses_properties[house.sizetype][1]

    def calculate_peopletotal(self, game, currentpeople):
        self.peopletotal = currentpeople
        for sizetype in game.houses:
            for house in sizetype:
                self.peopletotal += house.peoplemax


class RenderObject(pygame.sprite.DirtySprite):  # todo add hidden var?
    def __init__(self, game, middle, obj, main_obj_xy, inner_relative_xy, inner_obj_wh, drawdata, end):
        # "game obj", keskel, tekst/pilt, suure pildi xy, kasti xy pildi suhtes, kasti wh, teksti omadused, teksti lõpp
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = 15
        self.middle = middle
        self.end = end
        self.drawdata = drawdata
        self.txt_font = pygame.font.SysFont("centurygothic", drawdata[1], True)
        self.image = self.rect = self.new_obj = self.old_obj = self.main_obj_xy = self.old_main_obj_xy = \
            self.innerrect = None
        self.inner_relative_xy = inner_relative_xy
        self.inner_obj_wh = inner_obj_wh
        self.process_update(obj, main_obj_xy)
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

    def process_update(self, obj, main_obj_xy):
        self.new_obj = obj
        self.main_obj_xy = main_obj_xy

    def update(self, game):
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
