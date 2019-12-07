from .settings import *
from .credits import *

vec = pg.math.Vector2


class MainMenu:
    def __init__(self):
        # initialize game window, sound loader, screen and window title
        pg.mixer.pre_init(44100, -16, 2, 2048)
        pg.mixer.init()
        pg.init()
        pg.display.set_caption(title)
        self.screen = screen

        # initialize background 1 & 2
        self.bg = pg.image.load('bin/assets/main_menu/bg-darker-ingame.png').convert_alpha()
        self.bg2 = pg.image.load('bin/assets/main_menu/bg-darker-ingame.png').convert_alpha()
        self.bg_rect = self.bg.get_rect()

        # initialize the required classes
        self.logo = Logo()
        self.planet_venus = PlanetVenus()
        self.planet_earth = PlanetEarth()
        self.planet_mars = PlanetMars()
        self.button = Buttons()
        self.settings_screen = SettingsScreen()
        self.comets = Comets()
        self.how_to_play = HowToPlay()

        # initialize the required sounds
        self.sound_dir = path.join(directory, 'assets\\sounds')
        self.item_select = pg.mixer.Sound(path.join(self.sound_dir, 'BUTTON SELECT.wav'))

        self.mute = False


    def new(self, mute):
        self.mute = mute
        self.running = True
        self.timer = 0
        self.alpha = 0
        self.alpha_settings = 0
        self.show_settings = False
        self.background = vec(0, 0)
        self.background2 = vec(self.bg_rect.width, 0)
        # create the instance where the glow is positioned
        self.planet_mars.glow_new(self.timer)
        self.planet_venus.glow_new(self.timer)
        self.planet_earth.glow_new(self.timer)
        # load the background music
        pg.mixer.music.load(path.join(self.sound_dir, 'MAIN MENU BGM (SUGGESTION 2).mp3'))
        self.run()

    def run(self):
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
        if self.show_settings:
            if self.alpha < 100:
                self.alpha += 1
            if self.alpha_settings < 255:
                self.alpha_settings += 10
        self.background, self.background2 = scrolling_background(-2, 0, self.background, self.background2, self.bg_rect)
        self.mouse_coordinate = vec(pg.mouse.get_pos())
        # print("Mouse coordinate is at: {}".format(self.mouse_coordinate))
        self.planet_mars.glow_update()
        self.planet_venus.glow_update()
        self.planet_earth.glow_update()

    def draw(self):
        screen.blit(self.bg, self.background)
        screen.blit(self.bg2, self.background2)
        screen.blit(self.comets.comets_glow, self.comets.comets_glow_rect)
        screen.blit(self.comets.comets, self.comets.comets_rect)
        screen.blit(self.planet_mars.mars, self.planet_mars.mars_rect)
        screen.blit(self.planet_mars.mars_glow, self.planet_mars.mars_glow_rect)
        screen.blit(self.planet_venus.venus_glow, self.planet_venus.venus_glow_rect)
        screen.blit(self.planet_venus.venus, self.planet_venus.venus_rect)
        screen.blit(self.planet_earth.earth_glow, self.planet_earth.earth_glow_rect)
        screen.blit(self.planet_earth.earth, self.planet_earth.earth_rect)
        screen.blit(self.logo.logo, self.logo.position)

        # hover checker for settings button
        screen.blit(self.button.settings_button, self.button.settings_button_rect)

        if self.mouse_coordinate[0] > self.button.settings_button_rect.x:
            if self.mouse_coordinate[
                0] < self.button.settings_button_rect.x + self.button.settings_button_rect.width:
                if self.mouse_coordinate[1] > self.button.settings_button_rect.y:
                    if self.mouse_coordinate[
                        1] < self.button.settings_button_rect.y + self.button.settings_button_rect.height:
                        # 400 x 88 is proportional to the rect size of the settings button
                        self.button.settings_button_enlarged = pg.transform.smoothscale(self.button.settings_button, (140, 140))
                        self.button.settings_button_enlarged_rect = self.button.settings_button_enlarged.get_rect()
                        self.button.settings_button_enlarged_rect.center = self.button.settings_button_rect.center
                        screen.blit(self.button.settings_button_enlarged, self.button.settings_button_enlarged_rect)
                        draw_text('Settings', 25, white, self.button.settings_button_rect.centerx, height / 2 - 10)

        # hover checker for start button
        screen.blit(self.button.start_button, self.button.start_button_rect)

        if self.mouse_coordinate[0] > self.button.start_button_rect.x:
            if self.mouse_coordinate[
                0] < self.button.start_button_rect.x + self.button.start_button_rect.width:
                if self.mouse_coordinate[1] > self.button.start_button_rect.y:
                    if self.mouse_coordinate[
                        1] < self.button.start_button_rect.y + self.button.start_button_rect.height:
                        # 400 x 89 is proportional to the rect size of the start button
                        self.button.start_button_enlarged = pg.transform.smoothscale(self.button.start_button,
                                                                                        (140, 140))
                        self.button.start_button_enlarged_rect = self.button.start_button_enlarged.get_rect()
                        self.button.start_button_enlarged_rect.center = self.button.start_button_rect.center
                        screen.blit(self.button.start_button_enlarged, self.button.start_button_enlarged_rect)
                        draw_text('Play', 25, white, self.button.start_button_rect.centerx,
                                  height / 2 - 10)


        # hover checker for exit button
        screen.blit(self.button.exit_button, self.button.exit_button_rect)

        if self.mouse_coordinate.x > self.button.exit_button_rect.x:
            if self.mouse_coordinate.x < self.button.exit_button_rect.x + self.button.exit_button_rect.width:
                if self.mouse_coordinate.y > self.button.exit_button_rect.y:
                    if self.mouse_coordinate.y < self.button.exit_button_rect.y + self.button.exit_button_rect.height:
                        self.button.exit_button_enlarged = pg.transform.smoothscale(self.button.exit_button,
                                                                                     (140, 140))
                        self.button.exit_button_enlarged_rect = self.button.exit_button_enlarged.get_rect()
                        self.button.exit_button_enlarged_rect.center = self.button.exit_button_rect.center
                        screen.blit(self.button.exit_button_enlarged, self.button.exit_button_enlarged_rect)

        # hover checker for credits button
        screen.blit(self.button.credits_button, self.button.credits_button_rect)

        if self.mouse_coordinate.x > self.button.credits_button_rect.x:
            if self.mouse_coordinate.x < self.button.credits_button_rect.x + self.button.credits_button_rect.width:
                if self.mouse_coordinate.y > self.button.credits_button_rect.y:
                    if self.mouse_coordinate.y < self.button.credits_button_rect.y + self.button.credits_button_rect.height:
                        self.button.credits_button_enlarged = pg.transform.smoothscale(self.button.credits_button,
                                                                                     (140, 140))
                        self.button.credits_button_enlarged_rect = self.button.credits_button_enlarged.get_rect()
                        self.button.credits_button_enlarged_rect.center = self.button.credits_button_rect.center
                        screen.blit(self.button.credits_button_enlarged, self.button.credits_button_enlarged_rect)
                        draw_text('Credits', 25, white, self.button.credits_button_rect.centerx, height/2 - 10)

        # hover checker for how-to button
        screen.blit(self.button.how_to_button, self.button.how_to_button_rect)

        if self.mouse_coordinate.x > self.button.how_to_button_rect.x:
            if self.mouse_coordinate.x < self.button.how_to_button_rect.x + self.button.how_to_button_rect.width:
                if self.mouse_coordinate.y > self.button.how_to_button_rect.y:
                    if self.mouse_coordinate.y < self.button.how_to_button_rect.y + self.button.how_to_button_rect.height:
                        self.button.how_to_button_enlarged = pg.transform.smoothscale(self.button.how_to_button,
                                                                                     (140, 140))
                        self.button.how_to_button_enlarged_rect = self.button.how_to_button_enlarged.get_rect()
                        self.button.how_to_button_enlarged_rect.center = self.button.how_to_button_rect.center
                        screen.blit(self.button.how_to_button_enlarged, self.button.how_to_button_enlarged_rect)
                        draw_text('How To Play', 25, white, self.button.how_to_button_rect.centerx, height / 2 - 10)

        if self.show_settings:
            settings_overlay_with_opacity = pg.Surface((WIDTH, height), pg.SRCALPHA)
            settings_overlay_with_opacity.fill((100, 100, 100, self.alpha))
            screen.blit(settings_overlay_with_opacity, (0, 0))
            screen.blit(self.settings_screen.settings_overlay, self.settings_screen.settings_overlay_rect)
            screen.blit(self.settings_screen.x, self.settings_screen.x_rect)

            if self.mouse_coordinate.x > self.settings_screen.x_rect.x:
                if self.mouse_coordinate.x < self.settings_screen.x_rect.x + self.settings_screen.x_rect.width:
                    if self.mouse_coordinate.y > self.settings_screen.x_rect.y:
                        if self.mouse_coordinate.y < self.settings_screen.x_rect.y + self.settings_screen.x_rect.height:
                            self.settings_screen.x_rect_enlarged = pg.transform.smoothscale(self.settings_screen.x,
                                                                                          (115, 108))
                            self.settings_screen.x_rect_enlarged_rect = self.settings_screen.x_rect_enlarged.get_rect()
                            self.settings_screen.x_rect_enlarged_rect.center = self.settings_screen.x_rect.center
                            screen.blit(self.settings_screen.x_rect_enlarged, self.settings_screen.x_rect_enlarged_rect)

            if not self.mute:
                screen.blit(self.settings_screen.music_option_on, self.settings_screen.music_option_on_rect)
            else:
                screen.blit(self.settings_screen.music_option_off, self.settings_screen.music_option_off_rect)


        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.exit = True
            if self.show_settings:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.show_settings = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.mouse_coordinate.x > self.settings_screen.settings_overlay_rect.x + 562:
                        if self.mouse_coordinate.x < self.settings_screen.settings_overlay_rect.x + 652:
                            if self.mouse_coordinate.y > self.settings_screen.settings_overlay_rect.y:
                                if self.mouse_coordinate.y < self.settings_screen.settings_overlay_rect.y + 93:
                                    self.show_settings = False
                                    self.item_select.play()
                    if not self.mute:
                        if self.mouse_coordinate.x > self.settings_screen.music_option_off_rect.x:
                            if self.mouse_coordinate.x < self.settings_screen.music_option_off_rect.x + self.settings_screen.music_option_off_rect.width:
                                if self.mouse_coordinate.y > self.settings_screen.music_option_off_rect.y:
                                    if self.mouse_coordinate.y < self.settings_screen.music_option_off_rect.y + self.settings_screen.music_option_off_rect.height:
                                        self.mute = True
                                        self.item_select.play()
                                        pg.mixer.music.stop()
                    else:
                        if self.mouse_coordinate.x > self.settings_screen.music_option_on_rect.x:
                            if self.mouse_coordinate.x < self.settings_screen.music_option_on_rect.x + self.settings_screen.music_option_on_rect.width:
                                if self.mouse_coordinate.y > self.settings_screen.music_option_on_rect.y:
                                    if self.mouse_coordinate.y < self.settings_screen.music_option_on_rect.y + self.settings_screen.music_option_on_rect.height:
                                        self.mute = False
                                        self.item_select.play()
                                        pg.mixer.music.play(loops=-1)

            else:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.mouse_coordinate[0] > self.button.start_button_rect.x:
                        if self.mouse_coordinate[
                            0] < self.button.start_button_rect.x + self.button.start_button_rect.width:
                            if self.mouse_coordinate[1] > self.button.start_button_rect.y:
                                if self.mouse_coordinate[
                                    1] < self.button.start_button_rect.y + self.button.start_button_rect.height:
                                    self.running = False
                                    self.exit = False
                                    self.item_select.play()
                    if self.mouse_coordinate[0] > self.button.settings_button_rect.x:
                        if self.mouse_coordinate[
                            0] < self.button.settings_button_rect.x + self.button.settings_button_rect.width:
                            if self.mouse_coordinate[1] > self.button.settings_button_rect.y:
                                if self.mouse_coordinate[
                                    1] < self.button.settings_button_rect.y + self.button.settings_button_rect.height:
                                    self.alpha = 0
                                    self.alpha_settings = 0
                                    self.show_settings = True
                                    self.item_select.play()
                    if self.mouse_coordinate.x > self.button.exit_button_rect.x:
                        if self.mouse_coordinate.x < self.button.exit_button_rect.x + self.button.exit_button_rect.width:
                            if self.mouse_coordinate.y > self.button.exit_button_rect.y:
                                if self.mouse_coordinate.y < self.button.exit_button_rect.y + self.button.exit_button_rect.height:
                                    self.running = False
                                    self.exit = True
                                    self.item_select.play()
                    if self.mouse_coordinate.x > self.button.credits_button_rect.x:
                        if self.mouse_coordinate.x < self.button.credits_button_rect.x + self.button.credits_button_rect.width:
                            if self.mouse_coordinate.y > self.button.credits_button_rect.y:
                                if self.mouse_coordinate.y < self.button.credits_button_rect.y + self.button.credits_button_rect.height:
                                    self.item_select.play()
                                    c = Credits()
                                    c.new()

