from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.app import App
import requests
from kivy.properties import StringProperty, NumericProperty
from kivymd.app import MDApp
from kivymd.toast import toast
# from kivy_zbarcam import ZBarCam


# Kivy Layout from kv string
kv = '''
ScreenManager:
    LoginScreen:
    OtpScreen:
    MenuScreen:
    CartScreen:
    SuccessScreen:
    BarcodeScreen:

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        MDLabel:
            text: "Login to Book Cafe"
            halign: "center"
            font_style: "H5"
        MDTextField:
            id: mobile
            hint_text: "Mobile no"
            helper_text: "Enter your registered mobile number"
            helper_text_mode: "on_focus"
            icon_right: "cellphone"
            pos_hint: {"center_x": 0.5, "center_y": 0.6}
            size_hint_x: None
            width: 300
        MDRaisedButton:
            text: "Send OTP"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.send_otp(mobile.text)

<OtpScreen>:
    name: 'otp'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        MDLabel:
            text: "Enter OTP"
            halign: "center"
            font_style: "H5"
        MDTextField:
            id: otp
            hint_text: "Enter OTP"
            icon_right: "lock"
            pos_hint: {"center_x": 0.5}
            size_hint_x: None
            width: 300
        MDRaisedButton:
            text: "Validate OTP"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.validate_otp(otp.text)

<MenuScreen>:
    name: 'menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        MDLabel:
            text: "Menu"
            halign: "center"
            font_style: "H5"
        RecycleView:
            id: menu_list
            viewclass: 'MenuItem'
            RecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        MDRaisedButton:
            text: "View Cart"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.view_cart()
                
<MenuItem@BoxLayout>:
    orientation: 'horizontal'
    padding: 10
    MDLabel:
        text: root.name
    MDLabel:
        text: str(root.price)
    MDRaisedButton:
        text: "Add to Cart"
        on_release: app.add_to_cart(root.name, root.price)

<CartScreen>:
    name: 'cart'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        MDLabel:
            text: "Cart"
            halign: "center"
            font_style: "H5"
        RecycleView:
            id: cart_list
            viewclass: 'CartItem'
            RecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        MDLabel:
            id: total_amount
            text: "Total amount: 0.0"
            halign: "center"
            font_style: "H6"
        MDRaisedButton:
            text: "Place Order"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.place_order()

<CartItem@BoxLayout>:
    orientation: 'horizontal'
    padding: 10
    MDLabel:
        text: root.name
    MDLabel:
        text: str(root.price)

<SuccessScreen>:
    name: 'success'
    BoxLayout:
        orientation: 'vertical'
        padding: 50
        spacing: 20
        MDLabel:
            text: "Order Placed Successfully"
            halign: "center"
            font_style: "H5"
        MDRaisedButton:
            text: "Go to Home"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.go_home()

<BarcodeScreen>:
    name: 'barcode'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        MDLabel:
            text: "Scan Barcode"
            halign: "center"
            font_style: "H5"
        MDRaisedButton:
            text: "Scan Now"
            pos_hint: {"center_x": 0.5}
            on_release:
                app.scan_barcode()
'''


# class BarcodeScreen(BoxLayout):
#     def on_barcode_scanned(self, barcode):
#         import webbrowser
#         webbrowser.open(barcode)


class LoginScreen(Screen):
    pass


class OtpScreen(Screen):
    pass


class SuccessScreen(Screen):
    pass


class MenuScreen(Screen):
    def on_enter(self):
        response = requests.get('http://127.0.0.1:5000/menu')
        if response.status_code == 200:
            menu_data = response.json()
            self.ids.menu_list.data = [{'name': item['name'], 'price': item['price']} for item in menu_data]


class CartScreen(Screen):
    def on_enter(self):
        app = MDApp.get_running_app()
        response = requests.get(f'http://127.0.0.1:5000/cart?token={app.token}')
        if response.status_code == 200:
            cart_data = response.json()
            self.ids.cart_list.data = [{'name': item['name'], 'price': item['price']} for item in cart_data]
            total_amount = sum(item['price'] for item in cart_data)
            self.ids.total_amount.text = f"Total Amount: ${total_amount:.2f}"
        else:
            toast(f"{response.json().get('error')}")


class MenuItem(BoxLayout):
    name = StringProperty()
    price = NumericProperty()


class CartItem(BoxLayout):
    name = StringProperty()
    price = NumericProperty()
    total = NumericProperty()


# class BarcodeApp(App):
#     def build(self):
#         return BarcodeScreen()


class BookCafeApp(MDApp):
    mobile = None
    cart = []
    token = None

    def build(self):
        return Builder.load_string(kv)

    def send_otp(self, mobile):
        response = requests.post('http://127.0.0.1:5000/login', json={'mobile': mobile})
        if response.status_code == 200:
            self.mobile = mobile
            self.token = response.json().get('token')
            self.root.current = 'otp'  # switch to <OtpScreen>
        else:
            toast(f"{response.json().get('error')}")

    def validate_otp(self, otp):
        response = requests.post(f'http://127.0.0.1:5000/otp-validation/{otp}', json={'mobile': self.mobile})
        if response.reason == 'NOT FOUND':
            toast(f"Please enter OTP")

        if response.status_code == 200:
            self.root.current = 'menu'  # Switch to <MenuScreen>

        if response.status_code == 400:
            toast(f"{response.json().get('error')}")

    def add_to_cart(self, name, price):
        response = requests.post('http://127.0.0.1:5000/cart', json={'name': name, 'price': price, 'token': self.token})
        if response.status_code == 200:
            toast(f"{name} added to cart")
        else:
            toast(f"{response.json().get('error')}")

    def view_cart(self):
        response = requests.get(f'http://127.0.0.1:5000/cart?token={self.token}')
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                toast(f"Cart is Empty")
            else:
                self.root.current = 'cart'  # Switch to <CartScreen>
        else:
            toast(f"{response.json().get('error')}")

    def place_order(self):
        response = requests.post('http://127.0.0.1:5000/place-order', json={'token': self.token})
        if response.status_code == 200:
            self.cart = []
            toast("Order Placed Successfully")
            self.root.current = 'success'  # Switch to <SuccessScreen>

    def go_home(self):
        self.root.get_screen('login').ids.mobile.text = ''
        self.root.get_screen('otp').ids.otp.text = ''
        self.root.current = 'login'


if __name__ == '__main__':
    BookCafeApp().run()
