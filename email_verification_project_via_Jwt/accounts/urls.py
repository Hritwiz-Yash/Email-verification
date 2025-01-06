# accounts/urls.py

from django.urls import path
from .views import (
    EmailVerificationAPIView,
    VerifyEmailAPIView,
    VerifyEmailWithOtpAPIView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)

urlpatterns = [
    path('verify-email/', EmailVerificationAPIView.as_view(), name='verify_email'),
    path('verify/', VerifyEmailAPIView.as_view(), name='verify_otp'),
    path('verify-otp/', VerifyEmailWithOtpAPIView.as_view(), name='verify_email_with_otp'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # JWT login
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),  # JWT refresh
]