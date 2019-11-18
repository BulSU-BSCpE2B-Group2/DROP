# THIS IS JUST TEMPORARY SETS OF CODE FOR EXPERIMENTATION STUFF ON MAIN MODULE
# PLEASE USE WITH CAUTION
# THESE MAY CAUSE ERRORS

import random
import pygame as pg
from settings import *
from sprites import *

pg.init()
screen = pg.display.set_mode((500, 500))
font_name = pg.font.match_font(font_name)
clock = pg.time.Clock()
clock.tick(fps)

PULSE_EVENT = pg.USEREVENT + 1


def start_screen_animation(width, height, color, c_text):
    fade = pg.Surface((width, height))
    fade.fill((0, 0, 0))
    draw_text(text[times], 65, white, 500 / 2, 500 / 2)
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        screen.fill((color))
        draw_text(text[times], 65, c_text, 500 / 2, 500 / 2)
        screen.blit(fade, (0, 0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()


def draw_text(text, size, color, x, y):
    # function for drawing the text on the screen
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


try:
    run = True
    while run:
        show_main_menu = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_RETURN:
                    pg.time.set_timer(PULSE_EVENT, 1)
            if event.type == PULSE_EVENT:
                times = 0
                color = [(255, 0, 0), (0, 0, 255)]
                text = ['Ready', 'Set']
                color_text = [white, white, black]
                while times < 2:
                    start_screen_animation(500, 500, color[times], color_text[times])
                    pg.display.flip()
                    times += 1
                pg.time.set_timer(PULSE_EVENT, 0)
                show_main_menu = True
        if show_main_menu:
            new_screen = pg.Surface((500, 500))
            new_screen.fill((255, 255, 255))
            new_screen.set_alpha(255)
            # screen.blit(new_screen, (0, 0))
            for alpha in range(0, 255):
                new_screen.set_alpha(255 - alpha)
                draw_text('DROP!', 65, black, 250, 250)
                draw_text('Main menu should go here.', 25, black, 250, 350)
                draw_text('FLASH SHOULD HAPPEN', 20, black, 250, 100)
                draw_text('BEFORE THIS MENU SHOWS UP', 20, black, 250, 150)
                screen.blit(new_screen, (0, 0))
                pg.display.flip()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            pg.quit()

            pg.display.flip()
        else:
            screen.fill((255, 255, 255))


except pg.error:
    print("An error has occured within the program.")
else:
    pg.quit()
