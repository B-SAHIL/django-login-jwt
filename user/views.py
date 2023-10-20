# external imports
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
import random
from datetime import datetime
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

# local imports 
from .models import User, Otp
from .serializer import RegistrationSerializer, AuthTokenSerializer, OtpSerializer
from .email import send_email


def generate_otp():
    # Generate a 5-digit OTP
    otp = ''.join(random.choice('0123456789') for i in range(5))
    return otp


class RegisterViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = [AllowAny]
    queryset = User.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegistrationSerializer
        if self.action == 'request_otp':
            return OtpSerializer

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response("No data was given for registration", status=status.HTTP_400_BAD_REQUEST)

        response = self.validate_and_create_user(request.data)
        return response

    def validate_and_create_user(self, data):
        phone = data.get('phone')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')

        if phone and not (len(phone) == 10):
            return Response("Please enter a valid 10-digit phone number", status=status.HTTP_400_BAD_REQUEST)

        if not (first_name and last_name):
            return Response("Both first_name and last_name are required", status=status.HTTP_400_BAD_REQUEST)

        if not email:
            return Response("Email is required for user creation", status=status.HTTP_400_BAD_REQUEST)

        try:
            user_with_email = User.objects.get(email=email)
            return Response("A user with this email already exists.", status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass

        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='auth-otp', url_name='auth-otp')
    def request_otp(self, request, *args, **kwargs):
        if not request.data.get('email'):
            return Response("Email is required for otp sending", status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('email'):
            try:
                User.objects.get(email=request.data.get('email'))
            except:
                return Response("user with this email does not exists.", status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=request.data.get('email'))
        if Otp.objects.get(to_id=user.id):
            otp = Otp.objects.get(to=user.id)
            otp.otp = generate_otp()
            otp.request_time = datetime.now()
            otp.save()
            context = {
                'otp': otp.otp
            }
            html_message = render_to_string('otp_email.html', context=context)
            send_email(from_email='noreply@yopmail.com', subject='Otp for Sign Up',
                       recipient_list=[request.data.get('email')], html_message=html_message)
            return Response(
                f"otp hase been resend to {request.data.get('email')}",
                status=status.HTTP_200_OK
            )
        else:
            data = {
                "to": user.id,
                "otp": generate_otp(),
                "request_time": datetime.now()
            }
            context = data
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                html_message = render_to_string('otp_email.html', context=context)
                send_email(from_email='noreply@yopmail.com', subject='Otp for Sign Up',
                           recipient_list=[request.data.get('email')], html_message=html_message)
                return Response(
                    f"otp has been send to {request.data.get('email')}", status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

    @action(methods=['POST'], detail=False, url_path='verify-otp', url_name='verify-otp')
    def verify_otp(self, request, *args, **kwargs):
        if not request.data:
            return Response("Please enter email and otp", status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('email'):
            return Response("Email is required for verifying account", status=status.HTTP_400_BAD_REQUEST)
        if not request.data.get('otp'):
            return Response("Otp is required for verifying account", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=request.data.get('email'))
            otp = Otp.objects.get(to=user.id)
        except:
            return Response(
                "User does not exist", status=status.HTTP_400_BAD_REQUEST
            )
        if user.is_active == True:
            return Response(
                "User already verified", status=status.HTTP_400_BAD_REQUEST
            )
        now = timezone.now()
        expiration_time = otp.request_time + timedelta(minutes=10)
        print(now, "now", expiration_time, "erp")
        if now > expiration_time:
            return Response(
                "Otp  is expired request new", status=status.HTTP_400_BAD_REQUEST
            )
        if otp.otp == request.data.get('otp'):
            user.is_active = True
            user.save()
            serializer = AuthTokenSerializer(instance=user)
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        else:
            return Response(
                "Otp does not match", status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=['POST'], detail=False, url_path='auth-token', url_name='auth-token')
    def auth_token(self, request, *args, **kwargs):
        if not request.data.get('email'):
            return Response("Email is required for user login", status=status.HTTP_400_BAD_REQUEST
                            )
        if request.data.get('email'):
            try:
                User.objects.get(email=request.data.get('email'))
            except:
                return Response("user with this email does not exists.", status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=request.data.get('email'))
        if not user.is_active:
            return Response("Please verify  your email.", status=status.HTTP_400_BAD_REQUEST)
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.get(email=email)
        if user.check_password(password):
            serializer = AuthTokenSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("serializer.errors", status=status.HTTP_400_BAD_REQUEST)
