import random
from .settings import *

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = vec(WIDTH / 2, height / 2)
        self.vel = vec(0, 0)
        self.accel = vec(0, 0)
        self.next_frame = current_ticks()
        self.frame = 0
        self.frames = 6  # <====== frames that are contained in your gif spritesheet

        self.images = []
        img = pg.image.load('bin/assets/characters/spritesheet_astronaut.gif').convert_alpha()
        self.originalWidth = img.get_width() // self.frames
        self.originalHeight = img.get_height()

        self.x = 0
        for frameNo in range(self.frames):
            frameSurf = pg.Surface((self.originalWidth, self.originalHeight), pg.SRCALPHA, 32)
            frameSurf.blit(img, (self.x, 0))
            self.images.append(frameSurf.copy())
            self.x -= self.originalWidth
        self.image = pg.Surface.copy(self.images[0])

        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.mask = pg.mask.from_surface(self.image)
        self.angle = 0
        self.scale = 1

    def addImage(self, filename):
        self.images.append(pg.image.load(filename).convert_alpha())

    def changeImage(self, index):
        self.currentImage = index
        if self.angle == 0 and self.scale == 1:
            self.image = self.images[index]
        else:
            self.image = pg.transform.rotozoom(self.images[self.currentImage], -self.angle, self.scale)
        oldcenter = self.rect.center
        self.rect = self.image.get_rect()
        originalRect = self.images[self.currentImage].get_rect()
        self.originalWidth = originalRect.width
        self.originalHeight = originalRect.height
        self.rect.center = oldcenter
        self.mask = pg.mask.from_surface(self.image)

    def update(self, friction):
        self.accel = vec(0, player_gravity)
        # self.image.fill(self.cycle_color())
        if current_ticks() > self.next_frame:
            self.frame = (self.frame+1)%2
            self.next_frame += 100
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.accel.x = -player_accel

            # from StevePaget
            self.changeImage(1*2 + self.frame)

        elif keys[pg.K_RIGHT]:
            self.accel.x = player_accel

            # from StevePaget
            self.changeImage(2*2 + self.frame)

        else:
            self.changeImage(0*2 + self.frame)

        # kinematics equation from the settings module
        self.pos = kinematics(self.accel, self.vel, self.pos, friction)
        # wrap around the screen
        if self.pos.x > WIDTH - (player_width / 2):
            self.pos.x = WIDTH - player_width / 2
        if self.pos.x < player_width / 2:
            self.pos.x = player_width / 2

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('bin/assets/platform/platform-02.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = self.position


class SlowPlatformPowerUp(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('bin/assets/game_screen/slowplatform.png').convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (20, 22))
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = self.position


class TeleportPowerUp(pg.sprite.Sprite):
    def __init__(self, position):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10), pg.SRCALPHA)
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.center = self.position


def spawn_power_up(generate, pu_spawn_height):
    p_rect = pg.Rect(0, 0, WIDTH / 12, height + pu_spawn_height - 50)
    spawn = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    no_spawn = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if generate == 1:
        random.shuffle(spawn)
        sequence = spawn
    else:
        sequence = no_spawn
    return sequence, p_rect


def add_platform(gaps, spawn_height):
    rect = pg.Rect(0, 0, WIDTH / 12, height + spawn_height)
    gap_1 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_2 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_3 = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    gaps_4 = [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
    if gaps == 1:
        random.shuffle(gap_1)
        sequence = gap_1
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
    return sequence, rect
