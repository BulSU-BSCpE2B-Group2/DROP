# Sprite classes for platform game
import pygame as pg
import random
from settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((player_width, player_height))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, height / 2)
        self.pos = vec(WIDTH / 2, height / 2)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.cc_step = 1
        self.base_color = next(colors)
        self.next_color = next(colors)
        self.current_color = self.base_color

    """def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -player_jump"""

    def update(self):
        self.accel = vec(0, player_gravity)
        self.image.fill(self.cycle_color())
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.accel.x = -player_accel

        if keys[pg.K_RIGHT]:
            self.accel.x = player_accel

        # kinematics equation from the settings module
        self.pos = kinematics(self.accel, self.vel, self.pos)
        # wrap around the screen
        if self.pos.x > WIDTH - (player_width / 2):
            self.pos.x = WIDTH - player_width / 2
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
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface(dimensions)
        # self.image.fill(green)
        self.image = pg.image.load('assets/platform/platform-01.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = self.position


class SlowPlatformPowerUp(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = self.position


def spawn_power_up(generate, pu_spawn_height):
    p_rect = pg.Rect(0, 0, WIDTH / 12, height * pu_spawn_height - 50)
    spawn = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    no_spawn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if generate == 1:
        random.shuffle(spawn)
        sequence = spawn
    else:
        sequence = no_spawn
    return sequence, p_rect


def add_platform(gaps, spawn_height):
    rect = pg.Rect(0, 0, WIDTH / 12, height * spawn_height)
    gaps_1 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_3 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    if gaps == 1:
        random.shuffle(gaps_1)
        sequence = gaps_1
    elif gaps == 2:
        random.shuffle(gaps_2)
        sequence = gaps_2
    elif gaps == 3:
        random.shuffle(gaps_3)
        sequence = gaps_3
    elif gaps == 4:
        random.shuffle(gaps_4)
        sequence = gaps_4
    else:
        random.shuffle(gaps_2)
        sequence = gaps_2
    return sequence, rect