class Logo:
    def __init__(self):
        self.logo = pg.image.load('bin/assets/main_menu/TITLE.png').convert_alpha()
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.center = (WIDTH / 2, height / 2)
        self.position = vec(WIDTH / 2 - self.logo_rect.top, (height / 2) - self.logo_rect.left - 130)


class PlanetVenus:
    def __init__(self):
        self.venus = pg.image.load('bin/assets/main_menu/4.png').convert_alpha()
        self.venus_rect = self.venus.get_rect()
        self.venus_glow = pg.image.load('bin/assets/main_menu/3.png').convert_alpha()
        self.venus_glow_rect = self.venus_glow.get_rect()
        # set position for the planet mars and its glow
        self.position = (WIDTH / 9, height / 2 + 70)
        self.venus_rect.center = self.position
        self.venus_glow_rect.center = self.venus_rect.center

    def glow_new(self, timer):
        self.timer = timer
        self.scale_size_x = self.venus_glow_rect.width
        self.scale_size_y = self.venus_glow_rect.height

    def glow_update(self):
        self.venus_glow, self.venus_glow_rect, self.timer, self.scale_size_x, self.scale_size_y = grow_shrink(
            'bin/assets/main_menu/3.png',
            150,
            self.position,
            self.timer,
            self.scale_size_x,
            self.scale_size_y)


