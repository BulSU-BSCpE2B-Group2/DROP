# Sprite classes for platform game
import pygame as pg
from settings import *
vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((player_width, player_height))
        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)
        self.pos = vec(width / 2, height / 2)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.cc_step = 1
        self.base_color = next(colors)
        self.next_color = next(colors)
        self.current_color = self.base_color

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -player_jump

    def update(self):
        self.accel = vec(0, player_gravity)
        self.image.fill(self.cycle_color())
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.accel.x = -player_accel

        if keys[pg.K_RIGHT]:
            self.accel.x = player_accel

        # apply friction
        self.accel.x += self.vel.x * player_friction
        # equations of motion
        self.vel += self.accel
        self.pos += self.vel + 0.5 * self.accel
        # wrap around the screen
        if self.pos.x > width - (player_width / 2):
            self.pos.x = width - player_width / 2
        if self.pos.x < player_width / 2:
            self.pos.x = player_width / 2

        self.rect.midbottom = self.pos

    def cycle_color(self):
        change_bg_every_x_seconds = 3
        number_of_steps = change_bg_every_x_seconds * fps

        self.cc_step += 1
        if self.cc_step < number_of_steps:
            # (y-x)/number_of_steps calculates the amount of change per step required to
            # fade one channel of the old color to the new color
            # We multiply it with the current step counter
            self.current_color = [x + (((y - x) / number_of_steps) * self.cc_step) for x, y in
                             zip(pg.color.Color(self.base_color), pg.color.Color(self.next_color))]
        else:
            self.cc_step = 1
            self.base_color = self.next_color
            self.next_color = next(colors)
        return self.current_color


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



