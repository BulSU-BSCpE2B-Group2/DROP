# THIS IS JUST TEMPORARY SETS OF CODE FOR EXPERIMENTATION STUFF ON MAIN MODULE
# PLEASE USE WITH CAUTION
# THESE MAY CAUSE ERRORS

import random
import pygame as pg
from settings import *
from sprites import *

pg.init()
screen = pg.display.set_mode((500, 500))


def start_screen_animation(width, height):
    fade = pg.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        screen.fill((0, 255, 255))
        screen.blit(fade, (0, 0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
        pg.time.delay(1)


try:
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_RETURN:
                    start_screen_animation(500, 500)
        clock = pg.time.Clock()
        clock.tick(fps)
except pg.error:
    print("An error has occured within the program.")
else:
    pg.quit()
