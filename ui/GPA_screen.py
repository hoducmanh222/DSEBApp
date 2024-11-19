from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp


class GPA_Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.courses = {
            "CNXHKH": 2,
            "Macroeconomics": 3,
            "PLDC": 3,
            "Marketing": 3,
            "Discrete Math": 3,
            "Optimization": 3,
            "Statistics": 3,
            "Python": 3
        }
        self.grades_data = {}
        self.setup_menu()

    def setup_menu(self):
        menu_items = [
            {
                "text": f"{course}",
                "viewclass": "OneLineListItem",
                "on_release": lambda x=course: self.select_course(x),
            } for course in self.courses.keys()
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.course_dropdown,
            items=menu_items,
            width_mult=4,
        )

    def select_course(self, course_name):
        self.ids.course_dropdown.text = f"{course_name}"
        self.menu.dismiss()
        if course_name in self.grades_data:
            data = self.grades_data[course_name]
            self.ids.participation_score.text = str(data['participation'])
            self.ids.midterm_score.text = str(data['midterm'])
            self.ids.final_score.text = str(data['final'])
        else:
            self.ids.participation_score.text = ""
            self.ids.midterm_score.text = ""
            self.ids.final_score.text = ""

    def round_score(self, score):
        second_decimal = int((score * 100) % 10)
        base_score = int(score * 10) / 10
        return base_score + 0.1 if second_decimal >= 5 else base_score

    def calculate_grade(self, score):
        if score >= 9.0:
            return "A+", 4.0
        elif score >= 8.5:
            return "A", 4.0
        elif score >= 8.0:
            return "B+", 3.5
        elif score >= 7.0:
            return "B", 3.0
        elif score >= 6.5:
            return "C+", 2.5
        elif score >= 5.5:
            return "C", 2.0
        elif score >= 5.0:
            return "D+", 1.5
        elif score >= 4.0:
            return "D", 1.0
        else:
            return "F", 0.0

    def update_grades(self):
        course_text = self.ids.course_dropdown.text
        if not course_text or course_text == "Select Course":
            self.ids.grade_result.text = "Please select a course"
            return

        course = course_text.split(" (")[0]

        try:
            participation = float(self.ids.participation_score.text or 0)
            midterm = float(self.ids.midterm_score.text or 0)
            final = float(self.ids.final_score.text or 0)

            if not (0 <= participation <= 10 and 0 <= midterm <= 10 and 0 <= final <= 10):
                self.ids.grade_result.text = "Scores must be between 0 and 10"
                return

            raw_score = (participation * 0.1) + (midterm * 0.4) + (final * 0.5)
            rounded_score = self.round_score(raw_score)
            letter_grade, gpa_4 = self.calculate_grade(rounded_score)

            self.grades_data[course] = {
                'participation': participation,
                'midterm': midterm,
                'final': final,
                'score_10': rounded_score,
                'letter': letter_grade,
                'gpa_4': gpa_4,
                'credits': self.courses[course]
            }

            self.update_grades_table()

        except ValueError:
            self.ids.grade_result.text = "Please enter valid scores"

    def update_grades_table(self):
        table_text = "{:<20} {:^10} {:^10} {:^10}\n".format("Course", "Credits", "Score (10)", "Grade")
        table_text += "-" * 55 + "\n"

        total_credits = 0
        weighted_sum_10 = 0
        weighted_sum_4 = 0

        for course, data in self.grades_data.items():
            credits = data['credits']
            total_credits += credits
            weighted_sum_10 += data['score_10'] * credits
            weighted_sum_4 += data['gpa_4'] * credits

            table_text += "{:<20} {:^10} {:^10.2f} {:^10}\n".format(
                course, credits, data['score_10'], data['letter']
            )

        if total_credits > 0:
            avg_10 = weighted_sum_10 / total_credits
            avg_4 = weighted_sum_4 / total_credits

            table_text += "-" * 55 + "\n"
            table_text += f"GPA (10-scale): {avg_10:.2f}\n"
            table_text += f"GPA (4-scale): {avg_4:.2f}"

        self.ids.grade_result.text = table_text