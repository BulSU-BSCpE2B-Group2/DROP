from .settings import *


class StartAnimation:
    def __init__(self):
        self.flash = pg.Surface((WIDTH, height), pg.SRCALPHA)

        self.ready = pg.image.load('bin/assets/game_screen/READY.png').convert_alpha()
        self.ready_rect = self.ready.get_rect()
        self.ready_rect.center = (WIDTH / 2, height / 2)

        self.set = pg.image.load('bin/assets/game_screen/set.png').convert_alpha()
        self.set_rect = self.set.get_rect()
        self.set_rect.center = self.ready_rect.center

        self.go = pg.image.load('bin/assets/game_screen/go.png').convert_alpha()
        self.go_rect = self.go.get_rect()
        self.go_rect.center = self.ready_rect.center

    def new(self):
        self.alpha = 255
        self.iterator = 0
        self.running = True
        self.run()

    def run(self):
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def events(self):
        pass

    def update(self):
        if self.iterator < 3:
            if self.alpha > 0:
                self.alpha -= 5
            else:
                self.alpha = 255
                self.iterator += 1
        else:
            self.running = False

    def draw(self):
        if self.iterator == 0:
            screen.blit(self.ready, self.ready_rect)
        elif self.iterator == 1:
            screen.blit(self.set, self.set_rect)
        elif self.iterator == 2:
            screen.blit(self.go, self.go_rect)

        self.flash.fill((255, 255, 255, self.alpha))
        screen.blit(self.flash, (0, 0))
        pg.display.flip()



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
