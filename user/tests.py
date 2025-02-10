from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

REGISTER_URL = reverse("register")
TOKEN_URL = reverse("token_obtain")
PROFILE_URL = reverse("user_profile")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a new user is successful"""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_token(self):
        """Test that a token is created for the user"""
        payload = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        self.user = create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged-in user"""
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {"first_name": "New Name"}
        res = self.client.put(PROFILE_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, payload["first_name"])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
