import pygame
import Methods
import os.path
import shelve
from random import randint
main_dir = os.path.split(os.path.abspath(__file__))[0]


class Andmed:
    def __init__(self):
        self.fps_cap = 60
        self.resolution = (1280, 720)
        self.screen = pygame.display.set_mode(self.resolution)
        # self.screen = pygame.Surface(self.resolution)
        self.running = True
        self.tick = 0
        self.vasak_nupud = []
        self.parem_nupud = []
        self.majad = [[], [], [], [], []]
        self.majad_states = [[], [], [], [], []]
        self.maja_multiplier = 1.15
        """ majad_types struktuur [([a, [b, c, d]], [e, f, g], h, i, j, k), (sama), (sama), (sama), (sama)]
        sizetype(randtype[xbase, randtype[x laius/+vahe]], randtype[y], people, per people modifier, start price,
                                                                                                            minpeople)
        a = xbase ehk x kaugus vasakust ekraani servast
        b,c,d = (erinevad random tüübid) = randtype[x laius/+vahe] ehk maja laius + vahe järgmise majaga
        e,f,g = (erinevad random tüübid) = randtype[y] ehk maja ülemine serv (pilt kuvatakse xy alla paremale)
        h = people ehk maja elanike arv
        i = per people modifier ehk palju raha saab ühe elaniku kohta selles tüübis
        j = start price ehk selle maja tüübi alghind
        k = minpeople ehk vajalik rahvaarv, et seda maja tüübi nuppu kuvataks
        """
        self.majad_types = [([-15, [190, 125, 240]], [432, 347, 427], 10, 1, 1500, 0),
                            ([5, [90, 96, 0]], [340, 335, 0], 30, 3, 18000, 40),
                            ([-30, [103, 96, 0]], [255, 255, 0], 80, 8, 80000, 160),
                            ([-10, [130, 0, 0]], [115, 0, 0], 180, 18, 972000, 540),  # todo paika timmida kõik
                            ([80, [100, 100, 100]], [170, 170, 170], 450, 45, 5062500, 1200)]  # todo 5 muuta
        self.riba_amounts = [0, 100, 0]
        self.right_b_names = ["Tüüp 1", "Tüüp 2", "Tüüp 3", "Tüüp 4", "Tüüp 5"]
        self.right_b_peopletotal = [0, 0, 0, 0, 0]
        self.right_b_amounts = [0, 0, 0, 0, 0]
        self.right_b_prices = [0, 0, 0, 0, 0]
        self.pildid = None
        self.pilv = None
        self.riba = None
        self.parem_sahtel = None
        self.vasak_sahtel = None
        self.metro = None

    def init_all(self, andmed):
        self.pildid = Images()
        # self.filesystem_do(andmed, "load_state")
        self.pilv = Pilv(andmed)
        self.riba = Riba(andmed)
        self.parem_sahtel = ParemSahtel(andmed)
        # self.vasak_sahtel = VasakSahtel(andmed)
        self.metro = Metro(andmed)
        for sizetype in range(5):
            self.parem_nupud.append(ParemNupp(andmed, sizetype))
            # self.vasak_nupud.append(VasakNupp(andmed, sizetype))

    def filesystem_do(self, andmed, action):
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
                self.majad_states = d["majad_states"]
                self.right_b_amounts = d["right_b_amounts"]
                self.right_b_prices = d["right_b_prices"]
                self.right_b_peopletotal = d["right_b_peopletotal"]
                self.riba_amounts = [d["people"], d["money"], d["income"]]
            d.close()
            self.set_loaded_states(andmed)
        elif action == "save_state":
            self.get_current_states()
            d = shelve.open(file)
            d["majad_states"] = self.majad_states
            d["right_b_amounts"] = self.right_b_amounts
            d["right_b_prices"] = self.right_b_prices
            d["right_b_peopletotal"] = self.right_b_peopletotal
            d["people"] = self.riba.people
            d["money"] = self.riba.money
            d["income"] = self.riba.income
            d.close()

    def get_current_states(self):
        for nupp in range(len(self.parem_nupud)):
            self.right_b_amounts[nupp] = self.parem_nupud[nupp].amount
            self.right_b_prices[nupp] = self.parem_nupud[nupp].price
        self.majad_states = [[], [], [], [], []]
        for sizetype in self.majad:
            for maja in sizetype:
                self.majad_states[maja.sizetype].append([maja.sizetype, maja.randtype])

    def set_loaded_states(self, andmed):
        for sizetype in self.majad_states:
            for maja in sizetype:
                Methods.create_house(andmed, maja[0], maja[1])


