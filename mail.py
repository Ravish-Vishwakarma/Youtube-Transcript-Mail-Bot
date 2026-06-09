import smtplib
from email.mime.text import MIMEText

from helper import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_RECIPIENT


def send_email(subject: str, body: str):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Skipping email: EMAIL_ADDRESS or EMAIL_PASSWORD not set")
        return

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_RECIPIENT

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

    print(f"Email sent to {EMAIL_RECIPIENT}")
