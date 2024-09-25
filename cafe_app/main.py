from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from cafe_app.libs.main_screen import HomeScreen, OTPVerificationScreen, RegistrationCompleteScreen


class CafeLibraryApp(MDApp):
    user_name = StringProperty(None)
    mobile_no = NumericProperty(None)
    otp = NumericProperty(None)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        Builder.load_file('main.kv')

        manager = ScreenManager()
        manager.add_widget(HomeScreen(name='HomeScreen'))
        manager.add_widget(OTPVerificationScreen(name='OTPVerificationScreen'))
        manager.add_widget(RegistrationCompleteScreen(name='RegistrationCompleteScreen'))

        return manager


if __name__ == '__main__':
    CafeLibraryApp().run()
