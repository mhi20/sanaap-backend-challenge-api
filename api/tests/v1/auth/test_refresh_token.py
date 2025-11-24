from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CustomTokenRefreshViewTests(APITestCase):

    def setUp(self):
        self.url = reverse('token_refresh')
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

    def test_refresh_with_valid_token(self):
        refresh_token = RefreshToken.for_user(self.user)
        data = {
            'refresh': str(refresh_token)
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_data)
        self.assertIsInstance(response_data['access'], str)

    def test_refresh_with_invalid_token(self):
        data = {
            'refresh': 'invalid_token'
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response_data)

    def test_refresh_with_miss_param_token(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        response_data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', response_data)

    def test_refresh_with_empty_token(self):
        data = {
            'refresh': ''
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_with_access_token(self):
        refresh_token = RefreshToken.for_user(self.user)
        access_token = str(refresh_token.access_token)
        
        data = {
            'refresh': access_token
        }
        response = self.client.post(self.url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_with_expired_token(self):
        refresh_token = RefreshToken.for_user(self.user)

        data = {
            'refresh': str(refresh_token)
        }
        response = self.client.post(self.url, data, format='json')
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_data)


