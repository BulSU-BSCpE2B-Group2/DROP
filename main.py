import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height), pg.FULLSCREEN)
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.game_over = False
        self.font_name = pg.font.match_font(font_name)
        self.score = 0
        self.orig_pos = 0
        self.sequence = []
        self.newPlatform = 0
        self.newPlatformInterval = 100

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
        # self.newPlatform += 1
        gaps = random.randint(1, 5)
        gaps_1 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        gaps_2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        gaps_3 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        gaps_4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
        if gaps == 1:
            random.shuffle(gaps_1)
            self.sequence = gaps_1
        elif gaps == 2:
            random.shuffle(gaps_2)
            self.sequence = gaps_2
        elif gaps == 3:
            random.shuffle(gaps_3)
            self.sequence = gaps_3
        elif gaps == 4:
            random.shuffle(gaps_4)
            self.sequence = gaps_4
        else:
            random.shuffle(gaps_2)
            self.sequence = gaps_2
        for x in self.sequence:
            if x == 1:
                p = Platform(self.orig_pos, 90 + height, width / 12, 20)
                self.all_sprites.add(p)
                self.platforms.add(p)
                self.orig_pos += width / 12
            else:
                self.orig_pos += width / 12
        self.player.update()
        self.platforms.update()
        self.timePoint = pg.time.get_ticks()
        # check if player hits a platform - only if falling!
        for platform in self.platforms:
            platform.rect.y -= 2
            if platform.rect.top <= -30:
                platform.kill()

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top - 2
                self.player.vel.y = 0
        # if player reaches top 1/4 of the screen
        """if self.player.rect.top <= height / 4:
            self.player.pos.y += abs(self.player.vel.y)"""

        """if self.player.rect.bottom > (height / 4) * 3:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < -30:
                    sprite.kill()"""

        if self.player.rect.top < 0:
            self.game_over = True

        # spawn new platforms to keep same average number

        # wide = width / 8
        # p = Platform(random.randrange(0, width - wide), random.randrange(120 + height, 350 + width), wide, 20)
        """p = Platform(random.randrange(0, width / 4), 120 + height, wide, 20)
        p1 = Platform(random.randrange(100 + width / 4, width), 120 + height, wide, 20)
        self.platforms.add(p)
        self.platforms.add(p1)
        self.all_sprites.add(p)
        self.all_sprites.add(p1)"""
        """platforms_all = self.shuffle_platform(wide)
        for platform in platforms_all:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)"""



    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            """if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()"""

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
            self.screen.fill(dark_red)
            self.draw_text('GAME OVER', 26, white, width / 2, height / 2 - 30)
            self.draw_text('Press ESC to exit the game.', 24, white, width / 2, height / 2)
            self.draw_text('Press \'r\' to restart the game.', 24, white, width / 2, height / 2 + 30)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # show splash / start screen
        pass

    def show_go_screen(self):
        # show game over / continue
        pass

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