class PlanetEarth:
    def __init__(self):
        self.earth = pg.image.load('bin/assets/main_menu/2.png').convert_alpha()
        self.earth_rect = self.earth.get_rect()
        self.earth_glow = pg.image.load('bin/assets/main_menu/1.png').convert_alpha()
        self.earth_glow_rect = self.earth_glow.get_rect()
        # set position for the planet earth and its glow
        self.position = (WIDTH / 4, height / 4 - 50)
        self.earth_rect.center = self.position
        self.earth_glow_rect.center = self.earth_rect.center

    def glow_new(self, timer):
        self.timer = timer
        self.scale_size_x = self.earth_glow_rect.width
        self.scale_size_y = self.earth_glow_rect.height

    def glow_update(self):
        self.earth_glow, self.earth_glow_rect, self.timer, self.scale_size_x, self.scale_size_y = grow_shrink(
            'bin/assets/main_menu/1.png',
            50,
            self.position,
            self.timer,
            self.scale_size_x,
            self.scale_size_y)


class PlanetMars:
    def __init__(self):
        self.mars = pg.image.load('bin/assets/main_menu/6.png').convert_alpha()
        self.mars_rect = self.mars.get_rect()
        self.mars_glow = pg.image.load('bin/assets/main_menu/5.png').convert_alpha()
        self.mars_glow_rect = self.mars_glow.get_rect()
        self.position_glow = (WIDTH - WIDTH / 8 + 6, height / 8 + 2)
        self.mars_rect.center = (WIDTH - WIDTH / 8, height / 8)
        self.mars_glow_rect.center = self.position_glow

    def glow_new(self, timer):
        self.timer = timer
        self.scale_size_x = self.mars_glow_rect.width
        self.scale_size_y = self.mars_glow_rect.height

    def glow_update(self):
        self.mars_glow, self.mars_glow_rect, self.timer, self.scale_size_x, self.scale_size_y = grow_shrink(
            'bin/assets/main_menu/5.png',
            100,
            self.position_glow,
            self.timer,
            self.scale_size_x,
            self.scale_size_y)


