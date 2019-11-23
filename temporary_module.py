# THIS IS JUST TEMPORARY SETS OF CODE FOR EXPERIMENTATION STUFF ON MAIN MODULE
# PLEASE USE WITH CAUTION
# THESE MAY CAUSE ERRORS
# PLEASE RUN IT SEPARATELY FROM MAIN MODULE.

import random
import pygame as pg
from settings import *
from sprites import *

pg.init()
screen = pg.display.set_mode((500, 500))
font_name = pg.font.match_font(font_name)
clock = pg.time.Clock()

running = True
PULSE_EVENT = pg.USEREVENT
# block = 500 / 10


def fade_pause_animation():
    clock.tick(fps)
    screen.fill(white)
    i = 0
    position_x = 0
    interval = 1000
    while i <= 80:
        timer = 0
        while True:
            timer += 0.007
            if timer > interval:
                break
        surface = pg.Surface((500, 500), pg.SRCALPHA)
        pg.draw.rect(surface, black, (position_x, 0, 10, 500))
        pg.draw.rect(surface, black, (490 - position_x, 0, 10, 500))
        draw_text('PAUSE', 65, white, 500 / 2, 500 / 2)
        screen.blit(surface, (0, 0))
        pg.display.flip()
        b = event_while_animation()
        if b:
            return False
        i += 1
        position_x += 10
    a = wait_key_event_pause_screen()
    if a:
        fade_pause_animation()


def wait_key_event_pause_screen():
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                return waiting
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    waiting = True
                    return waiting
                if event.key == pg.K_ESCAPE:
                    waiting = False
                    return waiting


def event_while_animation():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                return True
            if event.key == pg.K_ESCAPE:
                return True


while running:
    clock.tick(fps)
    screen.fill(white)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_RETURN:
                fade_pause_animation()
    pg.display.flip()

pg.quit()