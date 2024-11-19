from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.properties import StringProperty
import re
import os
import json
import shutil
from datetime import datetime

class AccountScreen(Screen):
    profile_image_path = StringProperty()
    
    def __init__(self, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)
        self.dialog = None
        self.menu = None
        self.set_profile_image_path()

    def on_kv_post(self, base_widget):
        self.load_user_data()
        
    def set_profile_image_path(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.profile_image_path = os.path.join(current_dir, '..', 'photo', 'photo5.png')

    def load_user_data(self):
        try:
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.json')
            with open(data_path, 'r') as f:
                data = json.load(f)
                username = next(user['username'] for user in data['users'] if user.get('logged_in'))

            profile_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'profiles.json')
            try:
                with open(profile_path, 'r') as f:
                    profiles = json.load(f)
                    user_profile = profiles.get(username, {})
            except FileNotFoundError:
                profiles = {}
                user_profile = {}

            # Set default profile picture first
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.profile_image_path = os.path.join(current_dir, '..', 'photo', 'photo5.png')
            
            # Then override with user's photo if they have one
            if user_profile.get('photo'):
                self.profile_image_path = user_profile['photo']

            self.ids.name_label.text = f"Name: {user_profile.get('name', username)}"
            self.ids.dob_label.text = f"Date of Birth: {user_profile.get('dob', 'Not Set')}"
            self.ids.country_label.text = f"Country: {user_profile.get('country', 'Not Set')}"
            self.ids.email_label.text = f"Email: {user_profile.get('email', 'Not Set')}"

        except Exception as e:
            print(f"Error loading user data: {e}")


    def edit_profile(self):
        self.manager.current = 'edit_profile'

    def change_avatar(self):
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(400),
            md_bg_color=(0.6, 0.9, 0.6, 1)  # Pastel green background
        )
        
        file_chooser = FileChooserListView(
            filters=['*.png', '*.jpg', '*.jpeg'],
            path=os.path.expanduser('~')
        )
        content.add_widget(file_chooser)
        
        self.dialog = MDDialog(
            title="Choose Profile Picture",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="SELECT",
                    on_release=lambda x: self.process_avatar_selection(file_chooser)
                )
            ]
        )
        self.dialog.open()

    def process_avatar_selection(self, file_chooser):
        if file_chooser.selection:
            selected_file = file_chooser.selection[0]
            photo_dir = os.path.join(os.path.dirname(__file__), '..', 'photo')
            if not os.path.exists(photo_dir):
                os.makedirs(photo_dir)
            
            # Get current user
            data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.json')
            with open(data_path, 'r') as f:
                data = json.load(f)
                username = next(user['username'] for user in data['users'] if user.get('logged_in'))
            
            # Save photo with username in filename
            new_path = os.path.join(photo_dir, f'profile_{username}.png')
            shutil.copy2(selected_file, new_path)
            self.profile_image_path = new_path

            # Save photo path in profiles.json
            profile_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'profiles.json')
            try:
                with open(profile_path, 'r') as f:
                    profiles = json.load(f)
            except:
                profiles = {}
            
            if username not in profiles:
                profiles[username] = {}
            profiles[username]['photo'] = new_path

            with open(profile_path, 'w') as f:
                json.dump(profiles, f)

            self.dialog.dismiss()


class EditProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.menu = None

    def on_enter(self):
        try:
            with open('profiles.json', 'r') as f:
                profiles = json.load(f)
                current_user = MDApp.get_running_app().current_user
                if current_user in profiles:
                    profile = profiles[current_user]
                    self.ids.name_label.text = f"Name: {profile.get('name', '')}"
                    self.ids.dob_label.text = f"Date of Birth: {profile.get('dob', '')}"
                    self.ids.country_label.text = f"Country: {profile.get('country', '')}"
                    self.ids.email_label.text = f"Email: {profile.get('email', '')}"
                    self.profile_image_path = profile.get('profile_image', 'assets/default_avatar.png')
        except (FileNotFoundError, json.JSONDecodeError):
            profiles = {}
            with open('profiles.json', 'w') as f:
                json.dump(profiles, f)

    def save_changes(self, *args):
        # Get current logged in username
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.json')
        try:
            with open(data_path, 'r') as f:
                data = json.load(f)
                username = next(user['username'] for user in data['users'] if user.get('logged_in'))

            # Load or create profiles.json
            profile_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'profiles.json')
            try:
                with open(profile_path, 'r') as f:
                    profiles = json.load(f)
            except:
                profiles = {}

            # Save updated profile data
            profiles[username] = {
                'name': self.ids.name_field.text,
                'dob': self.ids.dob_field.text,
                'country': self.ids.country_field.text,
                'email': self.ids.email_field.text
            }

            # Write to profiles.json
            with open(profile_path, 'w') as f:
                json.dump(profiles, f)

            # Update account screen and switch back
            account_screen = self.manager.get_screen('account')
            account_screen.load_user_data()
            self.manager.current = 'account'

        except Exception as e:
            print(f"Error saving changes: {e}")

    def show_country_menu(self, instance):
        countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", 
                    "Australia", "Austria", "Bangladesh", "Belgium", "Brazil", "Canada", 
                    "China", "Denmark", "Egypt", "Finland", "France", "Germany", "Greece", 
                    "India", "Indonesia", "Italy", "Japan", "Kenya", "Malaysia", "Mexico", 
                    "Netherlands", "New Zealand", "Nigeria", "Norway", "Pakistan", "Philippines", 
                    "Poland", "Portugal", "Russia", "Saudi Arabia", "Singapore", "South Africa", 
                    "South Korea", "Spain", "Sweden", "Switzerland", "Thailand", "Turkey", 
                    "United Arab Emirates", "United Kingdom", "United States", "Vietnam"]
        
        menu_items = [{"viewclass": "OneLineListItem", 
                      "text": country,
                      "on_release": lambda x=country: self.set_country(instance, x)
                     } for country in countries]
        
        self.menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4,
            max_height=dp(300)
        )
        self.menu.open()

    def set_country(self, instance, country):
        instance.text = country
        self.menu.dismiss()

    def toggle_password_visibility(self):
        self.ids.password_field.password = not self.ids.password_field.password
        self.ids.password_eye_icon.icon = 'eye' if self.ids.password_field.password else 'eye-off'
