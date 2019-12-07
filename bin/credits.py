from .settings import *


class Credits:
    def __init__(self):
        self.black_cover = pg.Surface((WIDTH, height), pg.SRCALPHA)

    def new(self):
        self.running = True
        self.firstmessage = True
        self.secondmessage = False
        self.thirdmessage = False
        self.multiplier = 1
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
        self.timer += 2
        if 0 < self.timer < 254:
            self.alpha -= 2
            self.firstmessage = True
            self.secondmessage = False
        elif 253 < self.timer < 506:
            self.alpha += 2
        elif 506 <= self.timer < 759:
            self.alpha -= 2
            self.secondmessage = True
            self.firstmessage = False
        elif 759 <= self.timer < 1011:
            self.alpha += 2
        elif 1011 < self.timer < 1263:
            self.alpha -= 2
            self.thirdmessage = True
            self.secondmessage = False
        elif 1263 < self.timer < 1515:
            self.alpha += 2
        elif 1515 < self.timer < 1600:
            self.alpha = 255
        else:
            self.running = 0

        print("Timer is: {}".format(self.timer))
        print("ALPHA IS: {}".format(self.alpha))

    def draw(self):
        screen.fill(black)

        if self.firstmessage:
            draw_text('Prepared by GROUP 2', 25, white, WIDTH / 2, height / 2)
            draw_text('of BSCpE - 2B', 25, white, WIDTH / 2, height / 2 + 50)
        if self.secondmessage:
            draw_text('Credits to:', 25, white, WIDTH / 2, height / 2 - 100)
            draw_text('John Paul Cervantes - Graphics Design', 20, white, WIDTH / 2, height / 2 - 60)
            draw_text('Joshua Mark Esguerra - Graphics Design and Sounds', 20, white, WIDTH / 2, height / 2 - 30)
            draw_text('Melissa Mendoza - Graphics Design and Layout', 20, white, WIDTH / 2, height / 2)
            draw_text('Ramon Soledad - Graphics Design', 20, white, WIDTH / 2, height / 2 + 30)
        if self.thirdmessage:
            draw_text('Kristian Santos - Game Logistics and Power-up Implementation', 20, white, WIDTH / 2, height / 2 - 60)
            draw_text('Jonas Pagtalunan - Game Logistics', 20, white, WIDTH /2 , height / 2 - 30)
            draw_text('Paul Christian Aguilar - Game Logistics and Quality Control', 20, white, WIDTH / 2, height / 2)
            draw_text('Ronie de Jesus - Game Logistics', 20, white, WIDTH / 2, height / 2 + 30)

        self.black_cover.fill((0, 0, 0, self.alpha))
        screen.blit(self.black_cover, (0, 0))
        pg.display.flip()
