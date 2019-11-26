from settings import *
import pygame as pg
import random


def fade_pause_animation():
    clock.tick(fps)
    i = 0
    position_x = 0
    interval = 1000
    while i <= 80:
        timer = 0
        while True:
            timer += 0.007
            if timer > interval:
                break
        surface = pg.Surface((WIDTH, height), pg.SRCALPHA)
        pg.draw.rect(surface, black, (position_x, 0, 10, height))
        pg.draw.rect(surface, black, ((WIDTH - 10) - position_x, 0, 10, height))
        draw_text('PAUSE', 65, white, WIDTH / 2, height / 2 - 30)
        draw_text('Press ESC to continue.', 45, white, WIDTH / 2, height / 2 + 45)
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


def event_while_animation():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                return True
            if event.key == pg.K_ESCAPE:
                return True


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
