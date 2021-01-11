from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.app import App




class StartScreen(Screen):

    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)

        # TODO: add music only once ready to test in launcher
    #     self.music = SoundLoader.load('audio/disco_dancing.wav')
    #     self.music.loop = True
    #
    #     if self.music:
    #             self.music.play()
    #
    # def stop_music(self):
    #     if self.music:
    #         self.music.stop()


class PlayButton(Button):

    def __init__(self, **kwargs):
        super(PlayButton, self).__init__(**kwargs)
        self.background_normal = 'images/play_btn_normal.png'

        self.background_down = 'images/play_btn_down.png'
        self.size_hint = (None, None)
        self.size = (dp(100), dp(102))
        self.border = [0,0,0,0]



class HelpButton(Button):

    def __init__(self, **kwargs):
        super(HelpButton, self).__init__(**kwargs)

        self.background_normal = 'images/help_btn_normal.png'
        self.background_down = 'images/help_btn_down.png'
        self.size_hint = (None, None)
        self.size = (dp(70), dp(72))
        self.border = [0,0,0,0]


class GameTitle(Image):

    def __init__(self, **kwargs):
        super(GameTitle, self).__init__(**kwargs)
        self.source = 'images/game_title.png'
        self.size_hint = (None, None)
        self.allow_stretch = True
        self.size = (dp(273.3), dp(199))


class AnimatedWarning(Image):

    def __init__(self, **kwargs):
        super(AnimatedWarning, self).__init__(**kwargs)

        self.source = 'images/warning.png'
        self.size_hint = (None, None)
        self.size = (dp(276.6), dp(151.7))
        self.allow_stretch = True
        self.pos = (Window.width, Window.height/2)


    def animate_bounce(self):
        # += is a sequential step, while &= is in parallel
        animation = Animation(pos=((Window.width/2)-(self.width/2), self.y), t='in_out_circ', duration=0.5)
        animation += Animation(pos=((Window.width/2)-(self.width/2), self.y), t='in_out_circ', duration=0.8)

        animation += Animation(pos=(self.x - Window.width - self.width, self.y), t='in_out_circ', duration=0.5)
        animation.start(self)


    def on_pos(self, *args):
        self.pos = self.pos

















