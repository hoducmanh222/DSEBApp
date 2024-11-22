import os
import json
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    note_id = StringProperty()
    completed = BooleanProperty(False)
    content = StringProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._update_text_style()
    
    def _update_text_style(self):
        if self.completed:
            self.text = f"[color=808080][i][s]{self.text.replace('[color=808080]', '').replace('[i]', '').replace('[s]', '').replace('[/s]', '').replace('[/i]', '').replace('[/color]', '')}[/s][/i][/color]"
        else:
            self.text = self.text.replace("[color=808080]", "").replace("[i]", "").replace("[s]", "").replace("[/s]", "").replace("[/i]", "").replace("[/color]", "")

    def on_checkbox_active(self, checkbox_instance):
        self.completed = checkbox_instance.active
        self._update_text_style()
        
        screen = self.parent.parent.parent.parent
        for note in screen.notes:
            if note['id'] == self.note_id:
                note['completed'] = checkbox_instance.active
                break
        screen.on_checkbox_active(self.note_id, checkbox_instance.active)

    def edit_note(self):
        screen = self.parent.parent.parent.parent
        screen.edit_note_dialog(self.note_id)

    def delete_note(self):
        screen = self.parent.parent.parent.parent
        screen.delete_note(self.note_id)

    def view_note_content(self):
        screen = self.parent.parent.parent.parent
        screen.view_note_dialog(self.note_id)

class Notes_Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notes = []  # Explicitly initialize as a list
        self.dialog = None
        self.title_field = None
        self.content_field = None
        self.load_notes()  # Load notes when screen initializes

    def load_notes(self):
        try:
            notes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'notes.json')
            if os.path.exists(notes_path):
                with open(notes_path, 'r') as f:
                    loaded_data = json.load(f)
                    # Ensure loaded_data is a list
                    self.notes = loaded_data if isinstance(loaded_data, list) else []
                self.update_notes_list()
        except Exception as e:
            print(f"Error loading notes: {e}")
            self.notes = []  # Fallback to empty list
    def save_notes(self):
        try:
            notes_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'notes.json')
            with open(notes_path, 'w') as f:
                json.dump(self.notes, f, indent=4)
        except Exception as e:
            print(f"Error saving notes: {e}")

    def open_add_note_dialog(self):
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(200)
        )

        self.title_field = MDTextField(
            hint_text="Title",
            helper_text="Enter note title",
            helper_text_mode="on_error"
        )
        self.content_field = MDTextField(
            hint_text="Content",
            multiline=True,
            helper_text="Enter note content",
            helper_text_mode="on_error"
        )

        content.add_widget(self.title_field)
        content.add_widget(self.content_field)

        self.dialog = MDDialog(
            title="Add New Note",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dismiss_dialog
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=self.save_note
                ),
            ],
        )
        self.dialog.open()

    def save_note(self, *args):
        title = self.title_field.text.strip()
        content = self.content_field.text.strip()

        if not title or not content:
            return

        note = {
            'id': str(len(self.notes)),
            'title': title,
            'content': content,
            'completed': False
        }
        self.notes.append(note)
        self.update_notes_list()
        self.save_notes()  
        self.dismiss_dialog()

    def update_notes_list(self):
        notes_list = self.ids.note_list
        notes_list.clear_widgets()

        for note in self.notes:
            item = ListItemWithCheckbox(
                text=note['title'],
                note_id=note['id'],
                completed=note['completed'],
                content=note['content']
            )
            notes_list.add_widget(item)

    def edit_note_dialog(self, note_id):
        note = next((n for n in self.notes if n['id'] == note_id), None)
        if not note:
            return

        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(20),
            size_hint_y=None,
            height=dp(200)
        )

        self.title_field = MDTextField(
            text=note['title'],
            hint_text="Title"
        )
        self.content_field = MDTextField(
            text=note['content'],
            hint_text="Content",
            multiline=True
        )

        content.add_widget(self.title_field)
        content.add_widget(self.content_field)

        self.dialog = MDDialog(
            title="Edit Note",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dismiss_dialog
                ),
                MDFlatButton(
                    text="SAVE",
                    on_release=lambda x: self.update_note(note_id)
                ),
            ],
        )
        self.dialog.open()

    def update_note(self, note_id):
        title = self.title_field.text.strip()
        content = self.content_field.text.strip()

        if not title or not content:
            return

        note = next((n for n in self.notes if n['id'] == note_id), None)
        if note:
            note['title'] = title
            note['content'] = content
            self.update_notes_list()
            self.save_notes()  
            self.dismiss_dialog()

    def delete_note(self, note_id):
        self.notes = [n for n in self.notes if n['id'] != note_id]
        self.update_notes_list()
        self.save_notes() 

    def view_note_dialog(self, note_id):
        note = next((n for n in self.notes if n['id'] == note_id), None)
        if not note:
            return

        self.dialog = MDDialog(
            title=note['title'],
            text=note['content'],
            buttons=[
                MDFlatButton(
                    text="CLOSE",
                    on_release=self.dismiss_dialog
                ),
            ],
        )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None

    def on_checkbox_active(self, note_id, is_completed):
        note = next((n for n in self.notes if n['id'] == note_id), None)
        if note:
            note['completed'] = is_completed
            self.update_notes_list()
            self.save_notes()  # Save notes after marking complete/incomplete
