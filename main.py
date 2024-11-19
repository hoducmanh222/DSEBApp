import json
import os
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from ui.ui import LoginScreen, HelloScreen, AccountScreen, DeadlinesScreen, Notes_Screen, GPA_Screen, RegisterScreen, Weather_Screen, EditProfileScreen, ClassScreen, SplashScreen
from kivy.core.window import Window

Window.size = (360, 800)

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None  # Store current username

    def build(self):
        self.theme_cls.primary_palette = "Cyan"
        self.title = "DSEB"
        self.icon = 'photo/dseb.png'
        self.screen_manager = ScreenManager()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        Builder.load_file('ui/kv/login.kv')
        Builder.load_file('ui/kv/hello.kv')
        Builder.load_file('ui/kv/account.kv')
        Builder.load_file('ui/kv/deadlines.kv')
        Builder.load_file('ui/kv/notes.kv')
        Builder.load_file('ui/kv/GPA.kv')
        Builder.load_file('ui/kv/register.kv')
        Builder.load_file('ui/kv/weather.kv')
        Builder.load_file('ui/kv/class.kv')
        Builder.load_file('ui/kv/splash.kv')
        
        self.screen_manager.add_widget(SplashScreen(name='splash'))
        self.screen_manager.add_widget(LoginScreen(name='login'))
        self.screen_manager.add_widget(HelloScreen(name='hello'))
        self.screen_manager.add_widget(AccountScreen(name='account'))
        self.screen_manager.add_widget(EditProfileScreen(name='edit_profile'))
        self.screen_manager.add_widget(DeadlinesScreen(name='deadlines'))
        self.screen_manager.add_widget(Notes_Screen(name='notes'))
        self.screen_manager.add_widget(GPA_Screen(name='GPA'))
        self.screen_manager.add_widget(RegisterScreen(name='register'))
        self.screen_manager.add_widget(Weather_Screen(name='weather'))
        self.screen_manager.add_widget(ClassScreen(name='class'))
        

        return self.screen_manager

    def switch_screen(self, screen_name):
        try:
            print(f"Switching to screen: {screen_name}")  # Debug
            self.screen_manager.current = screen_name
        except Exception as e:
            print(f"Error switching screens: {str(e)}")

if __name__ == '__main__':
    MainApp().run()