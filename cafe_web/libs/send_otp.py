import os
import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class OTPClass:
    def __init__(self, email_id, user_name):
        self.smtp = smtplib.SMTP('smtp.gmail.com', 587)
        self.email_id = email_id
        self.user_name = user_name
        self.otp = str(random.randint(1000, 9999))
        self.msg_body = f"""\
        Dear {self.user_name},

        Your One-Time Password (OTP) for login is: {self.otp}

        If you did not request this code, please ignore this email.


        Thank you,
        Pints, Pages and Pour Overs Team
        """

        self.message = MIMEMultipart()
        self.message['From'] = "pravash.cse@gmail.com"
        self.message['To'] = self.email_id
        self.message['Subject'] = f"Your OTP - {self.otp}"

        # Attach the body to the email message
        self.message.attach(MIMEText(self.msg_body, 'plain'))

    def __call__(self, *args, **kwargs):
        self.smtp.starttls()
        self.smtp.login("pravash.cse@gmail.com", "flwb sjlt yihk htyo")

        self.smtp.sendmail('&&&&&&&&&&&', self.email_id, self.message.as_string())

        return self.otp


if __name__ == "__main__":
    obj = OTPClass("test@gmail.com")
    obj()
