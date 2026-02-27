from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.api.v1.serializers.user import CustomUserSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        update_last_login(None, user)
        token = super().get_token(user)
        token["id"] = user.id
        token["is_admin"] = user.is_admin
        token["is_superuser"] = user.is_superuser
        return str(token.access_token)


class RegisterRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    contact = serializers.CharField()
    password = serializers.CharField(write_only=True)


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class BaseResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class AuthResponseSerializer(BaseResponseSerializer):
    data = serializers.CharField()


class UserDataResponseSerializer(BaseResponseSerializer):
    data = CustomUserSerializer()
