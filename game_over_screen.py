from settings import *
import pygame as pg


class GameOverScreen:
    def __init__(self, score, highscore):
        self.screen = screen
        self.clock = pg.time.Clock()
        self.score = score
        self.highscore = highscore

    def new(self):
        self.alpha = 0
        self.running = True
        self.restart = False
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.alpha < 255:
            self.alpha += 1

    def draw(self):
        # fade to red screen
        fade = pg.Surface((WIDTH, height), pg.SRCALPHA)
        fade.fill((125, 0, 0, self.alpha))
        screen.blit(fade, (0, 0))

        # draw text for game over screen
        draw_text('GAME OVER', 26, (255, 255, 255, self.alpha), WIDTH / 2, height / 2 - 30)
        draw_text('Press ESC to exit the game.', 24, (255, 255, 255, self.alpha), WIDTH / 2, height / 2)
        draw_text('Press \'r\' to restart the game.', 24, (255, 255, 255, self.alpha), WIDTH / 2, height / 2 + 30)

        # if score is higher than highscore
        if self.score > self.highscore:
            draw_text('New high score!', 22, (255, 255, 255, self.alpha), WIDTH / 2, height / 2 + 70)
            with open(path.join(directory, highscore_textfile), 'w') as f:
                f.write(str(self.score))
            pg.display.flip()
        else:
            draw_text('High Score is: ' + str(self.highscore), 22, white, WIDTH / 2, height / 2 + 70)
            pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.restart = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.running = False
                    self.restart = True
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.restart = False