class Images:
    def __init__(self):
        self.backgrounds = [Images.load_image("Background.png"), Images.load_image("Background_metro.png")]
        self.current_background = self.backgrounds[0]
        self.parem_nupp = [Images.load_image("Button_available.png"), Images.load_image("Button_available_hover.png"),
                           Images.load_image("Button_unavailable.png")]
        self.parem_nupp_logod = [Images.load_image("Maja_1_logo.png"), Images.load_image("Maja_2_logo.png"),
                                 Images.load_image("Maja_3_logo.png"), Images.load_image("Maja_4_logo.png"),
                                 Images.load_image("Maja_5_logo.png")]
        self.vasak_nupp = []
        self.riba = Images.load_image("riba.png")
        self.pilv = Images.load_image("pilv.png")
        self.majad = [
            [Images.load_image("Maja_11.png"), Images.load_image("Maja_12.png"), Images.load_image("Maja_13.png")],
            [Images.load_image("Maja_21.png"), Images.load_image("Maja_22.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_31.png"), Images.load_image("Maja_32.png"), Images.load_image("kell.png")],
            [Images.load_image("Maja_41.png"), Images.load_image("kell.png"), Images.load_image("kell.png")],
            [Images.load_image("kell.png"), Images.load_image("kell.png"), Images.load_image("kell.png")]]
        self.metro = [Images.load_image("Metro.png"), Images.load_image("Metro_train.png"),
                      Images.load_image("Metro_overlay.png")]

    @staticmethod
    def load_image(file):
        file = os.path.join(main_dir, 'data', file)
        try:
            loaded_image = pygame.image.load(file)
        except:
            raise SystemExit("Could not load image " + file + ", " + pygame.get_error())
        return loaded_image.convert_alpha()


class Metro:
    def __init__(self, andmed):
        self.surface = andmed.screen
        self.image_metro = andmed.pildid.metro[0]
        self.image_train = andmed.pildid.metro[1]
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
        self.trainmaxx = andmed.resolution[0] * 2
        andmed.pildid.current_background = andmed.pildid.backgrounds[1]

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


class Maja:
    def __init__(self, andmed, sizetype, randtype):
        self.sizetype = sizetype
        if randtype is None:
            self.randtype = randint(0, 2)
            # kui esimene maja luuakse siis võetakse siit info
            self.inimesed = andmed.majad_types[self.sizetype][2]
            andmed.riba.sissetulek(andmed, self.sizetype, andmed.majad_types[self.sizetype][2], 0, 0)
            andmed.riba.people += self.inimesed
            # ajutine randtype määramine
            if self.sizetype == 3:  # 4 tüüpi on 2 puudu
                self.randtype = 0
            elif self.sizetype == 2 or self.sizetype == 1:  # 2 ja 3 tüüpi maju on 1 puudu
                self.randtype = randint(0, 1)
            elif self.sizetype == 4:  # 5 tüüpi maju pole, asenduseks kell.png
                self.randtype = 0
        else:
            self.randtype = randtype
        self.surface = andmed.screen
        self.image = andmed.pildid.majad[self.sizetype][self.randtype]
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = andmed.majad_types[self.sizetype][0][0]
        for maja in andmed.majad[self.sizetype]:
            self.x += andmed.majad_types[maja.sizetype][0][1][maja.randtype]
        self.y = andmed.majad_types[self.sizetype][1][self.randtype]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, andmed):
        if self.x < andmed.resolution[0]:
            self.surface.blit(self.image, (self.x, self.y))


class Pilv:
    def __init__(self, andmed):
        self.surface = andmed.screen
        self.image = andmed.pildid.pilv
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = -self.w
        self.y = 60
        self.minx = -self.w
        self.maxx = andmed.resolution[0]

    def draw(self):
        if self.x < self.maxx:
            self.x += 1
        else:
            self.x = self.minx
        if self.minx < self.x < self.maxx:
            self.surface.blit(self.image, (self.x, self.y))


class VasakSahtel:
    def __init__(self, andmed):
        self.surface = andmed.screen
        self.minx = 20
        self.maxx = 220
        self.x = self.minx
        self.y = 0
        self.w = 220
        self.h = andmed.resolution[1]
        self.rect = pygame.Rect(0, self.y, self.w, self.h)

    def mouse_hover_check(self, andmed, x, y):
        if self.rect.collidepoint(x, y):
            if self.x < self.maxx:
                self.x += 20
                for nupp in andmed.vasak_nupud:
                    nupp.x += 20
        else:
            if self.x > self.minx:
                self.x -= 20
                for nupp in andmed.vasak_nupud:
                    nupp.x -= 20


class ParemSahtel:
    def __init__(self, andmed):
        self.surface = andmed.screen
        self.minx = 1060
        self.maxx = andmed.resolution[0] - 20
        self.x = self.maxx
        self.y = 0
        self.w = andmed.resolution[0] - self.minx
        self.h = andmed.resolution[1]
        self.rect = pygame.Rect(self.minx, self.y, self.w, self.h)

    def mouse_hover_check(self, andmed, x, y):
        if self.rect.collidepoint(x, y):
            if self.x > self.minx:
                self.x -= 20
                for nupp in andmed.parem_nupud:
                    nupp.x -= 20
        else:
            if self.x < self.maxx:
                self.x += 20
                for nupp in andmed.parem_nupud:
                    nupp.x += 20


