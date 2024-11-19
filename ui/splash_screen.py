from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty
from kivy.clock import Clock
import os

class SplashScreen(MDScreen):
    image_path = StringProperty('')
    loading_text = StringProperty('Loading...')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(current_dir, '..', 'photo', 'dseb.png')
        self.dots = ['...', '..', '.', '..']
        self.current_dot = 0
        Clock.schedule_interval(self.animate_loading, 0.8)
        Clock.schedule_once(self.switch_to_login, 5)
        
    def animate_loading(self, dt):
        self.loading_text = f'Loading{self.dots[self.current_dot]}'
        self.current_dot = (self.current_dot + 1) % len(self.dots)
        
    def switch_to_login(self, dt):
        self.manager.current = 'login'
