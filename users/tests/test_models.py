from django.test import TestCase

from users.models import CustomUser


class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "contact": "1234567890",
            "password": "testpassword123",
        }

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.contact, self.user_data["contact"])
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpassword123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_user_str(self):
        user = CustomUser.objects.create_user(**self.user_data)
        expected_str = (
            f"{user.first_name} {user.last_name} || {user.email} || {user.contact}"
        )
        self.assertEqual(str(user), expected_str)

    def test_full_name(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.full_name, "Test User")

    def test_soft_delete(self):
        user = CustomUser.objects.create_user(**self.user_data)
        user.soft_delete(archive=True)
        self.assertTrue(user.archive)

        user.soft_delete(archive=False)
        self.assertFalse(user.archive)
