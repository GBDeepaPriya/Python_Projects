import smtplib
from email.message import EmailMessage
from src.config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to_email, subject, body):

    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True, None

    except Exception as e:
        return False, str(e)