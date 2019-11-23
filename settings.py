import itertools
import pygame as pg
from os import path


def load_hs_data():
    # read high score from highscore.txt
    with open(path.join(dir, highscore_textfile), 'w') as f:
        try:
            highscore = int(f.read())
        except:
            highscore = 0
    return highscore


def draw_text(text, size, color, x, y):
    # function for drawing the text on the screen
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def infade_draw_text(text, size, color, x, y):
    # function for drawing the text on the screen
    clock = pg.time.Clock()
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    txt_surf = text_surface.copy()
    alpha_surf = pg.Surface(txt_surf.get_size(), pg.SRCALPHA)
    alpha = 255
    while alpha > 0:
        alpha = max(alpha - 50, 0)
        txt_surf = text_surface.copy()
        alpha_surf.fill((255, 255, 255, 255 - alpha))
        txt_surf.blit(alpha_surf, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        screen.blit(txt_surf, text_rect)
        pg.display.flip()
        clock.tick(fps)


# game resolution and fps
running = True
title = "Pygame Platformer Test"
WIDTH = 800
height = 768
fps = 60
font_style = 'arial'
highscore_textfile = 'highscore.txt'
screen = pg.display.set_mode((WIDTH, height))
clock = pg.time.Clock()
font_name = pg.font.match_font(font_style)

# Player properties:
player_accel = 0.5
player_friction = -0.08
player_width = 30
player_height = 40
player_gravity = 1
player_jump = 20

# list of platforms
platform_list = []

# [((WIDTH / 2 - 50, height * 3 / 4), (100, 20)), ((125, height - 350), (100, 20)),
                 # ((350, 200), (100, 20)), ((172, 100), (50, 20))]


gaps_1 = [()]


# temporary (0, height - 40, width, 40),

# color
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (125, 125, 125)
yellow = (255, 255, 0)
dark_red = (125, 0, 0)
colors = itertools.cycle(['red', 'blue', 'orange', 'purple'])

#for loading hs data:
dir = path.dirname(__file__)
highscore = load_hs_data()

#for start_screen.py
text_at_start = ['Ready', 'Set']



