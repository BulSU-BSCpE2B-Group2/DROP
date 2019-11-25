from settings import *
vec = pg.math.Vector2

class Logo:
    def __init__(self):
        self.logo = pg.image.load('assets/main_menu/TITLE.png')
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (WIDTH/2, height/2)
        self.position = vec(WIDTH / 2 - self.logo_rect.top, (height / 2) - self.logo_rect.left)

class Planet:
    def __init__(self):
        self.planet = pg.image.load('assets/main_menu/4.png').convert_alpha()
        self.planet_rect = self.planet.get_rect()
        self.position = vec(self.planet_rect.top, self.planet_rect.left)

class MainMenu:
    def __init__(self):
        self.screen = screen
        self.bg = pg.image.load('assets/main_menu/bg.png').convert_alpha()
        self.bg_rect = self.bg.get_rect()
        self.bg2 = pg.image.load('assets/main_menu/bg.png').convert_alpha()
        self.glow = pg.image.load('assets/main_menu/3.png').convert_alpha()
        self.glow_rect = self.glow.get_rect()
        self.logo = Logo()
        self.planet = Planet()
        self.planet.planet_rect.center = self.glow_rect.center

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
        self.background.x -= 3
        self.background2.x -= 3
        if self.background.x < -self.bg_rect.width:
            self.background.x = self.bg_rect.width
        if self.background2.x < -self.bg_rect.width:
            self.background2.x = self.bg_rect.width
        #self.bg.scroll(dx=0, dy=-1)

    def draw(self):
        screen.blit(self.bg, (self.background.x, self.background.y))
        screen.blit(self.bg2, (self.background2.x, self.background2.y))
        #screen.blit(self.bg, (0, 0))
        # insert in this line the glowy effect thingies
        screen.blit(self.glow, self.glow_rect)
        screen.blit(self.planet.planet, self.planet.planet_rect)
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
