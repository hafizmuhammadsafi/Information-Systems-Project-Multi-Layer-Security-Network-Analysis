import random
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import bcrypt

# ----------------- OTP -----------------
def generate_otp():
    return str(random.randint(100000, 999999))

# ----------------- Email -----------------
def send_email(receiver_email, subject, body):
    # Configure SMTP here (example using Gmail)
    sender_email = "muhammadsafihafiz@gmail.com"
    sender_password = "gkcuojjiaciblpkh"
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

# ----------------- Password -----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

# ----------------- Time -----------------
def current_time():
    return datetime.now()

def time_plus_minutes(minutes):
    return datetime.now() + timedelta(minutes=minutes)