class Buttons:
    def __init__(self):
        # initialize asset for settings button
        self.settings_button = pg.image.load('bin/assets/main_menu/settingss.png').convert_alpha()
        self.settings_button = pg.transform.smoothscale(self.settings_button, (120, 120))
        self.settings_button_rect = self.settings_button.get_rect()
        # initialize asset for start button
        self.start_button = pg.image.load('bin/assets/main_menu/play.png').convert_alpha()
        self.start_button = pg.transform.smoothscale(self.start_button, (120, 120))
        self.start_button_rect = self.start_button.get_rect()
        # initialize asset for exit button
        self.exit_button = pg.image.load('bin/assets/main_menu/exit.png').convert_alpha()
        self.exit_button = pg.transform.smoothscale(self.exit_button, (120, 120))
        self.exit_button_rect = self.exit_button.get_rect()
        # initialize asset for how-to button
        self.how_to_button = pg.image.load('bin/assets/main_menu/how-to-play.png').convert_alpha()
        self.how_to_button = pg.transform.smoothscale(self.how_to_button, (120, 120))
        self.how_to_button_rect = self.how_to_button.get_rect()
        # initialize asset for credits button
        self.credits_button = pg.image.load('bin/assets/main_menu/credits.png').convert_alpha()
        self.credits_button = pg.transform.smoothscale(self.credits_button, (120, 120))
        self.credits_button_rect = self.credits_button.get_rect()
        # set position for the buttons
        self.credits_button_rect.center = (WIDTH / 2 + self.how_to_button_rect.width + 125, height / 2 + 100)
        self.how_to_button_rect.center = (WIDTH / 2 + 80, height / 2 + 100)
        self.settings_button_rect.center = (WIDTH / 2 - 80, height / 2 + 100)
        self.start_button_rect.center = (WIDTH / 2 - self.how_to_button_rect.width - 125, height / 2 + 100)
        self.exit_button_rect.center = (WIDTH / 2, height / 2 + 270)


