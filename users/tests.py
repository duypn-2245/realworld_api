from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User
from .factories import UserFactory

class RegisterTests(APITestCase):
    def setUp(self):
        self.url = reverse("user-register")
        self.data = {
            "user": {
                "email": "pham.ngoc.duy@sun-asterisk.com",
                "password": "Aa@123456",
                "username": "duypn2245"
            }
        }
    
    def test_register_user(self):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        expected_response = response.data["user"]
        expected_data = self.data["user"]
        self.assertEqual(expected_response["email"], expected_data["email"])
        self.assertEqual(expected_response["username"], expected_data["username"])
        self.assertIsNone(expected_response["bio"])
        self.assertIsNone(expected_response["image"])

class LoginTests(APITestCase):
    def setUp(self):
        self.url = reverse("user-login")
        self.user = UserFactory(
            email="pham.ngoc.duy@sun-asterisk.com",
            password="Aa@123456"
        )
        self.data = {
            "email": "pham.ngoc.duy@sun-asterisk.com",
            "password": "Aa@123456"
        }

    def test_login_success(self):
        response = self.client.post(self.url, data=self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = response.data
        self.assertIsNotNone(expected_response["access"])
        self.assertIsNotNone(expected_response["refresh"])

class UserInforTests(APITestCase):
    def setUp(self):
        self.url = reverse("user-infor")
        self.user = UserFactory(
            email="pham.ngoc.duy@sun-asterisk.com",
            password="Aa@123456"
        )
    
    def test_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = response.data["user"]
        expected_data = self.user
        self.assertEqual(expected_response["email"], expected_data.email)
        self.assertEqual(expected_response["username"], expected_data.username)
        self.assertIsNone(expected_response["bio"])
        self.assertIsNone(expected_response["image"])
    
    def test_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProfileTests(APITestCase):
    def setUp(self):
        self.current_user = UserFactory(
            email="pham.ngoc.duy@sun-asterisk.com", password="Aa@123456", username="duypn2245"
        )
        self.user = UserFactory(
            email="phamngocduytcnh@gmail.com", password="Aa@123456", username="phamngocduy"
        )
        self.url = reverse("user-profile", kwargs={"username": self.user.username})
    
    def test_with_auth(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_response = response.data["user"]
        expected_data = self.user
        self.assertEqual(expected_response["email"], expected_data.email)
        self.assertEqual(expected_response["username"], expected_data.username)
        self.assertIsNone(expected_response["bio"])
        self.assertIsNone(expected_response["image"])
        self.assertEqual(expected_response["following"], False)

    def test_without_auth(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
