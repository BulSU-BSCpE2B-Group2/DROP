from .settings import *


# run this as soon as the user hits enter to start the game
def start_game_animation_sequence():
    times = 0
    color = [(255, 255, 255), (255, 255, 255)]
    color_text = [black, black]
    while times < 2:
        a = start_game_animation(WIDTH, height, color[times], color_text[times], times)
        if a:
            return a
        pg.display.flip()
        times += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                if not run:
                    return run


def start_game_animation(width, height, color, c_text, times):
    fade = pg.Surface((width, height))
    draw_text(text_at_start[times], 65, white, width / 2, height / 2)
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.fill((color))
        draw_text(text_at_start[times], 65, c_text, width / 2, height / 2)
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
