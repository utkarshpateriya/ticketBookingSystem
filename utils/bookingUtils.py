import sqlite3
import datetime
import threading
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP Configuration
EMAIL_HOST = 'your_email_host'
EMAIL_PORT = 587
EMAIL_USER = 'your_email_username'
EMAIL_PASSWORD = 'your_email_password'


def send_email(recipient, subject, message):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()
    server.login(EMAIL_USER, EMAIL_PASSWORD)
    text = msg.as_string()
    server.sendmail(EMAIL_USER, recipient, text)
    server.quit()

def send_reminder(train_id, departure_time):
    current_time = datetime.datetime.now()
    reminder_time = departure_time - datetime.timedelta(minutes=30)
    delay = (reminder_time - current_time).total_seconds()
    threading.Timer(delay, send_email, args=[train_id]).start()