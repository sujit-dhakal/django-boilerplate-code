from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APITestCase

from users.models import CustomUser


class ViewsTest(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.get_user_url = reverse("get_user")

        self.user_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "contact": "1234567890",
            "password": "testpassword123",
        }
        self.user = CustomUser.objects.create_user(**self.user_data)
        self.user.set_password(self.user_data["password"])
        self.user.save()

    def test_register_view_success(self):
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "contact": "0987654321",
            "password": "newpassword123",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "User created successfully")
        self.assertTrue(CustomUser.objects.filter(email=data["email"]).exists())

    def test_register_view_missing_password(self):
        data = {
            "email": "nopass@example.com",
            "first_name": "No",
            "last_name": "Pass",
            "contact": "1111111111",
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Password is required")

    def test_login_view_success(self):
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successfully logged in")
        self.assertIn("data", response.data)

    def test_login_view_invalid_credentials(self):
        data = {"email": self.user_data["email"], "password": "wrongpassword"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 401)

    def test_get_user_data_view_valid_token(self):
        # Generate a valid JWT token manually for testing
        payload = {
            "user_uuid": str(self.user.uuid),
            "exp": datetime.now() + timedelta(days=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response = self.client.post(self.get_user_url, {"token": token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Successfully fetched user data")
        self.assertEqual(response.data["data"]["email"], self.user.email)

    def test_get_user_data_view_no_token(self):
        response = self.client.post(self.get_user_url, {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "No token Provided")

    def test_get_user_data_view_invalid_token(self):
        response = self.client.post(self.get_user_url, {"token": "invalid-token"})
        self.assertEqual(response.status_code, 400)
        # The jwt library returns "Not enough segments" or "not enough segments"
        self.assertIn("enough", response.data["message"].lower())
