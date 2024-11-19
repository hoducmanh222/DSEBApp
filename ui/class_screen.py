from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import (
    MDList,
    TwoLineListItem,
    ThreeLineListItem,
)
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabs, MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.toolbar import MDTopAppBar

class Tab(MDBoxLayout, MDTabsBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.tabs = MDTabs(
            tab_indicator_anim=True,
            tab_indicator_height="3dp"
        )



class ClassScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create main layout
        self.main_box = MDBoxLayout(orientation="vertical")
        
        # Add top bar
        self.top_bar = MDTopAppBar(
            title="Class",
            elevation=1,
            padding = ["0dp", 0, "100dp", 0],
            left_action_items=[["arrow-left", lambda x: MDApp.get_running_app().switch_screen('hello')]]
        )
        self.main_box.add_widget(self.top_bar)

        separator = MDBoxLayout(
            size_hint_y=None,
            height="1dp",
            md_bg_color=(1, 1, 1, 1)  # White color
        )
        self.main_box.add_widget(separator)
        
        # Create tabs
        self.tabs = MDTabs()
        
        # Tab 1: Class Members
        tab1 = Tab()
        tab1.title = "Class Members"
        tab1.icon = "account-group"
        scroll_view_members = MDScrollView()
        member_list = MDList()

        class_members = [
            {"name": "Bui Chau Anh", "ID": "11230508"},
            {"name": "Nguyen Thi Mai Anh", "ID": "11230512"},
            {"name": "Tran Tuan Anh", "ID": "11230515"},
            {"name": "Vu Ngoc Hong Anh", "ID": "11230517"},
            {"name": "Le Ngoc Bich", "ID": "11230520"},
            {"name": "Thanh Uyen Dung", "ID": "11230522"},
            {"name": "Do Tuan Dat", "ID": "11230527"},
            {"name": "Vu Tuan Dat", "ID": "11230529"},
            {"name": "Nguyen Phuong Dong", "ID": "11230530", "role": "Secretary"},
            {"name": "Tran Minh Duc", "ID": "11230531"},
            {"name": "Tran Thu Hang", "ID": "11230533"},
            {"name": "Nguyen Duong Hieu", "ID": "11230535"},
            {"name": "Nguyen Hoang", "ID": "11230538"},
            {"name": "Nguyen Viet Hoang", "ID": "11230539"},
            {"name": "Dang Nhat Huy", "ID": "11230544"},
            {"name": "Dinh Nam Khanh", "ID": "11230548"},
            {"name": "Nguyen Vinh Khanh", "ID": "11230549"},
            {"name": "Do Huu Kien", "ID": "11230552"},
            {"name": "Han Chi Kien", "ID": "11230553"},
            {"name": "Do Anh Ly", "ID": "11230563"},
            {"name": "Nguyen Ngoc Suong Mai", "ID": "11230564"},
            {"name": "Ho Duc Manh", "ID": "11230565"},
            {"name": "Khong Gia Minh", "ID": "11230567"},
            {"name": "Le Nguyen Tue Minh", "ID": "11230568"},
            {"name": "Pham Hong Minh", "ID": "11230570"},
            {"name": "Nghiem Tra My", "ID": "11230572"},
            {"name": "Nguyen Phu Nam", "ID": "11230574", "role": "Monitor"},
            {"name": "Hoang Thi Thanh Nhan", "ID": "11230578"},
            {"name": "Nguyen Tuan Phong", "ID": "11230580"},
            {"name": "Tran Dinh Tuan Phong", "ID": "11230581"},
            {"name": "Chu Bich Phuong", "ID": "11230584", "role": "Vice Monitor"},
            {"name": "Nguyen Dai Quan", "ID": "11230586"},
            {"name": "Nguyen Thanh Thao", "ID": "11230588"},
            {"name": "Le Thi Anh Thu", "ID": "11230591"},
            {"name": "Pham Van Thu", "ID": "11230592"},
            {"name": "Nguyen Thi Thu Trang", "ID": "11230595"},
            {"name": "Trieu Hai Dang Trinh", "ID": "11230597"},
            {"name": "Truong Hoang Tung", "ID": "11230601"},
            {"name": "Nguyen Tong Nguyen Vu", "ID": "11230604"},
        ]

        for member in class_members:
            role = member.get("role", None)
            is_bold = role in ["Monitor", "Vice Monitor", "Secretary"]
            
            name_id_text = f"[b]{member['name']} - {member['ID']}[/b]" if is_bold else f"{member['name']} - {member['ID']}"
            role_text = f"[b]{role}[/b]" if is_bold and role else "Member"
            
            member_item = ThreeLineListItem(
                text=name_id_text,
                secondary_text=role_text,
                font_style="Body1",
            )
            member_list.add_widget(member_item)

        scroll_view_members.add_widget(member_list)
        tab1.add_widget(scroll_view_members)
        self.tabs.add_widget(tab1)

        # Tab 2: Teachers
        tab2 = Tab()
        tab2.title = "Teachers"
        tab2.icon = "school"
        scroll_view_teachers = MDScrollView()
        teacher_list = MDList()

        teachers = [
            {"name": "Nguyen Van Hau", "subject": "CNXHKH"},
            {"name": "Nguyen Viet Hung", "subject": "Macroeconomics"},
            {"name": "Nguyen Tuan Long", "subject": "Programming"},
            {"name": "Nguyen Quynh Trang", "subject": "Marketing"},
            {"name": "Tran Thi Hong Nhung", "subject": "Fundamental of Laws"},
            {"name": "Nguyen Tuan Long", "subject": "Discrete mathematics"},
            {"name": "Vuong Van Yen", "subject": "Optimization"},
            {"name": "VU Thi Bich Ngoc", "subject": "Mathematical statistics"},
        ]

        for teacher in teachers:
            teacher_item = TwoLineListItem(
                text=f"{teacher['name']}",
                secondary_text=f"Subject: {teacher['subject']}",
            )
            teacher_list.add_widget(teacher_item)

        scroll_view_teachers.add_widget(teacher_list)
        tab2.add_widget(scroll_view_teachers)
        self.tabs.add_widget(tab2)
        
        # Add tabs to main layout
        self.main_box.add_widget(self.tabs)
        
        # Add main layout to screen
        self.add_widget(self.main_box)
