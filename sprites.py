# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((player_width, player_height))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width / 2, height / 2)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

    def update(self):
        self.accel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.accel.x = -player_accel

        if keys[pg.K_RIGHT]:
            self.accel.x = player_accel

        if keys[pg.K_UP]:
            self.accel.y = -player_accel

        if keys[pg.K_DOWN]:
            self.accel.y = player_accel

        if keys[pg.K_s]:
            self.pos = vec(width / 2, height / 2)
            self.vel = vec(0, 0)
            self.accel = vec(0, 0)

        # apply friction
        self.accel += self.vel * player_friction
        self.vel += self.accel
        self.pos += self.vel + 0.5 * self.accel
        # wrap around the screen
        if self.pos.x > width - (player_width / 2):
            self.pos.x = player_width / 2
        if self.pos.x < player_width / 2:
            self.pos.x = width - player_width / 2

        self.rect.center = self.pos
