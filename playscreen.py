import random
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.screenmanager import Screen
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from startscreen import AnimatedWarning
from kivy.properties import NumericProperty
import random
from kivy.modules import screen
from kivy.metrics import dp
from kivy.animation import Animation



class PlayScreen(Screen):

    """

    Screen holding the Playsurface and TimerBar
    Parent: Manager (ScreenManager)

    """

    def __init__(self, **kwargs):
        super(PlayScreen, self).__init__(**kwargs)
        self.warning = None
        self.play_surface = PlaySurface()
        self.timer_bar = None
        self.timer_event = None # timer event ref. to be able to cancel()



    def animated_warning(self, dt):
        """
        Warning label to bounce across PlayScreen on_enter

        :param dt:
        :return:
        """
        self.add_widget(self.warning)
        self.warning.animate_bounce() # resides in StartScreen

    def start_timer(self, dt):
        self.timer_event = Clock.schedule_interval(self.timer_countdown, 1/60)

    def timer_countdown(self, dt):
        timer_value = self.timer_bar.update_value()

        if timer_value == 0: # to stop the function being called

            return False

    def reset_timer(self):

        if self.timer_bar.value == 6: # does not need to be reset if bar full
            return

        self.timer_event.cancel() # stops timer being called too quickly
        self.timer_bar.value = 6
        Clock.schedule_once(self.start_timer, 0.1)


    def remove_warning(self, dt):
        self.remove_widget(self.warning)


    def on_enter(self, *args):
        self.add_widget(self.play_surface)
        self.timer_bar = TimerBar()
        self.add_widget(self.timer_bar)
        self.warning = AnimatedWarning()

        Clock.schedule_once(self.animated_warning, 1)
        Clock.schedule_once(self.remove_warning, 3)
        Clock.schedule_once(self.start_timer, 0.3)

    def on_leave(self, *args):
        self.play_surface.clear_widgets()

        # Stop the timer
        if self.timer_bar.value > 0:
            self.timer_event.cancel()
        self.clear_widgets()

    def reset_game(self):
        self.children[1].clear_widgets()
        self.clear_widgets()
        self.on_enter(self)

class TimerBar(ProgressBar):

    """
    TimerBar, controls game time, calls winning sequence once at zero
    Parent: PlayScreen

    """

    def __init__(self, **kwargs):
        super(TimerBar, self).__init__(**kwargs)

        self.max = 3
        self.value = 3
        self.pos = (0, Window.height - self.height)


    def update_value(self):
        self.value = self.value - 0.01
        return self.value

    def set_value(self, value):
        self.value = value

    # perform the picking of a single avatar as the winner of round
    def on_value(self, value, instance):
        if self.value == 0:
            self.parent.children[1].pick_winner() # referencing the PlaySurface

