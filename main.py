from bin import *
import random


class Game:
    def __init__(self):
        self.screen = screen     # add pg.FULLSCREEN in settings.py if you want to full screen

        # load the images for background in preparation for scrolling function at draw function inside game loop
        self.bg = pg.image.load('bin/assets/game_screen/bg-darker.png').convert_alpha()
        self.bg2 = pg.image.load('bin/assets/game_screen/bg-darker.png').convert_alpha()
        self.bg3 = pg.image.load('bin/assets/game_screen/bg-darker.png').convert_alpha()
        self.bg4 = pg.image.load('bin/assets/game_screen/bg-darker.png').convert_alpha()
        self.bg_rect = self.bg.get_rect()

        # load the image for spikes
        self.spikes = pg.image.load('bin/assets/game_screen/spikes.png').convert_alpha()
        self.spikes_rect = self.spikes.get_rect()
        self.spikes_rect.topleft = (0, 0)

        # will be used later for loading
        self.slow_indicator = pg.Surface((WIDTH, height), pg.SRCALPHA)
        self.slow_indicator.fill((0, 0, 125, 30))

        # load sounds
        self.asset_dir = path.join(directory, 'assets')
        self.sound_dir = path.join(self.asset_dir, 'sounds')
        self.damaged_sound = pg.mixer.Sound(path.join(self.sound_dir, 'DAMAGED.wav'))

    def new(self, mute):
        # starting a new game
        # set CONSTANT variables
        self.mute = mute    # mute checker
        self.score = 0
        self.running = True
        self.slow = False
        self.teleport = False
        self.exit = False
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
        self.teleportpowerup = pg.sprite.Group()

        self.spikes = pg.sprite.Group()
        self.spike = Spikes((0, 0))
        self.spikes.add(self.spike)

        # for spawning the starting platforms
        for plat in platform_list:
            p = Platform(plat)
            self.all_sprites.add(p)
            self.platforms.add(p)

        # assign CLASS
        self.player = Player(self)
        self.player_sprite.add(self.player)
        self.all_sprites.add(self.player)

        self.pause = PauseScreen()
        self.pause.exit = False

        self.cnfrm_ext = ConfirmExitScreen()
        self.cnfrm_ext.exit = False

        self.go = GameOverScreen()
        self.go.exit = False

        # assign the background used
        self.background = vec(0, 0)
        self.background2 = vec(0, self.bg_rect.height)
        self.background3 = vec(self.bg_rect.width, 0)
        self.background4 = vec(self.bg_rect.width, self.bg_rect.height)

        # load highscore data
        self.highscore = load_hs_data()

        # load the background music
        pg.mixer.music.load(path.join(self.sound_dir, 'IN-GAME BGM.mp3'))

        # run the main game loop
        self.run()

    def run(self):
        # Game loop
        if not self.mute:
            pg.mixer.music.play(loops=-1)
        while self.running:
            clock.tick(fps)
            self.events()
            self.update()
            self.draw()
        if not self.mute:
            pg.mixer.music.fadeout(500)

    def update(self):
        # game loop update
        # initialize variables needed for the function
        self.multiplier += 0.0005
        self.score += 1
        self.speed = 1 * self.multiplier * self.multiplier_powerup

        # if speed is more than 4, speed multiplier goes back to 0
        if self.speed >= 3.3:
            self.multiplier = 1

        if 0 < self.speed < 1:
            self.friction = player_friction
        if 1 < self.speed < 2:
            self.friction = -0.07
        if 2 < self.speed < 3:
            self.friction = -0.05
        if 3 < self.speed < 4:
            self.friction = -0.04

        # if slow is activated, speed is halved
        if self.slow:
            self.multiplier_powerup = 0.5

        # after slow, reset multiplier_powerup to 1
        else:
            self.multiplier_powerup = 1

        # gaps spawn algorithm
        self.gaps = random.randint(1, 6)
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

            # slow platform power up spawn algorithm
            self.generate_slow_platform = random.randint(0, 10)
            power_up, power_up_rect = spawn_power_up(self.generate_slow_platform, self.height_platform)
            for n in power_up:
                if n == 1:
                    slowplatform_powerup = SlowPlatformPowerUp(power_up_rect.center)
                    self.slowplatformpowerup.add(slowplatform_powerup)
                    self.all_sprites.add(slowplatform_powerup)
                    power_up_rect.width += 134
                else:
                    power_up_rect.width += 134

            # tp power up spawn algorithm
            self.generate_tp_powerup = random.randint(0, 8)
            tp_power_up, tp_power_up_rect = spawn_power_up(self.generate_tp_powerup, self.height_platform)
            for s in tp_power_up:
                if s == 1:
                    tpplatform_powerup = TeleportPowerUp(tp_power_up_rect.center)
                    self.teleportpowerup.add(tpplatform_powerup)
                    self.all_sprites.add(tpplatform_powerup)
                    tp_power_up_rect.width += 134
                else:
                    tp_power_up_rect.width += 134

            # after all that reset current interval to 0
            self.currentInterval = 0

        # if power up leaves the screen, kill it.
        for slowdown_platform in self.slowplatformpowerup:
            slowdown_platform.rect.y -= self.speed
            if slowdown_platform.rect.top <= -10:
                slowdown_platform.kill()

        for tp_pu in self.teleportpowerup:
            tp_pu.rect.y -= self.speed
            if tp_pu.rect.top <= -10:
                tp_pu.kill()

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

        teleport_hit = pg.sprite.spritecollide(self.player, self.teleportpowerup, True)
        if teleport_hit:
            pg.time.set_timer(TELEPORT_EVENT, 1)

        # check if player hits a platform - only if it's falling.
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False, pg.sprite.collide_mask)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # if player reaches 1/4 of the area from the bottom of the screen, camera should follow the player position
        if self.player.rect.bottom > (height / 4) * 3:
            self.score += 1
            self.currentInterval += 4
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if self.player.rect.bottom > height + 100:
            self.score += 30
            self.player.pos = vec(self.player.pos.x, height - height / 8)

        # teleport checker
        if self.teleport:
            self.player.pos = vec(self.player.pos.x, self.player.pos.y + 80)
            self.teleport = False

        # if player reaches spike, player dies.
        if self.score > 10:
            spike_hit = pg.sprite.spritecollide(self.player, self.spikes, False, pg.sprite.collide_mask)
            if spike_hit:
                self.damaged_sound.play()
                for player in self.player_sprite:
                    player.kill()
                self.game_over()

        # over time, alpha count falls for screen flash found in draw function
        self.alpha -= 5
        if self.alpha <= 0:
            self.alpha = 0

        # set background positions, scroll diagonally
        self.background, self.background2 = scrolling_background(-2, -1, self.background, self.background2, self.bg_rect)
        self.background3, self.background4 = scrolling_background(-2, -1, self.background3, self.background4, self.bg_rect)

        # update the number of platforms, player and platform and slow_platform position
        self.player.update(self.friction)
        self.platforms.update()
        self.slowplatformpowerup.update()
        self.teleportpowerup.update()
        self.spikes.update()

    def events(self):
        # Game loop for updates on inputs or whatever interaction you make inside the window
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                self.running = False
                self.exit = True
            if event.type == RESET_SPEED_EVENT:
                self.slow = False
                pg.time.set_timer(RESET_SPEED_EVENT, 0)
            if event.type == TELEPORT_EVENT:
                # self.player.pos = vec(self.player.pos.x, self.player.pos.y + 120)
                self.teleport = True
                pg.time.set_timer(TELEPORT_EVENT, 0)
            if event.type == pg.KEYDOWN:
                # if escape it should go to the confirm exit screen
                if event.key == pg.K_ESCAPE:
                    self.confirm_exit()
                # pressing spaces should pause the screen
                elif event.key == pg.K_SPACE:
                    self.pause_screen()

        if self.pause.exit:
            self.running = False

        if self.cnfrm_ext.exit:
            self.running = False

    def draw(self):
        # Game loop for drawing graphics

        # load the background images with their relative position on screen
        screen.blit(self.bg, self.background)
        screen.blit(self.bg2, self.background2)
        screen.blit(self.bg3, self.background3)
        screen.blit(self.bg4, self.background4)

        # draw and update all existing sprites on screen
        self.teleportpowerup.draw(self.screen)
        self.slowplatformpowerup.draw(self.screen)
        self.player_sprite.draw(self.screen)
        self.platforms.draw(self.screen)
        self.spikes.draw(self.screen)

        # draw and update the score
        draw_text('SCORE: ' + str(self.score), 22, white, WIDTH / 2, 75)

        # white flash
        if self.alpha > 0:
            flash = pg.Surface((WIDTH, height), pg.SRCALPHA)
            flash.fill((255, 255, 255, self.alpha))
            screen.blit(flash, (0, 0))

        if self.slow:
            screen.blit(self.slow_indicator, (0, 0))

        # *after* drawing everything, flip the display for changes to take effect on the window
        pg.display.flip()

    def pause_screen(self):  # pause screen
        self.pause.new()

    def confirm_exit(self):
        self.cnfrm_ext.new()

    def game_over(self):
        self.go.new(self.score, self.highscore)
        if self.go.exit:
            self.running = False
            self.exit = True
        else:
            self.running = False
            self.exit = False


# turn 'mm' into an object of MainMenu class
mm = MainMenu()
# turn 'g' into an object of Game class, essentially initializing pygame
g = Game()
# turn 'c' into an object of Credits class
c = Credits()
# loop that makes restarting work. will only be broken by break statements
start_animation = StartAnimation()
g.mute = False
c.new()
while True:
    # assign show_start_screen() to run variable to tell whether the return value of show_start_screen()/
    # / is true or false
    mm.new(g.mute)
    # if show_start_screen() returned false, break the loop, ending the program.
    if not mm.running:
        # else, initialize the game loop (which is the 'new' function) inside the Game class
        if mm.exit:
            break
        else:
            while True:
                # start animation sequence and initialize new game function & loop
                start_animation.new()
                g.new(mm.mute)
                # turn 'go' into an object of GameOver class
                if not g.pause.exit and not g.cnfrm_ext.exit and not g.running:
                    if g.exit or not g.go.restart:
                        break
                    else:
                        continue
                else:
                    break
pg.quit()
