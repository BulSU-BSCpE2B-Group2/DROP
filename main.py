import pygame as pg
import random
from os import path
from settings import *
from sprites import *


class Game:
    def __init__(self):
        # initialize game window, etc.
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, height)) # add pg.FULLSCREEN if you want to full screen
        pg.display.set_caption(title)
        self.clock = pg.time.Clock()
        self.running = True
        self.game_over = False
        self.font_name = pg.font.match_font(font_name)
        self.newPlatformInterval = 50
        self.currentInterval = 0
        self.load_hs_data()
        self.delay = pg.time.Clock()

    def load_hs_data(self):
        # read high score from highscore.txt
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, highscore_textfile), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        # starting a new game
        self.score = 0
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
            self.clock.tick(fps)
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
            self.game_over = True

    def events(self):
        # Game loop - EVENTS
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.show_start_screen()
                elif event.key == pg.K_r:
                    self.game_over = False
                    self.platforms.empty()
                    self.new()

    def draw(self):
        # Game loop for drawing graphics
        if not self.game_over:
            self.screen.fill(gray)
            self.all_sprites.draw(self.screen)
            self.draw_text(str(self.score), 22, white, WIDTH / 2, 50)
        else:
            self.show_go_screen()

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # show splash / start screen
        self.newwidth = self.width_loop = WIDTH
        self.newheight = self.height_loop = height
        self.animax = 0
        self.animay = 0
        rsg, rsg_text = ['red', 'yellow', 'green'], ['READY', 'SET', 'DROP!']
        rsg_count = 0
        while rsg_count < len(rsg):
            self.screen.fill(pg.color.Color(rsg[rsg_count]))
            self.draw_text(rsg_text[rsg_count], 125, white, WIDTH / 2, height / 2 - 30)
            pg.display.flip()
            pg.time.wait(500)
            rsg_count += 1

        while self.width_loop > player_width and self.height_loop > player_height:
            self.screen.fill(gray)
            pg.draw.rect(self.screen, green, [self.animax, self.animay, self.width_loop, self.height_loop])
            pg.display.flip()
            pg.time.wait(50)
            self.width_loop -= 22
            self.height_loop -= 20
            if self.animax < self.newwidth / 2.10 and self.animay < self.newheight / 2.25:
                self.animax += 11
                self.animay += 10

        #self.intrun() #sampleplay...too hard:(
        self.screen.fill(pg.color.Color('purple'))
        self.draw_text('Welcome to DROP!', 30, white, WIDTH / 2, height / 3)
        self.draw_text('Press RETURN to start the game!', 25, white, WIDTH / 2, height / 2)
        self.draw_text('Press ESC to exit.', 25, white, WIDTH / 2, height / 2 + 70)
        self.draw_text('High Score is: ' + str(self.highscore), 25, white, WIDTH / 2, height / 2 + 30)
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
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.running = False

    def show_go_screen(self):
        # show game over / continue
        self.screen.fill(dark_red)
        self.draw_text('GAME OVER', 26, white, WIDTH / 2, height / 2 - 30)
        self.draw_text('Press ESC to exit the game.', 24, white, WIDTH / 2, height / 2)
        self.draw_text('Press \'r\' to restart the game.', 24, white, WIDTH / 2, height / 2 + 30)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('New high score!', 30, white, WIDTH / 2, height / 2 + 70)
            with open(path.join(self.dir, highscore_textfile), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text('High Score is: ' + str(self.highscore), 25, white, WIDTH / 2, height / 2 + 70)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        # function for drawing the text on the screen
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def intrun(self):
        self.score = 0

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        for platform in platform_list:
            p = Platform(*platform)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.player = Player(self)
        self.all_sprites.add(self.player)

        while self.running:
            if self.score < 20:
                pass
                #automove
            else:
                # fadeout
                break

            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

        pg.display.flip()


g = Game()
g.show_start_screen()
while g.running:
    g.new()

pg.quit()