class PlaySurface(FloatLayout):

    """
    Main touchable play surface
    Parent: PlayScreen
    """

    def __init__(self, **kwargs):
        super(PlaySurface, self).__init__(**kwargs)
        self.texture = Image(source='images/tiled_background.png').texture
        self.texture.wrap = 'repeat'
        self.texture.uvsize = (3, 3) # this needs to be calculated
        self.timer_event = None # dumb timer for a wait period
        Window.bind(on_keyboard=self.android_back_click)

        with self.canvas:
            Color(1, 1, 1)
            Rectangle(pos=(0, 0), size=(2000, 2000), texture=self.texture)



    def on_touch_down(self, touch):

        if self.parent.timer_bar.value > 0:
            touch.ud['spinner'] = Spinner(pos=(touch.x - 100, touch.y - 100))
            self.add_widget(touch.ud['spinner'])
            # print(len(self.children))
            # print(self.children)
            self.parent.reset_timer()
            
        else:
            return super(PlaySurface, self).on_touch_down(touch) # do nothing once the timer is 0

    def on_touch_move(self, touch):
        if self.parent.timer_bar.value > 0:
            touch.ud['spinner'].pos = [touch.x - dp(18.15), touch.y - dp(45.7)]
            
        else: 
            super(PlaySurface, self).on_touch_move(touch)
            

    def on_touch_up(self, touch):
        if self.parent.timer_bar.value > 0:
            self.remove_widget(touch.ud['spinner'])

            
        else: 
            return super(PlaySurface, self).on_touch_up(touch)

    # winner picking sequence triggered when timer hits 0
    def pick_winner(self):

        # pick a random 'spinner' in the list of current spinners
        players_list_length = len(self.children)

        if players_list_length == 0:
            if self.timer_event:
                self.timer_event.cancel()

            App.get_running_app().root.current = 'start_screen'

            App.get_running_app().root.show_ad()

            return

        elif players_list_length == 1:
            self.clear_widgets()
            modal = AnimatedBoxLayoutAlone()
            self.add_widget(modal)
            modal.animate_bounce()
            return


        random_player = random.randint(0,players_list_length-1)


        winner = self.children[random_player]
        self.clear_widgets()
        self.add_widget(winner)

        self.timer_event = Clock.schedule_once(self.open_win_screen, 1.5) # delay while animation takes place

    def open_win_screen(self, dt): # called from clock after t time
        win_screen = AnimatedBoxLayoutChug()
        self.add_widget(win_screen)
        win_screen.animate_bounce()
        return False

    def android_back_click(self, window, key, *args):
        if key == 27:
            if self.timer_event:
                self.timer_event.cancel()




class Spinner(Image):
    angle = NumericProperty(0)



    def __init__(self, **kwargs):
        super(Spinner, self).__init__(**kwargs)
        Clock.schedule_interval(self.spin, 0)



        self.source = 'images/glass.png'
        self.size_hint = (None, None)
        self.allow_stretch = True
        self.size = (dp(36.3), dp(91.4))

    # help this function return false to stop clock running
    def spin(self, *args):
        self.angle += 3


    def on_pos(self, instance, value):
        #print(self.name)
        pass

    def pick_random_avatar(self):
        pick = random.randint(0,1)
        return pick

class PlayOptions(ModalView):
    pass

class AnimatedBoxLayoutAlone(BoxLayout):

    def __init__(self, **kwargs):
        super(AnimatedBoxLayoutAlone, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(276.8), dp(263.3))
        self.spacing = dp(20)
        self.pos = (Window.width, (Window.height / 2) - self.height/2)

    def animate_bounce(self):
        animation = Animation(pos=((Window.width / 2) - (self.width / 2), self.y), t='in_out_circ', duration=0.5)
        animation += Animation(pos=((Window.width / 2) - (self.width / 2), self.y), t='in_out_circ', duration=0.8)


        animation.start(self)


    def on_pos(self, *args):
        self.pos = self.pos

class AllAlone(Image):

    def __init__(self, **kwargs):
        super(AllAlone, self).__init__(**kwargs)
        self.source = 'images/alone.png'
        self.size_hint = (None, None)
        self.allow_stretch = True
        self.size = (dp(276.8), dp(138.8))

class AnimatedBoxLayoutChug(BoxLayout):

    def __init__(self, **kwargs):
        super(AnimatedBoxLayoutChug, self).__init__(**kwargs)

        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.size = (dp(203.5), dp(231.1))
        self.spacing = dp(20)
        self.pos = (Window.width, (Window.height / 2) - self.height/2)

    def animate_bounce(self):
        animation = Animation(pos=((Window.width / 2) - (self.width / 2), self.y), t='in_out_circ', duration=0.5)
        animation += Animation(pos=((Window.width / 2) - (self.width / 2), self.y), t='in_out_circ', duration=0.8)


        animation.start(self)


    def on_pos(self, *args):
        self.pos = self.pos

class Chug(Image):

    def __init__(self, **kwargs):
        super(Chug, self).__init__(**kwargs)
        self.source = 'images/chug.png'
        self.size_hint = (None, None)
        self.allow_stretch = True
        self.size = (dp(203.5), dp(147.8))

