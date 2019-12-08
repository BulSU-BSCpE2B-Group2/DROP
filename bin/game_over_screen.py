from .settings import *


class GameOverScreen:
    def __init__(self):
        self.screen = screen
        self.clock = pg.time.Clock()

        self.asset_dir = path.join(directory, 'assets')
        self.sound_dir = path.join(self.asset_dir, 'sounds')

        self.game_over_msg_not_hs = pg.image.load('bin/assets/game_over/game_over_msg.png').convert_alpha()
        self.game_over_msg_not_hs = pg.transform.smoothscale(self.game_over_msg_not_hs, (500, 246))
        self.game_over_msg_not_hs_rect = self.game_over_msg_not_hs.get_rect()
        self.game_over_msg_not_hs_rect.center = (WIDTH / 2, height / 2)

        self.gameover_overlay = pg.image.load('bin/assets/game_over/gameover_overlay.png').convert_alpha()
        self.gameover_overlay_rect = self.gameover_overlay.get_rect()
        self.gameover_overlay_rect.topleft = (0, 0)

        self.death_sound = pg.mixer.Sound(path.join(self.sound_dir, 'SOUND FX (DEATH).wav'))

        self.fade = pg.Surface((WIDTH, height), pg.SRCALPHA)

    def new(self, score, highscore):
        self.death_sound.play()
        self.score = score
        self.highscore = highscore
        self.alpha = 0
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.alpha < 20:
            self.alpha += 1
        else:
            self.running = self.wait_key_event()

        print(self.alpha)

    def draw(self):
        # fade to red screen
        self.fade.fill((125, 0, 0, self.alpha))
        screen.blit(self.fade, (0, 0))

        # draw text for game over screen
        screen.blit(self.game_over_msg_not_hs, self.game_over_msg_not_hs_rect)

        # if score is higher than highscore
        if self.score > self.highscore:
            draw_text('New high score!', 22, (255, 255, 255, self.alpha), WIDTH / 2, height / 2 + 300)
            with open(path.join(directory, highscore_textfile), 'w') as f:
                f.write(str(self.score))
            if self.alpha == 1:
                self.highscore = self.score

        draw_text(str(self.highscore), 30, white, WIDTH / 2 + 100, self.game_over_msg_not_hs_rect.centery - 41)

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.running = False
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.exit = True

    def wait_key_event(self):
        self.waiting = True
        while self.waiting:
            clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.restart = False
                    self.exit = True
                    return self.waiting
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        self.waiting = False
                        self.restart = True
                        self.exit = False
                        return self.waiting
                    if event.key == pg.K_ESCAPE:
                        self.waiting = False
                        self.restart = False
                        self.exit = True
                        return self.waiting
