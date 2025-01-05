# accounts/urls.py


from django.urls import path
from .views import *

urlpatterns = [
    path('verify-email/', EmailVerificationAPIView.as_view(), name='verify_email'),
    path('verify/', VerifyEmailAPIView.as_view(), name='verify_otp'),  # This should accept GET requests
    path('verify-otp/', VerifyEmailWithOtpAPIView.as_view(), name='verify_email_with_otp'),  # New POST endpoint

]