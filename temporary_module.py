# THIS IS JUST TEMPORARY SETS OF CODE FOR EXPERIMENTATION STUFF ON MAIN MODULE
# PLEASE USE WITH CAUTION
# THESE MAY CAUSE ERRORS

import random
import pygame as pg
from settings import *
from sprites import *


def shuffle_platform():
    gaps = random.randint(1, 5)
    gaps_1 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_3 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    if gaps == 1:
        random.shuffle(gaps_1)
        self.sequence = gaps_1
    elif gaps == 2:
        random.shuffle(gaps_2)
        self.sequence = gaps_2
    elif gaps == 3:
        random.shuffle(gaps_3)
        self.sequence = gaps_3
    elif gaps == 4:
        random.shuffle(gaps_4)
        self.sequence = gaps_4
    else:
        random.shuffle(gaps_2)
        self.sequence = gaps_2
    for x in self.sequence:
        if x == 1:
            p = Platform(self.orig_pos, 90 + height, width / 12, 20)
            self.all_sprites.add(p)
            self.platforms.add(p)
            self.orig_pos += width / 12
        else:
            self.orig_pos += width / 12

""" UNUSED CODE. MIGHT BE USED IN THE NEAR FUTURE
platforms_all = self.shuffle_platform(wide)
for platform in platforms_all:
    p = Platform(*platform)
    self.all_sprites.add(p)
    self.platforms.add(p)"""

# if player reaches top 1/4 of the screen
"""if self.player.rect.top <= height / 4:
    self.player.pos.y += abs(self.player.vel.y)"""