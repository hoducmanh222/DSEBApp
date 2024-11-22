# register_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import json
import os
from hashlib import sha256
from kivy.properties import StringProperty

class RegisterScreen(MDScreen):
    logo_path = StringProperty()

    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.logo_path = os.path.join(current_dir, '..', 'photo', 'neulogo.jpg')
        self.dialog = None

    def show_error_dialog(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Error",
                text=message,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=lambda x: self.dialog.dismiss()
                    )
                ]
            )
        else:
            self.dialog.text = message
        self.dialog.open()
    def register(self):
        try:
            username = self.ids.username_field.text.strip()
            password = self.ids.password_field.text.strip()
            
            if not username or not password:
                self.show_error_dialog("Username and password are required.")
                return
            
            if  len(password) < 6:
                self.show_error_dialog("Password must be at least 6 characters long.")
                return

            # Get absolute path to data directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)  # Go up one level
            data_dir = os.path.join(parent_dir, 'data')
            data_file = os.path.join(data_dir, 'data.json')

            # Create data directory if it doesn't exist
            os.makedirs(data_dir, exist_ok=True)

            # Load or create data
            try:
                with open(data_file, 'r') as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {'users': []}

            # Add new user
            hashed_password = sha256(password.encode()).hexdigest()
            if username not in [user['username'] for user in data['users']]:
                data['users'].append({'username': username, 'password': hashed_password})
            else:
                self.show_error_dialog("Username already exists.")
                return

            # Save data
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=4)

            print(f"Saved data to: {data_file}")  # Debug print
            self.manager.current = 'login'

            
        except Exception as e:
            print(f"Error saving data: {str(e)}")  # Debug print
            self.ids.error_label.text = f"Registration failed: {str(e)}"
