from settings import *
import pygame as pg

highscore = load_hs_data()


def show_go_screen(score, highscore):
    go_screen_animation(WIDTH, height, dark_red, score, highscore)
    run = wait_key_event_go_screen()
    return run


def go_screen_animation(width, height, color, score, highscore):
    fade = pg.Surface((width, height))
    for alpha in range(0, 255):
        fade.fill((color))
        draw_text('GAME OVER', 26, white, WIDTH / 2, height / 2 - 30)
        draw_text('Press ESC to exit the game.', 24, white, WIDTH / 2, height / 2)
        draw_text('Press \'r\' to restart the game.', 24, white, WIDTH / 2, height / 2 + 30)
        if score > highscore:
            draw_text('New high score!', 30, white, WIDTH / 2, height / 2 + 70)
            with open(path.join(dir, highscore_textfile), 'w') as f:
                f.write(str(score))
        else:
            draw_text('High Score is: ' + str(highscore), 25, white, WIDTH / 2, height / 2 + 70)
        fade.set_alpha(255 - alpha)
        screen.blit(fade, (0, 0))
        pg.display.flip()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return running
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pass


def wait_key_event_go_screen():
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                waiting = False
                return waiting
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return waiting
                if event.key == pg.K_ESCAPE:
                    waiting = False
                    return waiting
