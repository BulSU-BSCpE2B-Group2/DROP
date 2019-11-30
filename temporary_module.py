# THIS IS JUST TEMPORARY SETS OF CODE FOR EXPERIMENTATION STUFF ON MAIN MODULE
# PLEASE USE WITH CAUTION
# THESE MAY CAUSE ERRORS
# PLEASE RUN IT SEPARATELY FROM MAIN MODULE.
# DO NOT IMPORT TO MAIN

import random
import pygame as pg
from sprites import *

font_name = pg.font.match_font(font_name)
vec = pg.math.Vector2


def grow_shrink(directory, size_change_interval, position, timer, scale_size_x, scale_size_y):
    timer += 1
    if timer >= size_change_interval:
        scale_constant = -1
    if timer < size_change_interval:
        scale_constant = 1
    if timer > (size_change_interval * 2):
        timer = 0

    image = pg.image.load(directory)

    scale_size_x += 1 * scale_constant
    scale_size_y += 1 * scale_constant
    image = pg.transform.scale(image, (scale_size_x, scale_size_y))
    rect = image.get_rect()
    rect.center = position

    return image, rect, timer, scale_size_x, scale_size_y

class PlanetGlow:
    def __init__(self):
        self.directory = 'assets/main_menu/5.png'
        self.image = pg.image.load(self.directory)
        self.rect = self.image.get_rect()

    def new(self, timer):
        self.timer = timer
        self.scale_size_x = self.rect.width
        self.scale_size_y = self.rect.height

    def update(self):
        self.image, self.rect, self.timer, self.scale_size_x, self.scale_size_y = grow_shrink(self.directory, 100, (250/2, 250/2), self.timer, self.scale_size_x, self.scale_size_y)


class GameDevTest:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()
        self.win = pg.display.set_mode((500, 500))
        self.planet_glow = PlanetGlow()
        self.running = True

    def new(self):
        self.timer = 0
        self.planet_glow.new(self.timer)
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

    def update(self):
        self.planet_glow.update()

    def draw(self):
        self.win.fill(white)
        self.win.blit(self.planet_glow.image, (self.planet_glow.rect))
        pg.display.flip()

gd = GameDevTest()
while True:
    gd.new()
    if not gd.running:
        break

pg.quit()