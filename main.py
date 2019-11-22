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
        # initialize variables needed for the function
        self.multiplier += 0.0001
        self.score += 1
        self.height_platform = 2
        speed = 2 * self.multiplier
        # if speed is more than 4, speed multiplier goes back to 0
        if speed > 4:
            self.multiplier = 1
        # gaps spawn function
        self.gaps = random.randint(1, 6)
        self.currentInterval += 1
        if self.currentInterval * self.multiplier > self.newPlatformInterval:
            if not self.height_platform > 6:
                self.height_platform += 1
            sequence, rect = add_platform(self.gaps, self.height_platform)
            for x in sequence:
                if x == 1:
                    p = Platform(rect.center, (67, 20))
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                    rect.width += 134
                else:
                    rect.width += 134
            self.currentInterval = 0
        # update number of platforms, update the player position
        self.player.update()
        self.platforms.update()

        # if platform leaves the screen, kill it.
        for platform in self.platforms:
            platform.rect.y -= speed
            if platform.rect.top <= -20:
                platform.kill()

        # check if player hits a platform - only if falling!
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top - speed
                self.player.vel.y = 0

        # if player reaches 1/4 from the bottom of the screen, camera should follow the player position
        if self.player.rect.bottom > (height / 4) * 3:
            self.score += 1
            self.currentInterval += 4
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 20)
                if sprite.rect.bottom < 10:
                    sprite.kill()

        # if player reaches spike, player dies.
        if self.player.rect.top < 0:
            self.running = False

    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                # if escape it should go to the game over screen
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_e:
                    # pressing 'e' should reset the game
                    self.platforms.empty()
                    self.new()
                # soon! pause feature.
                elif event.key == pg.K_SPACE:
                    # self.pause_screen()
                    pass

    def draw(self):
        # Game loop for drawing graphics
        # the background is gray, will add animated background soon!
        self.screen.fill(gray)
        # draw and update all existing sprites on screen
        self.all_sprites.draw(self.screen)
        # draw and update the score
        draw_text(str(self.score), 22, white, WIDTH / 2, 50)
        # *after* drawing everything, flip the display for changes to take effect on the window
        pg.display.flip()

    def pause_screen(self): # does not work yet, will edit soon!
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


# turn 'g' into an object of Game class, essentially initializing pygame
g = Game()
# loop that makes restarting work. will only be broken by break statements
while True:
    # assign show_start_screen() to run variable to tell whether the return value of show_start_screen()/
    # / is true or false
    run = show_start_screen()
    # if show_start_screen() returned false, break the loop, ending the program.
    if not run:
        break
    # else, initialize the game loop (which is the 'new' function) inside the Game class
    else:
        while run:
            g.new()
            # if player dies, game over screen shows, show_go_screen tells restart whether or not it wants to
            # restart or not (True or False statement gate again)
            restart = show_go_screen(g.score, g.highscore)
            # if you want to restart, run sets to true then loop happens all over again.
            if restart:
                run = True
            # it puts you back to the outer loop, showing you the start_screen and giving you another choice to
            # start the game or completely exit.
            else:
                break
pg.quit()
