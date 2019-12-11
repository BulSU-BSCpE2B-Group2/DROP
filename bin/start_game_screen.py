from .settings import *


class StartAnimation:
    def __init__(self):
        self.flash = pg.Surface((WIDTH, height), pg.SRCALPHA)

        self.ready = pg.image.load('bin/assets/game_screen/READY.png').convert_alpha()
        self.ready_rect = self.ready.get_rect()
        self.ready_rect.center = (WIDTH / 2, height / 2)

        self.set = pg.image.load('bin/assets/game_screen/set.png').convert_alpha()
        self.set_rect = self.set.get_rect()
        self.set_rect.center = self.ready_rect.center

        self.go = pg.image.load('bin/assets/game_screen/go.png').convert_alpha()
        self.go_rect = self.go.get_rect()
        self.go_rect.center = self.ready_rect.center

    def new(self):
        self.alpha = 255
        self.iterator = 0
        self.running = True
        self.run()

    def run(self):
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pass
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    pass
                if event.key == pg.K_ESCAPE:
                    pass

    def update(self):
        if self.iterator < 3:
            if self.alpha > 0:
                self.alpha -= 5
            else:
                self.alpha = 255
                self.iterator += 1
        else:
            self.running = False

    def draw(self):
        if self.iterator == 0:
            screen.blit(self.ready, self.ready_rect)
        elif self.iterator == 1:
            screen.blit(self.set, self.set_rect)
        elif self.iterator == 2:
            screen.blit(self.go, self.go_rect)

        self.flash.fill((255, 255, 255, self.alpha))
        screen.blit(self.flash, (0, 0))
        pg.display.flip()
