from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTestCase(APITestCase):

    def setUp(self):
        """Create a user for login/profile tests"""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            phone="1234567890"
        )

        self.signup_url = reverse("user_signup")
        self.token_url = reverse("token_obtain_pair")
        self.profile_url = reverse("user_profile")

    # ----------------------------------------------------
    # USER SIGNUP
    # ----------------------------------------------------
    def test_user_signup_success(self):
        """User can sign up successfully"""
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
            "phone": "555111222",
            "date_of_birth": "2000-01-01"
        }

        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(User.objects.count(), 2)

    def test_user_signup_invalid(self):
        """Invalid signup returns errors"""
        data = {
            "username": "",
            "email": "not-an-email",
            "password": "short"
        }

        response = self.client.post(self.signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    # ----------------------------------------------------
    # LOGIN (TOKEN)
    # ----------------------------------------------------
    def test_login_success(self):
        """User can login and receive JWT token"""
        data = {"username": "testuser", "password": "testpass123"}

        response = self.client.post(self.token_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        """Invalid login credentials return error"""
        data = {"username": "testuser", "password": "wrongpass"}

        response = self.client.post(self.token_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("detail", response.data)

    # ----------------------------------------------------
    # USER PROFILE RETRIEVE
    # ----------------------------------------------------
    def authenticate(self):
        """Helper: authenticate the test user"""
        response = self.client.post(
            self.token_url,
            {"username": "testuser", "password": "testpass123"},
            format="json"
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_profile_retrieve(self):
        """Authenticated user can retrieve their profile"""
        self.authenticate()

        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    def test_profile_retrieve_unauthenticated(self):
        """Unauthenticated user cannot access profile"""
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------------------------------------------
    # USER PROFILE UPDATE
    # ----------------------------------------------------
    def test_profile_update(self):
        """Authenticated user can update their profile"""
        self.authenticate()

        data = {"phone": "999888777"}

        response = self.client.patch(self.profile_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "999888777")

