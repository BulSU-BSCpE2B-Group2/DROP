import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from start_game_screen import *
from game_over_screen import *
from pause_screen import *
from main_menu import *

RESET_SPEED_EVENT = pg.USEREVENT + 1

class Game:
    def __init__(self):
        # initialize game window, sound loader, screen and window title
        pg.init()
        pg.mixer.init()
        self.screen = screen # add pg.FULLSCREEN in settings.py if you want to full screen
        pg.display.set_caption(title)

        # load the images for background in preparation for scrolling function at draw function inside game loop
        self.bg = pg.image.load('assets/game_screen/bg-darker.png').convert_alpha()
        self.bg2 = pg.image.load('assets/game_screen/bg-darker.png').convert_alpha()
        self.bg3 = pg.image.load('assets/game_screen/bg-darker.png').convert_alpha()
        self.bg4 = pg.image.load('assets/game_screen/bg-darker.png').convert_alpha()
        self.bg_rect = self.bg.get_rect()

    def new(self):
        # starting a new game
        # set CONSTANT variables
        self.score = 0
        self.running = True
        self.slow = False
        self.multiplier = 1
        self.height_platform = 700
        self.event_interval = 5000
        self.newPlatformInterval = 100
        self.currentInterval = 0
        self.alpha = 255
        self.multiplier_powerup = 1

        # assign sprite groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.slowplatformpowerup = pg.sprite.Group()
        self.player_sprite = pg.sprite.Group()

        # for spawning the starting platforms
        for plat in platform_list:
            p = Platform(plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # assign CLASS
        self.player = Player(self)
        self.player_sprite.add(self.player)
        self.all_sprites.add(self.player)

        # assign the background used
        self.background = vec(0, 0)
        self.background2 = vec(0, self.bg_rect.height)
        self.background3 = vec(self.bg_rect.width, 0)
        self.background4 = vec(self.bg_rect.width, self.bg_rect.height)

        # load highscore data
        self.highscore = load_hs_data()

        # run the main game loop
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
        self.multiplier += 0.0005
        self.score += 1
        self.speed = 1 * self.multiplier * self.multiplier_powerup

        # if speed is more than 4, speed multiplier goes back to 0
        if self.speed >= 5:
            self.multiplier = 1

        # if slow is activated, speed is halved
        if self.slow:
            self.multiplier_powerup = 0.5

        # after slow, reset multiplier_powerup to 1
        else:
            self.multiplier_powerup = 1

        # gaps spawn algorithm
        self.gaps = random.randint(1, 6)
        self.generate = random.randint(0, 10)
        self.currentInterval += 1
        if self.currentInterval > (self.newPlatformInterval / self.speed):
            if not self.height_platform > height * 2:
                self.height_platform += 100
            sequence, rect = add_platform(self.gaps, self.height_platform)
            for x in sequence:
                if x == 1:
                    p = Platform(rect.center)
                    self.platforms.add(p)
                    self.all_sprites.add(p)
                    rect.width += 134
                else:
                    rect.width += 134

        # slow platform power up algorithm spawn
            power_up, power_up_rect = spawn_power_up(self.generate, self.height_platform)
            for n in power_up:
                if n == 1:
                    slowplatform_powerup = SlowPlatformPowerUp(power_up_rect.center)
                    self.slowplatformpowerup.add(slowplatform_powerup)
                    self.all_sprites.add(slowplatform_powerup)
                    power_up_rect.width += 134
                else:
                    power_up_rect.width += 134
            # after all that set reset current interval
            self.currentInterval = 0


        # if power up leaves the screen, kill it.
        for slowdown_platform in self.slowplatformpowerup:
            slowdown_platform.rect.y -= self.speed
            if slowdown_platform.rect.top <= -10:
                slowdown_platform.kill()

        # if platform leaves the screen, kill it.
        for platform in self.platforms:
            platform.rect.y -= self.speed
            if platform.rect.top <= -10:
                platform.kill()

        # check if player hits a power_up
        slow_down_hit = pg.sprite.spritecollide(self.player, self.slowplatformpowerup, True)
        if slow_down_hit:
            self.slow = True
            pg.time.set_timer(RESET_SPEED_EVENT, self.event_interval)

        # check if player hits a platform - only if it's falling.
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top + 3
                self.player.vel.y = 0

        # if player reaches 1/4 from the bottom of the screen, camera should follow the player position
        if self.player.rect.bottom > (height / 4) * 3:
            self.score += 1
            self.currentInterval += 4
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 10:
                    sprite.kill()

        # if player reaches spike, player dies.
        if self.player.rect.top < 0:
            self.running = False

        # over time, alpha count falls for screen flash found in draw function
        self.alpha -= 5
        if self.alpha <= 0:
            self.alpha = 0

        # set background positions, scroll diagonally
        self.background, self.background2 = scrolling_background(-2, -1, self.background, self.background2, self.bg_rect)
        self.background3, self.background4 = scrolling_background(-2, -1, self.background3, self.background4, self.bg_rect)

        # update the number of platforms, player and platform and slow_platform position
        self.player.update()
        self.platforms.update()
        self.slowplatformpowerup.update()

        # for debugging purposes, do not remove yet.
        """print("Speed is: {}".format(self.speed))
        print("Speed multiplier is: {}".format(self.multiplier))
        print("Current interval is: {}".format(self.currentInterval))"""

    def events(self):
        # Game loop for updates on inputs or whatever interaction you make inside the window
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            if event.type == RESET_SPEED_EVENT:
                self.slow = False
                pg.time.set_timer(RESET_SPEED_EVENT, 0)
            if event.type == pg.KEYDOWN:
                # if escape it should go to the game over screen
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_e:
                    # pressing 'e' should reset the game
                    self.platforms.empty()
                    self.new()
                    # pressing spaces should pause the screen
                elif event.key == pg.K_SPACE:
                    self.pause_screen()

    def draw(self):
        # Game loop for drawing graphics

        # load the background images with their relative position on screen
        screen.blit(self.bg, self.background)
        screen.blit(self.bg2, self.background2)
        screen.blit(self.bg3, self.background3)
        screen.blit(self.bg4, self.background4)

        # draw and update all existing sprites on screen
        self.slowplatformpowerup.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.platforms.draw(self.screen)

        # draw and update the score
        draw_text(str(self.score), 22, white, WIDTH / 2, 50)

        # white flash
        if self.alpha > 0:
            flash = pg.Surface((WIDTH, height), pg.SRCALPHA)
            flash.fill((255, 255, 255, self.alpha))
            screen.blit(flash, (0, 0))

        # *after* drawing everything, flip the display for changes to take effect on the window
        pg.display.flip()

    def pause_screen(self): # pause screen
        self.pause = fade_pause_animation()
        return self.pause


# turn 'g' into an object of Game class, essentially initializing pygame
g = Game()
# turn 'mm' into an object of MainMenu class
mm = MainMenu()
# loop that makes restarting work. will only be broken by break statements
while True:
    # assign show_start_screen() to run variable to tell whether the return value of show_start_screen()/
    # / is true or false
    mm.new()
    # if show_start_screen() returned false, break the loop, ending the program.
    if not mm.running:
        # else, initialize the game loop (which is the 'new' function) inside the Game class
        if mm.exit:
            break
        else:
            while True:
                # start animation sequence and initialize new game function & loop
                start_game_animation_sequence()
                g.new()
                # turn 'go' into an object of GameOver class
                go = GameOverScreen(g.score, g.highscore)
                # if player dies, game over screen runs
                go.new()
                # if you want to restart, run sets to true then loop happens all over again.
                if not go.running:
                    if go.restart:
                        continue
                # it puts you back to the outer loop, showing you the start_screen and giving you another choice to
                # start the game or completely exit.
                    else:
                        break
pg.quit()
