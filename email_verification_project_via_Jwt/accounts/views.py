
# accounts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import generate_otp, send_verification_email
from django.core.cache import cache
from django.contrib.auth import get_user_model

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.permissions import IsAuthenticated


from rest_framework_simplejwt.tokens import RefreshToken


class EmailVerificationAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if email and password:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                if user.email_verified:
                    return Response({"error": "Email already verified."}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user = User(email=email)
                user.set_password(password)  # Set the password
                user.save()  # Save the user to the database

            otp = generate_otp()
            send_verification_email(email, otp)
            cache.set(email, otp, timeout=300)  # OTP valid for 5 minutes
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid input."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailAPIView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        otp = request.query_params.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(email)

        if cached_otp and str(otp) == str(cached_otp):
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user.email_verified = True
                user.save()
                cache.delete(email)  # Invalidate the OTP after successful verification
                
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Email verified successfully!",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User  not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailWithOtpAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(email)

        if cached_otp and str(otp) == str(cached_otp):
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user.email_verified = True
                user.save()
                cache.delete(email)  # Invalidate the OTP after successful verification
                
                # Generate JWT token
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Email verified successfully!",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User  not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):

    pass

class CustomTokenRefreshView(TokenRefreshView):
    pass

