# login_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import json
import os
from hashlib import sha256
from kivy.properties import StringProperty


class LoginScreen(MDScreen):
    logo_path = StringProperty()
    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
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
    def login(self):
        try:
            username = self.ids.username_field.text.strip()
            password = self.ids.password_field.text.strip()
            
            if not username or not password:
                self.show_error_dialog("Username and password are required.")
                return
                
            data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.json')
            
            with open(data_file, 'r') as f:
                data = json.load(f)
                
            hashed_password = sha256(password.encode()).hexdigest()
            
            for user in data.get('users', []):
                if user['username'] == username and user['password'] == hashed_password:
                    # Clear all previous logged_in flags
                    for u in data['users']:
                        u.pop('logged_in', None)  # Remove logged_in flag if exists
                    
                    # Set new user as logged in
                    user['logged_in'] = True
                    
                    # Save changes
                    with open(data_file, 'w') as f:
                        json.dump(data, f, indent=4)
                    
                    print(f"Successfully logged in as: {username}")
                    self.ids.error_label.text = ""
                    account_screen = self.manager.get_screen('account')
                    account_screen.load_user_data()
                    self.manager.current = 'hello'
                    return

            print("Invalid credentials")  # Debug
            self.show_error_dialog("Invalid credentials")
            
        except Exception as e:
            print(f"Login error: {str(e)}")  # Debug
            self.ids.error_label.text = f"Login failed: {str(e)}"

        
