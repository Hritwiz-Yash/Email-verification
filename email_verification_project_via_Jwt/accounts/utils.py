# accounts/utils.py

import random
from django.core.mail import send_mail

def generate_otp():
    return random.randint(100000, 999999)

def send_verification_email(email, otp):
    verification_link = f"http://localhost:8000/accounts/verify/"
    subject = "Email Verification"
    message = f"Your OTP is {otp}. Click the link to verify: {verification_link}?email={email}&otp={otp}"
    send_mail(subject, message, 'from@example.com', [email])