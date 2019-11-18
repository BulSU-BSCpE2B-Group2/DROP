from settings import *
import pygame as pg
import __init__ as init

def show_start_screen():
    # show splash / start screen
    times = 0
    color = [(255, 0, 0), (0, 0, 255)]
    color_text = [white, white, black]
    while times < 2:
        start_screen_animation(WIDTH, height, color[times], color_text[times], times)
        pg.display.flip()
        times += 1
    new_screen = pg.Surface((WIDTH, height))
    new_screen.fill((255, 255, 255))
    new_screen.set_alpha(255)
    # screen.blit(new_screen, (0, 0))
    for alpha in range(0, 255):
        new_screen.set_alpha(255 - alpha)
        draw_text('DROP!', 30, black, WIDTH / 2, height / 3)
        draw_text('Press RETURN to start the game!', 25, black, WIDTH / 2, height / 2)
        draw_text('Press ESC to exit.', 25, black, WIDTH / 2, height / 2 + 70)
        draw_text('High Score is: ' + str(highscore), 25, black, WIDTH / 2, height / 2 + 30)
        screen.blit(new_screen, (0, 0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                if not running:
                    return running
        pg.display.flip()
    running = wait_key_event_start_screen()
    return running


def start_screen_animation(width, height, color, c_text, times):
    fade = pg.Surface((width, height))
    fade.fill((0, 0, 0))
    draw_text(text_at_start[times], 65, white, WIDTH / 2, height / 2)
    for alpha in range(0, 255):
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
                running = False
                if not running:
                    return running
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    waiting = False
                    running = True
                    if running:
                        return running
                if event.key == pg.K_ESCAPE:
                    waiting = False
                    running = False
                    if not running:
                        return running

"""try:
    running = True
    while running:
        show_main_menu = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
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
    print("An error has occured within the program.")"""

