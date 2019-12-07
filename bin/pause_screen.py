from .settings import *
import pygame as pg
import random


class PauseScreen:
    def __init__(self):
        self.i = 0
        self.position_x = 0
        self.interval = 1000

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
        pg.draw.rect(self.surface, (0, 0, 0, 100), (self.position_x, 0, 10, height))
        pg.draw.rect(self.surface, (0, 0, 0, 100), ((WIDTH - 10) - self.position_x, 0, 10, height))
        screen.blit(self.surface, (0, 0))
        draw_text('PAUSE', 65, white, WIDTH / 2, height / 2 - 50)
        draw_text('Press ESC to exit.', 25, white, WIDTH / 2, height / 2 + 30)
        draw_text('Press RETURN to continue.', 25, white, WIDTH / 2, height / 2 + 85)
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


def fade_pause_animation():
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
        pg.draw.rect(surface, (0, 0, 0, 100), (position_x, 0, 10, height))
        pg.draw.rect(surface, (0, 0, 0, 100), ((WIDTH - 10) - position_x, 0, 10, height))
        screen.blit(surface, (0, 0))
        draw_text('PAUSE', 65, white, WIDTH / 2, height / 2 - 30)
        draw_text('Press ESC to continue.', 45, white, WIDTH / 2, height / 2 + 45)
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



