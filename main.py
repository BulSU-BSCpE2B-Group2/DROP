import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()
        # starting a new game

    def run(self):
        # Game loop
        while self.running:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        # game loop update

    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False

    def draw(self):
        # Game loop for drawing graphics
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        font = pg.font.SysFont('consolas', 30)
        text = font.render("Press 's' to reset the figure", 5, (255, 0, 0))
        self.screen.blit(text, (width / 2 - (text.get_width() / 2), height / 2 - (text.get_height() / 2)))
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # show splash / start screen
        pass

    def show_go_screen(self):
        # show game over / continue
        pass


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
