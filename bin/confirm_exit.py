from .settings import *


class ConfirmExitScreen:
    def __init__(self):
        self.i = 0
        self.position_x = 0
        self.interval = 1000

        self.confirm_exit_img = pg.image.load('bin/assets/confirm_exit/sure.png').convert_alpha()
        self.confirm_exit_img = pg.transform.smoothscale(self.confirm_exit_img, (730, 353))
        self.confirm_exit_img_rect = self.confirm_exit_img.get_rect()
        self.confirm_exit_img_rect.center = (WIDTH / 2, height / 2)

    def new(self):
        self.running = True
        self.exit = False
        self.i = 0
        self.position_x = -10
        self.timer = 0
        self.run()

    def run(self):
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.i <= 80:
            self.timer += 0.007
            self.surface = pg.Surface((WIDTH, height), pg.SRCALPHA)
            self.i += 1
            self.position_x += 10

        else:
            self.running = self.wait_key_event_pause_screen()

    def draw(self):
        pg.draw.rect(self.surface, (125, 125, 0, 100), (self.position_x, 0, 10, height))
        pg.draw.rect(self.surface, (125, 125, 0, 100), ((WIDTH - 10) - self.position_x, 0, 10, height))
        screen.blit(self.surface, (0, 0))
        screen.blit(self.confirm_exit_img, self.confirm_exit_img_rect)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.running = False
                if event.key == pg.K_ESCAPE:
                    self.exit = True
                    self.running = False

    def wait_key_event_pause_screen(self):
        self.waiting = True
        while self.waiting:
            clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    return self.waiting
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.waiting = False
                        return self.waiting
                    if event.key == pg.K_ESCAPE:
                        self.waiting = False
                        self.exit = True
                        return self.waiting
