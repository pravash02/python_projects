from kivymd.app import MDApp
from twilio.rest import Client
import random
from kivy.uix.screenmanager import Screen, SlideTransition


class HomeScreen(Screen):
    def send_otp(self, mobile_no):
        # TODO: Code to send OTP would go here (API integration with SMS service)
        _otp = str(random.randint(1000, 9999))

        app = MDApp.get_running_app()
        app.mobile_number = mobile_no
        app.otp = _otp

        self.send_sms(mobile_no, _otp)

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'OTPVerificationScreen'

    def send_sms(self, mobile_no, otp):
        account_sid = ''
        auth_token = ''
        twilio_number = ''

        # client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     body=f"Your otp code for Cafe Library - {otp}",
        #     from_=twilio_number,
        #     to=mobile_no
        # )
        # print(f"message sent with SID: {message.sid}")

    def logger(self):
        self.ids.welcome_label.text = f"Hey {self.ids.login.text}"

    def clear(self):
        self.ids.mobile_no.text = ""
        self.ids.user_name.text = ""


class OTPVerificationScreen(Screen):
    def verify_otp(self, user_entered_otp):
        app = MDApp.get_running_app()
        # if user_entered_otp == app.otp:
        #     self.do_login(app.user_name, app.mobile_no)
        # else:
        #     print("Invalid OTP. Please try again.")

        # TODO: For Testing Purpose
        if user_entered_otp == "123456":
            self.do_login(app.user_name, app.mobile_no)
        else:
            print("Invalid OTP. Please try again.")

    def do_login(self, user_name, mobile_no):
        app = MDApp.get_running_app()
        print(user_name, mobile_no)

        # TODO: code to insert data into customer table

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'RegistrationCompleteScreen'


class RegistrationCompleteScreen(Screen):
    def go_back_home(self):
        home_screen = self.manager.get_screen('HomeScreen')
        otp_verification = self.manager.get_screen('OTPVerificationScreen')
        home_screen.ids.user_name.text = ''
        home_screen.ids.mobile_no.text = ''
        otp_verification.ids.otp_input.text = ''

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'HomeScreen'
