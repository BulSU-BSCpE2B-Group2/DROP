from .settings import *


class Credits:
    def __init__(self):
        self.black_cover = pg.Surface((WIDTH, height), pg.SRCALPHA)
        self.imgs = [pg.image.load('bin/assets/credits/prepared.png').convert_alpha(),
                     pg.image.load('bin/assets/credits/GRAPHICS-TEAM.png').convert_alpha(),
                     pg.image.load('bin/assets/credits/LOGIC-TEAM.png').convert_alpha()]
        self.img1 = pg.transform.smoothscale(self.imgs[0], (WIDTH, height))
        self.img1_rect = self.imgs[0].get_rect()
        self.img1_rect.topleft = (0, 0)
        self.img2 = pg.transform.smoothscale(self.imgs[1], (WIDTH, height))
        self.img2_rect = self.imgs[1].get_rect()
        self.img2_rect.topleft = (0, 0)
        self.img3 = pg.transform.smoothscale(self.imgs[2], (WIDTH, height))
        self.img3_rect = self.imgs[2].get_rect()
        self.img3_rect.topleft = (0, 0)

    def new(self):
        self.running = True
        self.message = 1
        self.iterator = 0
        self.timer = 0
        self.alpha = 255
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
                self.running = False
                self.exit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def update(self):
        if self.message < 4:
            if self.iterator %2 == 0:
                self.alpha -= 2
                if self.alpha == 1:
                    self.iterator += 1
            elif self.iterator %2 >= 1:
                self.alpha += 2
                if self.alpha == 255:
                    self.iterator += 1
                    self.message += 1
        else:
            self.running = False
        print("ALPHA IS: {}".format(self.alpha))


    def draw(self):
        screen.fill(black)

        if self.message == 1:
            screen.blit(self.img1, self.img1_rect)
        if self.message == 2:
            screen.blit(self.img2, self.img2_rect)
        if self.message == 3:
            screen.blit(self.img3, self.img3_rect)

        self.black_cover.fill((0, 0, 0, self.alpha))
        screen.blit(self.black_cover, (0, 0))
        pg.display.flip()
