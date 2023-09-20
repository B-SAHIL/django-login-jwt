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



def check_duplicates(email, phone):
    if email is None or email == '':
        return Response (f"Please specify email")
    if email is not None:
        User.objects.filter(email=email).exists()
        return Response (f"wtih email = '{email}' this email user aleary exist")
    if phone is not None:
        User.objects.filter(phone=phone).exists()
        return Response (f"wtih phone = '{phone}' this phone user aleary exist")
    else:
         return True



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer
    queryset = User.objects.none()

    def create(self, request, *args, **kwargs):
        data = self.request.data
        email_from_data = data.get('email')
        phone = data.get('phone')
        check_duplicates(email=email_from_data, phone=phone)
        serizalizer = RegistrationSerializer(data=data)
        if serizalizer.is_valid():
            serizalizer.save()
            return Response(serizalizer.data)
        else:
            return Response(serizalizer.errors)

        
        
        