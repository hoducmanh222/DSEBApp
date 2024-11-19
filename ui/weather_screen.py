from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
import requests
from datetime import datetime
from kivy.metrics import dp
from kivy.clock import Clock
from functools import partial

class Weather_Screen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None
        self.last_search = ""
        self.search_delay = 0.5
        self.scheduled_search = None
        self.cities = ["London", "Paris", "New York", "Tokyo", "Beijing", "Sydney", 
                    "Dubai", "Singapore", "Hong Kong", "Seoul", "Moscow", "Berlin",
                    "Rome", "Madrid", "Amsterdam", "Vienna", "Bangkok", "Mumbai",
                    "Toronto", "Chicago", "San Francisco", "Los Angeles", "Miami",
                    "Rio de Janeiro", "Cairo", "Istanbul", "Stockholm", "Oslo",
                    "Copenhagen", "Helsinki", "Prague", "Budapest", "Warsaw",
                    "Athens", "Lisbon", "Dublin", "Edinburgh", "Brussels",
                    "Zurich", "Geneva", "Milan", "Barcelona", "Valencia",
                    "Porto", "Munich", "Frankfurt", "Hamburg", "Vancouver",
                    "Montreal", "Quebec", "Mexico City", "Buenos Aires",
                    "Santiago", "Lima", "Bogota", "Sao Paulo", "Hanoi",
                    "Ho Chi Minh City", "Jakarta", "Manila", "Kuala Lumpur"]

    api_key = "fb5d71ff9a5e07ceca86d42c2d23e1be"

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.get_weather("Ha Noi"), 0.5)
        self.get_current_date()

    def on_text_change(self, text):
        if not text:
            if self.menu:
                self.menu.dismiss()
            return

        # Cancel previous scheduled search
        if self.scheduled_search:
            self.scheduled_search.cancel()

        # Schedule new search with delay
        self.scheduled_search = Clock.schedule_once(
            partial(self.show_suggestions, text), 
            self.search_delay
        )

    def show_suggestions(self, text, *args):
        text = text.lower()
        suggestions = [
            city for city in self.cities 
            if text in city.lower() 
            or any(text in word.lower() for word in city.split())
        ][:10]  # Limit to 10 suggestions for performance

        if suggestions:
            menu_items = [
                {
                    "text": city,
                    "viewclass": "OneLineListItem",
                    "height": dp(56),
                    "on_release": lambda x=city: self.select_city(x),
                } for city in suggestions
            ]

            if self.menu:
                self.menu.dismiss()

            self.menu = MDDropdownMenu(
                caller=self.ids.city_name,
                items=menu_items,
                position="bottom",
                width_mult=4,
                max_height=dp(250),
            )
            self.menu.open()

    def select_city(self, city):
        self.ids.city_name.text = city
        if self.menu:
            self.menu.dismiss()
        Clock.schedule_once(lambda dt: self.get_weather(city), 0.1)

    def get_weather(self, location):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200 and data["cod"] != "404":
                self.update_weather_ui(data)
            else:
                self.show_error_message("City not found")

        except requests.RequestException:
            self.show_error_message("Connection error")
        except Exception as e:
            self.show_error_message(f"Error: {str(e)}")

    def search_weather(self):
        city_name = self.ids.city_name.text.strip()
        if city_name:
            self.get_weather(city_name)


    def update_weather_ui(self, data):
        temperature = round(data["main"]["temp"])
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["description"]
        weather_id = data["weather"][0]["id"]
        wind_speed = round(data["wind"]["speed"] * 18 / 5)
        location = f"{data['name']}, {data['sys']['country']}"

        self.ids.temperature.text = f"[b]{temperature}°C[/b]"
        self.ids.weather.text = weather.capitalize()
        self.ids.humidity.text = f"{humidity}%"
        self.ids.wind_speed.text = f"{wind_speed} km/h"
        self.ids.location.text = location
        self.ids.weather_icon.icon = self.get_weather_icon(weather_id, weather)

    def get_weather_icon(self, weather_id, weather_desc):
        if weather_id == 800:
            return "weather-sunny"
        elif 200 <= weather_id <= 232:
            return "weather-lightning"
        elif 300 <= weather_id <= 321 or 500 <= weather_id <= 531:
            return "weather-rainy"
        elif 600 <= weather_id <= 622:
            return "weather-snowy"
        elif 701 <= weather_id <= 781:
            return "weather-fog"
        elif 801 <= weather_id <= 804:
            return "weather-cloudy"
        elif "cloud" in weather_desc:
            return "weather-cloudy"
        return "weather-sunny"

    def get_current_date(self):
        self.ids.date_label.text = datetime.now().strftime("%Y/%m/%d")

    def show_error_message(self, message):
        print(f"Weather Error: {message}")
