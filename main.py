import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from start_screen import *
from game_over_screen import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = screen # add pg.FULLSCREEN if you want to full screen
        pg.display.set_caption(title)
        self.newPlatformInterval = 50
        self.currentInterval = 0
        self.highscore = load_hs_data()
        self.running = True

    def new(self):
        # starting a new game
        self.score = 0
        self.running = True
        self.multiplier = 1
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        for platform in platform_list:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.player = Player(self)
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # Game loop
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop update
        self.multiplier += 0.0001
        self.score += 1
        speed = 2 * self.multiplier
        if speed > 4:
            self.multiplier = 1
        self.gaps = random.randint(1, 6)
        self.currentInterval += 1
        if self.currentInterval * self.multiplier > self.newPlatformInterval:
            sequence, rect = add_platform(self.gaps)
            for x in sequence:
                if x == 1:
                    p = Platform(rect.center, (67, 20))
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                    rect.width += 134
                else:
                    rect.width += 134
            self.currentInterval = 0
        self.player.update()
        self.platforms.update()

        # check if player hits a platform - only if falling!
        for platform in self.platforms:
            platform.rect.y -= speed
            if platform.rect.top <= -20:
                platform.kill()

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top - speed
                self.player.vel.y = 0

        # if player reaches 1/4 from the bottom of the screen
        if self.player.rect.bottom > (height / 4) * 3:
            self.score += 1
            self.currentInterval += 4
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 10:
                    sprite.kill()

        if self.player.rect.top < 0:
            self.running = False

    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_e:
                    self.platforms.empty()
                    self.new()
                elif event.key == pg.K_SPACE:
                    # self.pause_screen()
                    pass

    def draw(self):
        # Game loop for drawing graphics
        self.screen.fill(gray)
        self.all_sprites.draw(self.screen)
        draw_text(str(self.score), 22, white, WIDTH / 2, 50)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def pause_screen(self):
        pause = True
        while pause:
            clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pause = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        pause = False
                    if event.key == pg.K_ESCAPE:
                        self.running = False


g = Game()
while True:
    run = show_start_screen()
    if not run:
        break
    else:
        while run and g.running:
            g.new()
            restart = show_go_screen(g.score, g.highscore)
            if restart:
                g.running = True
            else:
                break
pg.quit()
