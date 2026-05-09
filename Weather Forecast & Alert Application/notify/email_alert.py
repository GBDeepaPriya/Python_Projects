import os
import smtplib

from dotenv import load_dotenv
from email.mime.text import MIMEText

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ==========================================
# SEND EMAIL FUNCTION
# ==========================================

def send_email(receiver, subject, body):

    try:

        msg = MIMEText(body)

        msg["Subject"] = subject

        msg["From"] = EMAIL_USER

        msg["To"] = receiver

        # ==================================
        # SMTP SERVER
        # ==================================

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        # ==================================
        # LOGIN
        # ==================================

        server.login(
            EMAIL_USER,
            EMAIL_PASSWORD
        )

        # ==================================
        # SEND EMAIL
        # ==================================

        server.sendmail(
            EMAIL_USER,
            receiver,
            msg.as_string()
        )

        server.quit()

        print("Email Sent Successfully")

    except Exception as e:

        print("Email Error:", e)