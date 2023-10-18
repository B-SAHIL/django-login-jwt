from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny

from .models import User
from .serializer import UserSerializer, RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RegisterViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    queryset = User.objects.none()

    def create(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                "No data was given for registration", status=status.HTTP_400_BAD_REQUEST
            )
        if request.data:
            if request.data.get('phone'):
                if len(request.data.get('phone')) > 10 or len(request.data.get('phone')) < 10:
                    return Response(
                        "Please enter valid Phone number",
                        status=status.HTTP_400_BAD_REQUEST
                    )
            if request.data.get('first_name') is None or request.data.get('last_name') is None:
                print(request.data.get('first_name'), request.data.get('last_name'))
                return Response(
                    "Both first_name and last_name are required",
                    status=status.HTTP_400_BAD_REQUEST
                )
            if not request.data.get('email'):
                return Response(
                    "Email is required for user creation",
                    status=status.HTTP_400_BAD_REQUEST
                )
            if request.data.get('email'):
                try:
                    user_with_email = User.objects.get(email=request.data.get('email'))
                    if user_with_email:
                        return Response(
                            "A user with this email already exists.",
                            status=status.HTTP_400_BAD_REQUEST
                        )
                except ObjectDoesNotExist:
                    pass
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        
        
        
