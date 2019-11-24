from settings import *


class MainMenu:
    def __init__(self):
        self.screen = screen

    def new(self):
        self.running = True
        self.run()

    def run(self):
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(white)
        # show splash / start screen

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