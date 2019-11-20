from settings import *
import pygame as pg

def show_start_screen():
    # show splash / start screen
    times = 0
    color = [(255, 0, 0), (0, 0, 255)]
    color_text = [white, white, black]
    while times < 2:
        a = start_screen_animation(WIDTH, height, color[times], color_text[times], times)
        if a:
            return a
        pg.display.flip()
        times += 1
    new_screen = pg.Surface((WIDTH, height))
    new_screen.fill((white))
    for alpha in range(0, 255, 5):
        new_screen.set_alpha(255 - alpha)
        """draw_text('DROP!', 30, black, WIDTH / 2, height / 3)
        draw_text('Press RETURN to start the game!', 25, black, WIDTH / 2, height / 2)
        draw_text('Press ESC to exit.', 25, black, WIDTH / 2, height / 2 + 70)
        draw_text('High Score is: ' + str(highscore), 25, black, WIDTH / 2, height / 2 + 30)"""
        screen.blit(new_screen, (0, 0))
        pg.display.flip()
    infade_draw_text('DROP!', 30, black, WIDTH / 2, height / 3)
    infade_draw_text('Press RETURN to start the game!', 25, black, WIDTH / 2, height / 2)
    infade_draw_text('High Score is: ' + str(highscore), 25, black, WIDTH / 2, height / 2 + 35)
    infade_draw_text('Press ESC to exit.', 25, black, WIDTH / 2, height / 2 + 70)
    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            if not run:
                return run
    run = wait_key_event_start_screen()
    return run


def start_screen_animation(width, height, color, c_text, times):
    fade = pg.Surface((width, height))
    fade.fill((0, 0, 0))
    draw_text(text_at_start[times], 65, white, WIDTH / 2, height / 2)
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.fill((color))
        draw_text(text_at_start[times], 65, c_text, WIDTH / 2, height / 2)
        screen.blit(fade, (0, 0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                if not running:
                    return running
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pass


def wait_key_event_start_screen():
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                return waiting
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    waiting = True
                    return waiting
                if event.key == pg.K_ESCAPE:
                    waiting = False
                    return waiting
