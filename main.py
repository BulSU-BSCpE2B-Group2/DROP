import pygame as pg
import random
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.game_over = False
        self.font_name = pg.font.match_font(font_name)
        self.score = 0

    def new(self):
        # starting a new game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for platform in platform_list:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)
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
        self.all_sprites.update()
        # check if player hits a platform - only if falling!
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
        # if player reaches top 1/4 of the screen
        if self.player.rect.top <= height / 4:
            self.player.pos.y += abs(self.player.vel.y)
            for platform in self.platforms:
                platform.rect.y += abs(self.player.vel.y)
                if platform.rect.top >= height:
                    platform.kill()

        if self.player.rect.bottom > height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.game_over = True

        # spawn new platforms to keep same average number
        while len(self.platforms) < 6:
            wide = random.randrange(50, 100)
            p = Platform(random.randrange(0, width - wide), random.randrange(-75, -30), wide, 20)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            self.running = False
        if keys[pg.K_r]:
            self.game_over = False
            self.new()

    def draw(self):
        # Game loop for drawing graphics
        self.screen.fill(black)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, white, width / 2, 50)
        if self.game_over:
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
