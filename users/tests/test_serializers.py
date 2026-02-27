from django.test import TestCase
from rest_framework_simplejwt.tokens import AccessToken

from users.api.v1.serializers.auth import (
    CustomTokenObtainPairSerializer,
    UserTokenSerializer,
)
from users.api.v1.serializers.user import CustomUserSerializer
from users.models import CustomUser


class SerializerTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            contact="1234567890",
            password="testpassword123",
        )

    def test_custom_user_serializer(self):
        serializer = CustomUserSerializer(instance=self.user)
        expected_fields = {
            "id",
            "uuid",
            "first_name",
            "last_name",
            "contact",
            "email",
            "is_admin",
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)
        self.assertEqual(serializer.data["email"], self.user.email)

    def test_custom_token_obtain_pair_serializer(self):
        token_str = CustomTokenObtainPairSerializer.get_token(self.user)
        token = AccessToken(token_str)

        self.assertEqual(token["id"], self.user.id)
        self.assertEqual(token["is_admin"], self.user.is_admin)
        self.assertEqual(token["is_superuser"], self.user.is_superuser)

    def test_user_token_serializer_valid(self):
        data = {"token": "some-random-token-string"}
        serializer = UserTokenSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_token_serializer_invalid(self):
        data = {}
        serializer = UserTokenSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("token", serializer.errors)
