import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout


BASE_API_URL = 'https://your-backend-api.com/api'


class LoginScreen(Screen):
    pass


# class HomeScreen(Screen):
#     Builder.load_file('main.kv')


class SeatBookingScreen(Screen):
    def book_seat(self):
        # Replace with the current user's ID
        user_id = 1
        data = {'user_id': user_id, 'seat_id': 5}  # seat_id is the selected seat
        response = requests.post(f"{BASE_API_URL}/book-seat", data=data)
        if response.status_code == 200:
            print("Seat booked for 1 hour!")
            self.manager.current = "token"
        else:
            print("Failed to book the seat.")


class BookListScreen(Screen):
    def on_enter(self):
        # Fetch books from the backend when the user navigates to this screen
        response = requests.get(f"{BASE_API_URL}/books")
        if response.status_code == 200:
            books = response.json()
            print("Available books:", books)
        else:
            print("Failed to fetch books")


class TokenScreen(Screen):
    def on_enter(self):
        # Fetch the active token for the user
        user_id = 1  # Replace with the current user's ID
        response = requests.get(f"{BASE_API_URL}/token?user_id={user_id}")
        if response.status_code == 200:
            token = response.json()
            self.ids.token_label.text = f"Token ID: {token['id']}\nExpires at: {token['expires_at']}"
        else:
            self.ids.token_label.text = "No active token"


class CafeLibraryApp(App):
    def build(self):
        sm = ScreenManager()
        # sm.add_widget(HomeScreen(name="HomeScreen"))
        return Builder.load_file('main.kv')
        # sm.add_widget(LoginScreen(name="login"))
        # sm.add_widget(SeatBookingScreen(name="seat_booking"))
        # sm.add_widget(BookListScreen(name="book_list"))
        # sm.add_widget(TokenScreen(name="token"))
        # return sm

    def login_user(self, email, password):
        response = requests.post(f"{BASE_API_URL}/login", data={'email': email, 'password': password})
        if response.status_code == 200:
            print("Login successful!")
            self.root.current = "home"
        else:
            print("Login failed.")


if __name__ == '__main__':
    CafeLibraryApp().run()
