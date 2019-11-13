# Please do not mind the messiness of the code. I am simply a beginner on Pygame and is looking for more experience
# If you do know how to make the code more efficient I am happy to entertain suggestions.
import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height)) # add pg.FULLSCREEN if you want to full screen
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.game_over = False
        self.font_name = pg.font.match_font(font_name)
        self.score = 0
        self.orig_pos = 0
        self.newPlatform = 90 + height
        self.newPlatformInterval = 100
        self.currentInterval = 0

    def new(self):
        # starting a new game
        self.score = 0
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
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop update
        # Plan here was to spawn platforms with specific number of gaps
        # The platforms has to be aligned, and has to have enough room for the ball to fall and navigate through
        # ISSUE: Platforms are hollow after the initial pre-placed platforms. Still looking into this issue
        # Open for suggestions
        self.gaps = random.randint(1, 5)
        # self.currentInterval += 1
        self.add_platform(self.gaps)
        self.player.update()
        self.platforms.update()

        # check if player hits a platform - only if falling!
        for platform in self.platforms:
            platform.rect.y -= 2
            if platform.rect.top <= -20:
                platform.kill()

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top - 2
                self.player.vel.y = 0
        # if player reaches top 1/4 of the screen
        """if self.player.rect.top <= height / 4:
            self.player.pos.y += abs(self.player.vel.y)"""

        if self.player.rect.bottom > (height / 4) * 3:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 10:
                    sprite.kill()

        if self.player.rect.top < 0:
            self.game_over = True

    def add_platform(self, gaps):
        gaps_1 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        gaps_2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        gaps_3 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        gaps_4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        if gaps == 1:
            random.shuffle(gaps_1)
            sequence = gaps_1
        elif gaps == 2:
            random.shuffle(gaps_2)
            sequence = gaps_2
        elif gaps == 3:
            random.shuffle(gaps_3)
            sequence = gaps_3
        elif gaps == 4:
            random.shuffle(gaps_4)
            sequence = gaps_4
        else:
            random.shuffle(gaps_2)
            sequence = gaps_2
        for x in sequence:
            if x == 1:
                p = Platform(self.orig_pos, self.newPlatform, width / 12, 20)
                self.platforms.add(p)
                self.all_sprites.add(p)
                self.orig_pos += width / 12
            else:
                self.orig_pos += width / 12

        # Initial plan was to spawn new platforms to keep same average number
        # wide = width / 8
        # p = Platform(random.randrange(0, width - wide), random.randrange(120 + height, 350 + width), wide, 20)
        """p = Platform(random.randrange(0, width / 4), 120 + height, wide, 20)
        p1 = Platform(random.randrange(100 + width / 4, width), 120 + height, wide, 20)
        self.platforms.add(p)
        self.platforms.add(p1)
        self.all_sprites.add(p)
        self.all_sprites.add(p1)"""

    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                elif event.key == pg.K_r:
                    self.game_over = False
                    self.platforms.empty()
                    self.new()

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.running = False
        if keys[pg.K_r]:
            self.game_over = False
            self.new()

    def draw(self):
        # Game loop for drawing graphics
        if not self.game_over:
            self.screen.fill(gray)
            self.all_sprites.draw(self.screen)
            self.draw_text(str(self.score), 22, white, width / 2, 50)
        else:
            self.show_go_screen()

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # show splash / start screen
        self.screen.fill(pg.color.Color('purple'))
        self.draw_text('Welcome to DROP!', 30, white, width/2, height/3)
        self.draw_text('Press RETURN to start the game!', 25, white, width/2, height/2)
        pg.display.flip()
        self.wait_key_event()

    def wait_key_event(self):
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        waiting = False

    def show_go_screen(self):
        # show game over / continue
        self.screen.fill(dark_red)
        self.draw_text('GAME OVER', 26, white, width / 2, height / 2 - 30)
        self.draw_text('Press ESC to exit the game.', 24, white, width / 2, height / 2)
        self.draw_text('Press \'r\' to restart the game.', 24, white, width / 2, height / 2 + 30)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        # function for drawing the text on the screen
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()

pg.quit()
