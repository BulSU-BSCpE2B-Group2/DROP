# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((player_width, player_height))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width / 2, height / 2)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        self.accel = vec(0, player_gravity)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.accel.x = -player_accel

        if keys[pg.K_RIGHT]:
            self.accel.x = player_accel

        if keys[pg.K_s]:
            self.pos = vec(width / 2, height / 2)
            self.vel = vec(0, 0)
            self.accel = vec(0, 0)



        # apply friction
        self.accel.x += self.vel.x * player_friction
        # equations of motion
        self.vel += self.accel
        self.pos += self.vel + 0.5 * self.accel
        # wrap around the screen
        if self.pos.x > width - (player_width / 2):
            self.pos.x = player_width / 2
        if self.pos.x < player_width / 2:
            self.pos.x = width - player_width / 2

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
