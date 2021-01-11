from kivy.app import App
from kivy.metrics import Metrics
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import Metrics
from startscreen import StartScreen, AnimatedWarning
from playscreen import PlayScreen, PlaySurface, Spinner
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.image import Image
import math
from kivy.properties import ObjectProperty

#from jnius import autoclass

from kivy.utils import platform

#if platform=="android":
    #PythonActivity = autoclass("org.kivy.android.PythonActivity")
    #AdBuddiz = autoclass("com.purplebrain.adbuddiz.sdk.AdBuddiz")



class Manager(ScreenManager):

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)


    def play_screen(self):
        self.current = "play_screen"

    def show_ad(self):
        #AdBuddiz.showAd(PythonActivity.mActivity)
        pass





class PubApp(App):


    def __init__(self, **kwargs):
        super(PubApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.android_back_click)
        self.background_setup()
        self.main_screen_background = None




    # handle the back click of android, always returning to the start screen
    def android_back_click(self, window, key, *args):
        if key == 27:
            self.root.current = "start_screen"
            return True

    def background_setup(self):  # calculate how many backgrounds to spread across screen

        self.texture = Image(source='images/background.png').texture
        self.texture.wrap = 'repeat'
        self.uv_width = math.floor(Window.width / 720)

        if self.uv_width == 0:
            self.texture.uvsize = (1, -1)

        else:
            self.texture.uvsize = (self.uv_width, -1)

    def build(self):

        #AdBuddiz.setPublisherKey("bb96f587-0913-4a67-87de-dc0180cab5fa")  # replace the key with your app Key
        #AdBuddiz.setTestModeActive()  # test mode will be active
        #AdBuddiz.cacheAds(PythonActivity.mActivity)  # now we are caching the ads



        manager = Manager()

        def on_pause(self):
            return

        def on_resume(self):
            return


        return manager








    
if __name__ == '__main__':

    app = PubApp()
    app.run()
    
    