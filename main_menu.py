from settings import *
vec = pg.math.Vector2


class MainMenu:
    def __init__(self):
        # initialize screen
        self.screen = screen

        # initialize background 1 & 2
        self.bg = pg.image.load('assets/main_menu/bg-darker.png').convert_alpha()
        self.bg2 = pg.image.load('assets/main_menu/bg-darker.png').convert_alpha()
        self.bg_rect = self.bg.get_rect()

        # initialize the required classes
        self.logo = Logo()
        self.planet_venus = PlanetVenus()
        self.planet_earth = PlanetEarth()
        self.planet_mars = PlanetMars()
        self.button = Buttons()
        self.settings_screen = SettingsScreen()
        self.comets = Comets()

    def new(self):
        self.running = True
        self.timer = 0
        self.show_settings = False
        self.background = vec(0, 0)
        self.background2 = vec(self.bg_rect.width, 0)
        self.run()

    def run(self):
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        """if self.timer < 120:
            # self.b.position.x += 1
            self.timer += 1"""
        self.background, self.background2 = scrolling_background(-2, 0, self.background, self.background2, self.bg_rect)
        self.mouse_coordinate = pg.mouse.get_pos()

    def draw(self):
        screen.blit(self.bg, self.background)
        screen.blit(self.bg2, self.background2)
        # insert in this line the glowy effect thingies
        screen.blit(self.comets.comets_glow, self.comets.comets_glow_rect)
        screen.blit(self.comets.comets, self.comets.comets_rect)
        screen.blit(self.planet_mars.mars, self.planet_mars.mars_rect)
        screen.blit(self.planet_mars.mars_glow, self.planet_mars.mars_glow_rect)
        screen.blit(self.planet_venus.venus_glow, self.planet_venus.venus_glow_rect)
        screen.blit(self.planet_venus.venus, self.planet_venus.venus_rect)
        screen.blit(self.planet_earth.earth_glow, self.planet_earth.earth_glow_rect)
        screen.blit(self.planet_earth.earth, self.planet_earth.earth_rect)
        screen.blit(self.button.settings_button, self.button.settings_button_rect)
        screen.blit(self.button.start_button, self.button.start_button_rect)
        screen.blit(self.logo.logo, self.logo.position)
        if self.show_settings:
            settings_overlay_with_opacity = pg.Surface((WIDTH, height), pg.SRCALPHA)
            settings_overlay_with_opacity.fill((100, 100, 100, 100))
            screen.blit(settings_overlay_with_opacity, (0, 0))
            screen.blit(self.settings_screen.settings_overlay, self.settings_screen.settings_overlay_rect)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.exit = True
            if not self.show_settings:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.running = False
                        self.exit = False
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        self.exit = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.mouse_coordinate[0] > self.button.start_button_rect.x:
                        if self.mouse_coordinate[0] < self.button.start_button_rect.x + self.button.start_button_rect.top:
                            if self.mouse_coordinate[1] > self.button.start_button_rect.y:
                                if self.mouse_coordinate[1] < self.button.start_button_rect.y + 120:
                                    self.running = False
                                    self.exit = False
                    if self.mouse_coordinate[0] > self.button.settings_button_rect.x:
                        if self.mouse_coordinate[0] < self.button.settings_button_rect.x + self.button.settings_button_rect.top:
                            if self.mouse_coordinate[1] > self.button.settings_button_rect.y:
                                if self.mouse_coordinate[1] < self.button.settings_button_rect.y + 106:
                                    self.show_settings = True
            else:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.show_settings = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.mouse_coordinate[0] > self.settings_screen.settings_overlay_rect.x + 562:
                        if self.mouse_coordinate[0] < self.settings_screen.settings_overlay_rect.x + 652:
                            if self.mouse_coordinate[1] > self.settings_screen.settings_overlay_rect.y:
                                if self.mouse_coordinate[1] < self.settings_screen.settings_overlay_rect.y + 93:
                                    self.show_settings = False


class Logo:
    def __init__(self):
        self.logo = pg.image.load('assets/main_menu/TITLE.png').convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (WIDTH/2, height/2)
        self.position = vec(WIDTH / 2 - self.logo_rect.top, (height / 2) - self.logo_rect.left - 90)


class PlanetVenus:
    def __init__(self):
        self.venus = pg.image.load('assets/main_menu/4.png').convert_alpha()
        self.venus_rect = self.venus.get_rect()
        self.venus_glow = pg.image.load('assets/main_menu/3.png').convert_alpha()
        self.venus_glow_rect = self.venus_glow.get_rect()
        # set position for the planet mars and its glow
        self.venus_rect.center = (WIDTH / 9, height / 2 + 70)
        self.venus_glow_rect.center = self.venus_rect.center

class PlanetEarth:
    def __init__(self):
        self.earth = pg.image.load('assets/main_menu/2.png').convert_alpha()
        self.earth_rect = self.earth.get_rect()
        self.earth_glow = pg.image.load('assets/main_menu/1.png').convert_alpha()
        self.earth_glow_rect = self.earth_glow.get_rect()
        # set position for the planet earth and its glow
        self.earth_rect.center = (WIDTH / 4, height / 4 - 50)
        self.earth_glow_rect.center = self.earth_rect.center

class PlanetMars:
    def __init__(self):
        self.mars = pg.image.load('assets/main_menu/6.png').convert_alpha()
        self.mars_rect = self.mars.get_rect()
        self.mars_glow = pg.image.load('assets/main_menu/5.png').convert_alpha()
        self.mars_glow_rect = self.mars_glow.get_rect()
        self.mars_rect.center = (WIDTH - WIDTH / 8, height / 8)
        self.mars_glow_rect.center = (WIDTH - WIDTH / 8 + 6, height / 8 + 2)

class Buttons:
    def __init__(self):
        # initialize asset for settings button
        self.settings_button = pg.image.load('assets/main_menu/SETTINGS.png').convert_alpha()
        self.settings_button_rect = self.settings_button.get_rect()
        # initialize asset for start button
        self.start_button = pg.image.load('assets/main_menu/START.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect()
        # set position for the buttons
        self.settings_button_rect.center = (WIDTH / 2, height / 2 + 190)
        self.start_button_rect.center = (WIDTH / 2, height / 2 + 70)

class SettingsScreen:
    def __init__(self):
        self.settings_overlay = pg.image.load('assets/settings_menu/SETTINGS.png').convert_alpha()
        self.settings_overlay_rect = self.settings_overlay.get_rect()
        self.settings_overlay_rect.center = (WIDTH / 2, height / 2)

class Comets:
    def __init__(self):
        self.comets = pg.image.load('assets/main_menu/bg-09.png').convert_alpha()
        self.comets_glow = pg.image.load('assets/main_menu/bg-08.png').convert_alpha()
        self.comets_rect = self.comets.get_rect()
        self.comets_glow_rect = self.comets_glow.get_rect()
        self.comets_rect.center = (WIDTH / 2 + 200, height / 2 - 90 + 270)
        self.comets_glow_rect.center = (WIDTH / 2 + 190, height / 2 - 115 + 270)
