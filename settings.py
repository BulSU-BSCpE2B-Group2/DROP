import itertools
import pygame as pg
# game resolution and fps
title = "Pygame Platformer Test"
width = 1280
height = 768
fps = 60
font_name = 'consolas'

#Player properties:
player_accel = 0.5
player_friction = -0.12
player_width = 30
player_height = 40
player_gravity = 0.8
player_jump = 20

# list of platforms
platform_list = [(0, height - 40, width, 40), (width / 2 - 50, height * 3 / 4, 100, 20), (125, height - 350, 100, 20),
                 (350, 200, 100, 20), (172, 100, 50, 20)]

# color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
dark_red = (125, 0, 0)
colors = itertools.cycle(['red', 'blue', 'orange', 'purple'])