class SettingsScreen:
    def __init__(self):
        self.settings_overlay = pg.image.load('bin/assets/settings_menu/SETTINGS.png').convert_alpha()
        self.settings_overlay_rect = self.settings_overlay.get_rect()
        self.settings_overlay_rect.center = (WIDTH / 2, height / 2)
        self.music_option_on = pg.image.load('bin/assets/settings_menu/on.png').convert_alpha()
        self.music_option_on_rect = self.music_option_on.get_rect()
        self.music_option_on_rect.center = (372, 374)
        self.music_option_off = pg.image.load('bin/assets/settings_menu/off.png').convert_alpha()
        self.music_option_off_rect = self.music_option_off.get_rect()
        self.music_option_off_rect.center = (self.music_option_on_rect.centerx + self.music_option_on_rect.width + 2, 374)
        self.x = pg.image.load('bin/assets/settings_menu/x.png').convert_alpha()
        self.x_rect = self.x.get_rect()
        self.x_rect.topright = self.settings_overlay_rect.topright


class Comets:
    def __init__(self):
        self.comets = pg.image.load('bin/assets/main_menu/bg-09.png').convert_alpha()
        self.comets_glow = pg.image.load('bin/assets/main_menu/bg-08.png').convert_alpha()
        self.comets_rect = self.comets.get_rect()
        self.comets_glow_rect = self.comets_glow.get_rect()
        self.comets_rect.center = (WIDTH / 2 + 200, height / 2 - 90 + 270)
        self.comets_glow_rect.center = (WIDTH / 2 + 190, height / 2 - 115 + 270)


class HowToPlay:
    def __init__(self):
        # self.how_to_play_button = pg.image.load()
        pass
