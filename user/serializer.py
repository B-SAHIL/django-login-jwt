from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Otp


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id',  'username','email','trial_ended','first_name','last_name','email','phone','password']

        extra_kwargs = {'password': {'write_only': True},
                        'username': {'read_only': True},
                        'jwt_token': {'read_only': True},
                        'trial_ended': {'read_only': True},
                        'id': {'read_only': True}, }

    def create(self, validated_data):
        # Ensure that the password is hashed before saving it to the database
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = False
        return super().create(validated_data)


class AuthTokenSerializer(serializers.ModelSerializer):
    jwt_token = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'jwt_token','email','trial_ended','first_name','last_name','email','phone']

        extra_kwargs = {'username': {'read_only': True},
                        'jwt_token': {'read_only': True},
                        'trial_ended': {'read_only': True},
                        'id': {'read_only': True}, }
        
    def get_jwt_token(self, instance):
        refresh = RefreshToken.for_user(instance)
        jwt_token = str(refresh.access_token)
        return jwt_token


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        fields = ['to', 'otp', 'request_time']