class VasakNupp:
    def __init__(self, andmed, sizetype):
        self.surface = andmed.screen
        self.sizetype = sizetype
        self.image_regular = andmed.pildid.parem_nupp[0]
        self.image_highlighted = andmed.pildid.parem_nupp[1]
        self.w = self.image_regular.get_rect().w
        self.h = self.image_regular.get_rect().h
        self.x = 20 - self.w
        self.y = 15 + 100 * self.sizetype
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.logo = andmed.pildid.parem_nupp_logod[self.sizetype]
        self.name = andmed.right_b_names[self.sizetype]
        self.amount = andmed.right_b_amounts[self.sizetype]
        self.price = andmed.right_b_prices[self.sizetype]
        self.desc1 = andmed.right_b_desc1[self.sizetype]
        self.desc2 = andmed.right_b_desc2[self.sizetype]

    def draw(self, andmed, is_highlighted):
        if is_highlighted:
            self.surface.blit(self.image_highlighted, (self.x, self.y))
        else:
            self.surface.blit(self.image_regular, (self.x, self.y))
        Methods.kuva_obj_keskele(andmed, self.logo, (self.x, self.y), (7, 6.653), (47.25, 47.603))
        Methods.kuva_obj_keskele(andmed, self.amount, (self.x, self.y), (7, 62.178), (47.25, 19.256))
        Methods.kuva_obj_keskele(andmed, self.name, (self.x, self.y), (62.013, 7.216), (132.25, 19.256))
        Methods.kuva_obj_keskele(andmed, self.desc1, (self.x, self.y), (62.013, 34.394), (47.25, 19.256))
        Methods.kuva_obj_keskele(andmed, self.desc2, (self.x, self.y), (119, 34.394), (76, 19.256))
        Methods.kuva_obj_keskele(andmed, round(self.price), (self.x, self.y), (62.013, 62.178), (132.25, 19.256))

    def mouse_click_check(self, andmed, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.rect.collidepoint(x, y):
            self.amount += 1
            self.price = andmed.majad_types[self.sizetype][4] * andmed.maja_multiplier ** self.amount
            Methods.create_house(andmed, self.sizetype, None)

    def mouse_hover_check(self, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.rect.collidepoint(x, y):
            return True


class ParemNupp:
    def __init__(self, andmed, sizetype):
        self.hidden = True
        self.surface = andmed.screen
        self.sizetype = sizetype
        self.image_available = andmed.pildid.parem_nupp[0]
        self.image_available_highlighted = andmed.pildid.parem_nupp[1]
        self.image_unavailable = andmed.pildid.parem_nupp[2]
        self.w = self.image_available.get_rect().w
        self.h = self.image_available.get_rect().h
        self.x = andmed.resolution[0] - 20
        self.y = 15 + 100 * self.sizetype
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.logo = andmed.pildid.parem_nupp_logod[self.sizetype]
        self.name = andmed.right_b_names[self.sizetype]
        self.amount = andmed.right_b_amounts[self.sizetype]
        self.price = andmed.majad_types[self.sizetype][4]
        self.people = andmed.majad_types[self.sizetype][2]
        self.peopletotal = andmed.right_b_peopletotal[self.sizetype]

    def draw(self, andmed, is_highlighted):
        if not self.hidden:
            if andmed.riba.money >= self.price:
                if is_highlighted:
                    self.surface.blit(self.image_available_highlighted, (self.x, self.y))
                else:
                    self.surface.blit(self.image_available, (self.x, self.y))
            else:
                self.surface.blit(self.image_unavailable, (self.x, self.y))
            Methods.kuva_obj_keskele(andmed, self.logo, (self.x, self.y), (7, 6.653), (47.25, 47.603))
            Methods.kuva_obj_keskele(andmed, self.amount, (self.x, self.y), (7, 62.178), (47.25, 19.256))
            Methods.kuva_obj_keskele(andmed, self.name, (self.x, self.y), (62.013, 7.216), (132.25, 19.256))
            Methods.kuva_obj_keskele(andmed, self.people, (self.x, self.y), (62.013, 34.394), (47.25, 19.256))
            Methods.kuva_obj_keskele(andmed, self.peopletotal, (self.x, self.y), (119, 34.394), (76, 19.256))
            Methods.kuva_obj_keskele(andmed, round(self.price), (self.x, self.y), (62.013, 62.178), (132.25, 19.256))
        else:
            if andmed.riba.people >= andmed.majad_types[self.sizetype][5]:
                self.hidden = False

    def mouse_click_check(self, andmed, x, y):
        if not self.hidden:
            self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
            if self.rect.collidepoint(x, y):
                if andmed.riba.money >= self.price:
                    andmed.riba.money -= self.price
                    self.amount += 1
                    self.peopletotal += self.people
                    self.price = andmed.majad_types[self.sizetype][4] * andmed.maja_multiplier ** self.amount
                    Methods.create_house(andmed, self.sizetype, None)

    def mouse_hover_check(self, x, y):
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        if self.rect.collidepoint(x, y):
            return True


class Riba:
    # """ :type income_data list"""
    def __init__(self, andmed):
        self.surface = andmed.screen
        self.image = andmed.pildid.riba
        self.time_from_beginning = 0
        self.w = self.image.get_rect().w
        self.h = self.image.get_rect().h
        self.x = 300
        self.y = 6
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.people = andmed.riba_amounts[0]
        self.money = andmed.riba_amounts[1]
        self.income = andmed.riba_amounts[2]
        # esialgsed muutujad
        self.income_space = 0
        self.income_data = [(self.money, 1)]
        self.income_time = 0
        self.temp_multiplier = 0
        self.temo_time2 = 0
        self.objxy = ((19.591, 254.095, 488.6), 7.413)
        self.objwh = (148, 21.621)
        self.objh = 21.621

    def update(self, andmed):
        self.add_income(andmed)
        self.arvuta_space(andmed)
        self.draw(andmed)

    def arvuta_space(self, andmed):
        self.income_time += andmed.tick  # liidame aja lugejale eelmise framei aja
        if self.income_time > 100:  # kui 100ms on täis
            self.temo_time2 += self.income_time  # liidame lugeja väärtuse lugeja2-le
            self.temp_multiplier = (self.income_time / 100)  # kui palju on vaja spacei sissetulekut korrutada et see vastaks 100ms-le

            if self.income_data[-1][0] <= self.money * self.temp_multiplier:  # kui eelmine raha oli väiksem kui praegune raha * ajast tingitud multiplier
                self.income_data.append((self.money * self.temp_multiplier, self.temo_time2))  # lisame uue rahasumma listi, paneme kaasa lugeja2 aja
                # if len(self.income_data) > 7:
                # self.income_space = self.income_data[-1][0] - self.income_data[0][0] - self.income
            elif self.income_data[-1][0] > self.money * self.temp_multiplier:  # kui uus raha (korda multiplier) oli suurem kui vana raha
                self.income_data = [(self.money * self.temp_multiplier, self.temo_time2)]  # teeme uue listi uue rahaga, anname kaasa lugeja2 aja

            if self.income_data[-1][1] - self.income_data[0][1] > 1000:  # kui eelmise raha aeg - praeguse aja vahele jäi vähemalt 1sec
                print(self.temo_time2, self.income_data)
                # lahutame uuest vana raha ja majade fixed sissetuleku ja korrutame selle lugeja2-st tingitud multiplierist
                self.income_space = (self.income_data[-1][0] - self.income_data[0][0] - self.income) * (self.income_data[0][1] / 1000)
                self.income_data.pop(0)  # eemaldame esimese elemendi

            # if len(self.income_data) >= 10:
            #     self.income_data.pop(0)

            self.income_time = 0  # nullime aja lugeja

    @staticmethod
    def sissetulek(andmed, sizetype, people, tax, special):
        per_people = 1.15 * andmed.majad_types[sizetype][3]
        from_people = people * per_people
        per_special = 1
        from_special = special * per_special
        taxed_income = (from_people + from_special) * (1 + tax / 100)
        andmed.riba.income += taxed_income

    def add_income(self, andmed):
        self.time_from_beginning += andmed.tick
        if self.time_from_beginning < 10:  # less than 10ms per frame
            andmed.riba.money += andmed.riba.income / 1000 * self.time_from_beginning / 1
        elif self.time_from_beginning < 100:  # less than 100ms per frame
            andmed.riba.money += andmed.riba.income / 100 * self.time_from_beginning / 10
        elif self.time_from_beginning < 1000:  # less than 1000ms per frame
            andmed.riba.money += andmed.riba.income / 10 * self.time_from_beginning / 100
        self.time_from_beginning = 0

    def draw(self, andmed):
        self.surface.blit(self.image, (self.x, self.y))
        Methods.kuva_obj_keskele(andmed, self.people, (self.x, self.y), (self.objxy[0][0], self.objxy[1]), self.objwh)
        Methods.kuva_obj_keskele(andmed, round(self.money), (self.x, self.y),
                                 (self.objxy[0][1], self.objxy[1]), self.objwh)
        Methods.kuva_obj_keskele(andmed, round(self.income + self.income_space), (self.x, self.y),
                                 (self.objxy[0][2], self.objxy[1]), self.objwh)
