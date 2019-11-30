import itertools
import pygame as pg
from os import path
vec = pg.math.Vector2

directory = path.dirname(__file__)

# for loading hs data:
def load_hs_data():
    # read high score from highscore.txt
    with open(path.join(directory, highscore_textfile), 'r') as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0
    return high_score


def draw_text(text, size, color, x, y):
    # function for drawing the text on the screen
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def kinematics(accel, vel, pos):
    # apply friction
    accel.x += vel.x * player_friction
    # equations of motion
    vel += accel
    pos += vel + 0.5 * accel
    return pos

def scrolling_background(x_speed, y_speed, background, background2, bg_rect):
    # assuming that background and background2 are the same images, one bg_rect should only exist
    background.x += x_speed
    background2.x += x_speed
    background.y += y_speed
    background2.y += y_speed
    if background.x < -bg_rect.width:
        background.x = bg_rect.width
    if background2.x < -bg_rect.width:
        background2.x = bg_rect.width
    if background.y < -bg_rect.height:
        background.y = bg_rect.height
    if background2.y < -bg_rect.height:
        background2.y = bg_rect.height
    return background, background2

def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pg.Surface((source.get_width(), source.get_height()), pg.SRCALPHA).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)

def grow_shrink(directory, size_change_interval, position, timer, scale_size_x, scale_size_y):
    timer += 1
    if timer >= size_change_interval:
        scale_constant = -1
    if timer <= size_change_interval:
        scale_constant = 1
    if timer == (size_change_interval * 2):
        timer = 0

    image = pg.image.load(directory)

    scale_size_x += 1 * scale_constant
    scale_size_y += 1 * scale_constant
    image = pg.transform.scale(image, (scale_size_x, scale_size_y))
    rect = image.get_rect()
    rect.center = position

    return image, rect, timer, scale_size_x, scale_size_y

# game resolution and fps
running = True
title = "DROP!"
WIDTH = 800
height = 768
fps = 60
font_style = 'verdana'
highscore_textfile = 'highscore.txt'
screen = pg.display.set_mode((WIDTH, height))
clock = pg.time.Clock()
font_name = pg.font.match_font(font_style)

# Player properties:
player_accel = 0.5
player_friction = -0.10
player_width = 30
player_height = 40
player_gravity = 0.5
player_jump = 20

# list of starter platforms
platform_list = [(WIDTH / 2, height / 2 + 300), (WIDTH / 2 - 85, height / 2 + 300),
                 (WIDTH / 2 - 85*2, height / 2 + 300), (WIDTH / 2 - 85*3, height / 2 + 300),
                 (WIDTH / 2 + 85, height / 2 + 300), (WIDTH / 2 + 85*2, height / 2 + 300),
                 (WIDTH / 2 + 85*3, height / 2 + 300)]

# [((WIDTH / 2 - 50, height * 3 / 4), (100, 20)), ((125, height - 350), (100, 20)),
                 # ((350, 200), (100, 20)), ((172, 100), (50, 20))]

# gaps_1 = [()]


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

#for start_game_screen.py
text_at_start = ['READY', 'SET']
