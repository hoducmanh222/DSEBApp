from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
import json
from datetime import datetime
from kivy.uix.widget import Widget
import os

class DeadlinesScreen(Screen):
    def __init__(self, **kwargs):
        super(DeadlinesScreen, self).__init__(**kwargs)
        self.dialog = None
        self.data = self.load_deadlines()
        self.theme_cls = MDApp.get_running_app().theme_cls

    def on_enter(self):
        self.display_deadlines()

    def load_deadlines(self):
        try:
            deadline_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'deadlines.json')
            with open(deadline_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default structure if file doesn't exist or is invalid
            return {"deadlines": []}


    def save_deadlines(self):
        deadline_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'deadlines.json')
        with open(deadline_path, 'w') as f:
            json.dump(self.data, f)  # Use self.data instead of self.deadlines



    def show_add_deadline_dialog(self):
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="400dp"
        )

        self.deadline_title = MDTextField(
            hint_text="Enter deadline title",
            size_hint_y=None,
            height="40dp"
        )
        self.deadline_description = MDTextField(
            hint_text="Enter deadline description",
            size_hint_y=None,
            height="40dp"
        )
        self.deadline_date = MDTextField(
            hint_text="Select deadline date",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )
        self.deadline_time = MDTextField(
            hint_text="Select deadline time",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )

        date_button = MDRaisedButton(
            text="Pick Date",
            size_hint_y=None,
            height="40dp",
            width="100dp",
            on_release=self.show_date_picker
        )

        time_button = MDRaisedButton(
            text="Pick Time",
            size_hint_y=None,
            height="40dp",
            on_release=self.show_time_picker
        )

        layout.add_widget(self.deadline_title)
        layout.add_widget(self.deadline_description)
        layout.add_widget(self.deadline_date)
        layout.add_widget(date_button)
        layout.add_widget(self.deadline_time)
        layout.add_widget(time_button)

        self.dialog = MDDialog(
            title="Add Deadline",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="ADD",
                    on_release=self.add_deadline
                )
            ]
        )
        self.dialog.open()

    def add_deadline(self, *args):
        title = self.deadline_title.text
        description = self.deadline_description.text
        date = self.deadline_date.text
        time = self.deadline_time.text

        if title and date:
            self.data['deadlines'].append({
                'name': title,
                'content': description,
                'day': date,
                'time': time
            })
            self.save_deadlines()
            self.display_deadlines()
            self.dialog.dismiss()

    def show_edit_deadline_dialog(self, deadline):
        layout = MDBoxLayout(
            orientation="vertical",
            spacing="15dp",
            size_hint_y=None,
            height="400dp"
        )

        self.deadline_title = MDTextField(
            text=deadline['name'],
            hint_text="Enter deadline title",
            size_hint_y=None,
            height="40dp"
        )
        self.deadline_description = MDTextField(
            text=deadline['content'],
            hint_text="Enter deadline description",
            size_hint_y=None,
            height="40dp"
        )
        self.deadline_date = MDTextField(
            text=deadline['day'],
            hint_text="Select deadline date",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )
        self.deadline_time = MDTextField(
            text=deadline['time'],
            hint_text="Select deadline time",
            size_hint_y=None,
            height="40dp",
            readonly=True,
        )

        date_button = MDRaisedButton(
            text="Pick Date",
            size_hint_y=None,
            height="40dp",
            width="100dp",
            on_release=self.show_date_picker
        )

        time_button = MDRaisedButton(
            text="Pick Time",
            size_hint_y=None,
            height="40dp",
            on_release=self.show_time_picker
        )

        layout.add_widget(self.deadline_title)
        layout.add_widget(self.deadline_description)
        layout.add_widget(self.deadline_date)
        layout.add_widget(date_button)
        layout.add_widget(self.deadline_time)
        layout.add_widget(time_button)

        self.dialog = MDDialog(
            title="Edit Deadline",
            type="custom",
            content_cls=layout,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=lambda x: self.edit_deadline(deadline)
                )
            ]
        )
        self.dialog.open()

    def edit_deadline(self, old_deadline):
        title = self.deadline_title.text
        description = self.deadline_description.text
        date = self.deadline_date.text
        time = self.deadline_time.text

        if title and date:
            for deadline in self.data['deadlines']:
                if deadline == old_deadline:
                    deadline['name'] = title
                    deadline['content'] = description
                    deadline['day'] = date
                    deadline['time'] = time
                    break
            self.save_deadlines()
            self.display_deadlines()
            self.dialog.dismiss()

    def remove_deadline(self, deadline):
        self.data['deadlines'].remove(deadline)
        self.save_deadlines()
        self.display_deadlines()


    def display_deadlines(self):
        self.ids.deadline_box.clear_widgets()
        sorted_deadlines = sorted(
            self.data['deadlines'],
            key=lambda x: datetime.strptime(f"{x['day']}", '%d/%m/%Y')
        )

        if not sorted_deadlines:
            no_deadlines_label = MDLabel(
                text="No deadlines upcoming, just chilling babe",
                halign='center',
                valign='middle',
                theme_text_color='Secondary',
                size_hint_y=None,
                height=dp(65),
                text_size=(self.ids.deadline_scroll.width - dp(20), None),
                font_style='H6',
                bold=True
            )
            self.ids.deadline_box.add_widget(no_deadlines_label)
            return
        
        for deadline in sorted_deadlines:
            # Main card (always visible)
            main_card = MDCard(
                orientation='horizontal',
                padding=dp(10),
                size_hint_y=None,
                height=dp(60),
                md_bg_color=(0.98, 0.95, 0.75, 1)
            )
            
            # Store expanded state and create content card
            main_card.expanded = False
            main_card.content_card = None
            
            clock_icon = MDIconButton(
                icon='calendar-clock',
                size_hint=(None, None),
                size=(dp(24), dp(24))
            )

            date_label = MDLabel(
                text=deadline['day'],
                size_hint=(None, None),
                size=(dp(110), dp(40)),
                font_style='H6',
                font_size='7.5sp'
            )

            title_label = MDLabel(
                text=deadline['name'],
                size_hint=(None, None),
                size=(dp(90), dp(40)),
                font_style='H6',
                font_size='8sp',
                shorten=True,            # Enable text shortening
                shorten_from='right',    # Truncate from right side
                max_lines=1,            # Limit to one line
                text_size=(dp(90), None)  # Set text wrapping width
            )

            edit_button = MDIconButton(
                icon='pencil',
                size_hint=(None, None),
                size=(dp(24), dp(24)),
                on_release=lambda x, d=deadline: self.show_edit_deadline_dialog(d)
            )

            delete_button = MDIconButton(
                icon='delete',
                size_hint=(None, None),
                size=(dp(24), dp(24)),
                theme_text_color='Error',
                on_release=lambda x, d=deadline: self.remove_deadline(d)
            )

            main_card.add_widget(clock_icon)
            main_card.add_widget(date_label)
            main_card.add_widget(title_label)
            main_card.add_widget(edit_button)
            main_card.add_widget(delete_button)

            # Add click behavior
            main_card.bind(on_release=lambda x, d=deadline: self.toggle_deadline_details(x, d))
            
            self.ids.deadline_box.add_widget(main_card)

    def toggle_deadline_details(self, instance, deadline):
        content = MDBoxLayout(
            orientation='vertical',
            spacing=20,
            padding=[20, 20, 20, 20],
            size_hint_y=None,
            height=400
        )
        
        # Title section with icon
        title_box = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            adaptive_height=True,
            padding=[0, 10, 0, 10]
        )
        
        title_icon = MDIconButton(
            icon="format-title",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            font_size="24sp",
            pos_hint={'center_y': 0.5}
        )
        
        title = MDLabel(
            text=deadline['name'],
            theme_text_color="Primary",
            font_style="H5",
            adaptive_height=True,
            pos_hint={'center_y': 0.5}
        )
    
        title_box.add_widget(title_icon)
        title_box.add_widget(title)
        
        # Date section with icon
        date_box = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            adaptive_height=True,
            padding=[0, 10, 0, 10]
        )
        
        date_icon = MDIconButton(
            icon="calendar",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            font_size="24sp",
            pos_hint={'center_y': 0.5}
        )
        
        date = MDLabel(
            text=deadline['day'],
            theme_text_color="Secondary",
            adaptive_height=True,
            pos_hint={'center_y': 0.5}
        )
    
        date_box.add_widget(date_icon)
        date_box.add_widget(date)
        
        # Description section with icon
        desc_box = MDBoxLayout(
            orientation='horizontal',
            spacing=15,
            adaptive_height=True,
            padding=[0, 10, 0, 10]
        )
        
        desc_icon = MDIconButton(
            icon="text",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            font_size="24sp",
            pos_hint={'center_y': 0.5}
        )
        
        description = MDLabel(
            text=deadline['content'],
            theme_text_color="Secondary",
            adaptive_height=True,
            pos_hint={'center_y': 0.5}
        )
        desc_box.add_widget(desc_icon)
        desc_box.add_widget(description)
        
        separator1 = MDBoxLayout(
            size_hint_y=None,
            height="1dp",
            md_bg_color=(1, 1, 1, 1)  # White color
        )
        separator2 = MDBoxLayout(
            size_hint_y=None,
            height="1dp",
            md_bg_color=(1, 1, 1, 1)  # White color
        )
        
        # Add all sections to main content
        content.add_widget(title_box)
        content.add_widget(separator1)
        content.add_widget(date_box)
        content.add_widget(separator2)
        content.add_widget(desc_box)

        self.dialog = MDDialog(
            title="",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    theme_text_color="Custom",
                    on_release=self.close_dialog
                )
            ],
            size_hint=(.8, None)
        )
        self.dialog.open()
    def close_dialog(self, *args):
        self.dialog.dismiss()

    def show_date_picker(self, *args):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_selected)
        date_dialog.open()

    def on_date_selected(self, instance, value, date_range):
        self.deadline_date.text = value.strftime('%d/%m/%Y')

    def show_time_picker(self, *args):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.on_time_selected)
        time_dialog.open()

    def on_time_selected(self, instance, time):
        self.deadline_time.text = str(time)
