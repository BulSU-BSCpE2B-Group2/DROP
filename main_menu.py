from settings import *
vec = pg.math.Vector2


class MainMenu:
    def __init__(self):
        # initialize screen
        self.screen = screen

        # initialize background 1 & 2
        self.bg = pg.image.load('assets/main_menu/bg.png').convert_alpha()
        self.bg2 = pg.image.load('assets/main_menu/bg.png').convert_alpha()
        self.bg_rect = self.bg.get_rect()

        # initialize the required classes
        self.logo = Logo()
        self.planet_mars = PlanetMars()
        self.planet_earth = PlanetEarth()
        self.button = Buttons()

    def new(self):
        self.running = True
        self.timer = 0
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
        self.background, self.background2 = scrolling_background(-3, 0, self.background, self.background2, self.bg_rect)

    def draw(self):
        screen.blit(self.bg, (self.background.x, self.background.y))
        screen.blit(self.bg2, (self.background2.x, self.background2.y))
        # insert in this line the glowy effect thingies
        screen.blit(self.planet_mars.mars_glow, self.planet_mars.mars_glow_rect)
        screen.blit(self.planet_mars.mars, self.planet_mars.mars_rect)
        screen.blit(self.planet_earth.earth_glow, self.planet_earth.earth_glow_rect)
        screen.blit(self.planet_earth.earth, self.planet_earth.earth_rect)
        screen.blit(self.button.settings_button, self.button.settings_button_rect)
        screen.blit(self.button.start_button, self.button.start_button_rect)
        screen.blit(self.logo.logo, self.logo.position)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.exit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.running = False
                    self.exit = False
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.exit = True


class Logo:
    def __init__(self):
        self.logo = pg.image.load('assets/main_menu/TITLE.png').convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (WIDTH/2, height/2)
        self.position = vec(WIDTH / 2 - self.logo_rect.top, (height / 2) - self.logo_rect.left - 90)


class PlanetMars:
    def __init__(self):
        self.mars = pg.image.load('assets/main_menu/4.png').convert_alpha()
        self.mars_rect = self.mars.get_rect()
        self.mars_glow = pg.image.load('assets/main_menu/3.png').convert_alpha()
        self.mars_glow_rect = self.mars_glow.get_rect()
        self.position = vec(self.mars_rect.top, self.mars_rect.left)
        self.mars_rect.center = (WIDTH / 2 + 120, height / 2 + 70)
        self.mars_glow_rect.center = self.mars_rect.center

class PlanetEarth:
    def __init__(self):
        self.earth = pg.image.load('assets/main_menu/2.png').convert_alpha()
        self.earth_rect = self.earth.get_rect()
        self.earth_glow = pg.image.load('assets/main_menu/1.png').convert_alpha()
        self.earth_glow_rect = self.earth_glow.get_rect()
        self.position = vec(self.earth_rect.top, self.earth_rect.left)
        self.earth_rect.center = (WIDTH / 4, height / 4 - 50)
        self.earth_glow_rect.center = self.earth_rect.center

class Buttons:
    def __init__(self):
        self.settings_button = pg.image.load('assets/main_menu/SETTINGS.png').convert_alpha()
        self.settings_button_rect = self.settings_button.get_rect()
        self.start_button = pg.image.load('assets/main_menu/START.png').convert_alpha()
        self.start_button_rect = self.start_button.get_rect()
        self.position = vec(self.settings_button_rect.top, self.settings_button_rect.left)
        self.settings_button_rect.center = (WIDTH / 2, height / 2 + 190)
        self.start_button_rect.center = (WIDTH / 2, height / 2 + 70)
