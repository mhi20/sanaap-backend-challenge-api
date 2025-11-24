from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class CustomTokenObtainPairViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('token_obtain_pair')
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_login_with_valid_signin(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_data)
        self.assertIn('refresh', response_data)
        self.assertIsInstance(response_data['access'], str)
        self.assertIsInstance(response_data['refresh'], str)

    def test_login_with_invalid_username(self):
        data = {
            'username': 'wronguser',
            'password': self.password
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_data)

    def test_login_with_invalid_password(self):
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_data)

    def test_login_with_missing_username(self):
        data = {
            'password': self.password
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response_data)

    def test_login_with_missing_password(self):
        data = {
            'username': self.username
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response_data)

    def test_login_with_empty_username_password(self):
        data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)




