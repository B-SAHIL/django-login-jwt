from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class RegistrationSerializer(serializers.ModelSerializer):
    jwt_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'jwt_token',  'username','email','trial_ended','first_name','last_name','email','phone','password']

        extra_kwargs = {'password': {'write_only': True},
                        'username': {'read_only': True},
                        'jwt_token': {'read_only': True},
                        'trial_ended': {'read_only': True},
                        'id': {'read_only': True}, }

    

    def get_jwt_token(self, user):
        # Generate the JWT access token using rest_framework_simplejwt
        refresh = RefreshToken.for_user(user)
        jwt_token = str(refresh.access_token)
        return jwt_token
    

    def create(self, validated_data):
        # Ensure that the password is hashed before saving it to the database
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    
