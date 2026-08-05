import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.config import EMAIL, EMAIL_PASSWORD


def send_email(to_email, subject, body):

    msg = MIMEMultipart()

    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(
        EMAIL,
        EMAIL_PASSWORD,
    )

    server.sendmail(
        EMAIL,
        to_email,
        msg.as_string(),
    )

    server.quit()