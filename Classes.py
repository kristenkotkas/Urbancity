import pygame
import os.path
from random import randint
main_dir = os.path.split(os.path.abspath(__file__))[0]


class Game:
    def __init__(self):
        self.fps_cap = 60
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1600, 900))
        self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.running = True
        self.images = self.sounds = self.background = self.cursor = self.cloud = self.metro = self.pipe = self.fiber = \
            self.power = self.watersupply = None
        self.allsprites = pygame.sprite.LayeredDirty()

    def initialize_all(self, game):
        self.images = Images()
        self.sounds = Sounds()
        self.background = Background(game)
        self.cursor = Cursor(game, 10)
        self.cloud = Cloud(game, 0)
        # self.metro = Metro(game)
        self.pipe = Pipe(game, 1)
        self.fiber = Fiber(game, 2)
        # self.power = Power(game)
        # self.watersupply = Watersupply(game)

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
    def __init__(self, game, layer):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = layer
        self.image, self.rect = game.images.cursor
        game.add_new_renderable(self, self.layer)

    def update(self):
        self.rect.topleft = pygame.mouse.get_pos()


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
    def __init__(self, game, layer):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = layer
        self.image, self.rect = game.images.misc[2]
        self.rect.x = -10
        self.rect.y = game.resolution[1] - self.rect.h + 30
        self.drawnout = False
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


class Fiber(pygame.sprite.DirtySprite):
    def __init__(self, game, layer):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 1
        self.layer = layer
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
        game.add_new_renderable(self, self.layer)


class Watersupply:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.misc[5]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = 0
        self.y = game.resolution[1] - self.h + 5
        self.timesx = game.resolution[0] // self.w
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.areaendrect = pygame.Rect(0, 0, game.resolution[0] - self.w * self.timesx + 5 * (self.timesx + 1), self.h)

    def draw(self):
        for column in range(int(self.timesx)):
            self.rect = pygame.Rect(self.w * column - 5 * (column + 1), self.y, self.w, self.h)
            self.surface.blit(self.image, self.rect)
        self.rect = pygame.Rect(self.w * self.timesx - 5 * (self.timesx + 1), self.y, self.w, self.h)
        self.surface.blit(self.image, self.rect, self.areaendrect)


class Power:
    def __init__(self, game):
        self.surface = game.screen
        self.image = game.images.misc[4]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = 0
        self.fixedy = game.resolution[1] - self.h - game.background.groundsize + 14
        self.y = self.fixedy + self.h
        self.offset = 20
        self.timesx = game.resolution[0] // (self.w - self.offset)
        self.drawnout = False
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.arearect = pygame.Rect(0, self.h, self.w, self.h)
        self.areaendrect = \
            pygame.Rect(0, self.h, game.resolution[0] - self.w * self.timesx + self.offset * (self.timesx + 2), self.h)

    def draw(self):
        if not self.drawnout:
            if self.arearect.y > 0:
                self.arearect.y -= 5
                self.areaendrect.y -= 5
                self.y -= 5
            else:
                self.drawnout = True
                self.y = self.fixedy
        for column in range(int(self.timesx)):
            self.rect = pygame.Rect(self.w * column - self.offset * (column + 2), self.y, self.w, self.h)
            self.surface.blit(self.image, self.rect, self.arearect)
        self.rect = pygame.Rect(self.w * self.timesx - self.offset * (self.timesx + 2), self.y, self.w, self.h)
        self.surface.blit(self.image, self.rect, self.areaendrect)


class Cloud(pygame.sprite.DirtySprite):
    def __init__(self, game, layer):
        pygame.sprite.DirtySprite.__init__(self)
        self.dirty = 2
        self.layer = layer
        self.image, self.rect = game.images.misc[0]
        self.x = self.minx = -self.rect.w
        self.maxx = game.resolution[0]
        self.rect.y = game.resolution[1] - 660
        game.add_new_renderable(self, self.layer)

    def update(self):
        if self.rect.x < self.maxx:
            self.rect.x += 1
        else:
            self.rect.x = self.minx
