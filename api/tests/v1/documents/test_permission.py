import io
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DocumentPermissionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="normaluser", password="password123")
        self.client.force_authenticate(user=self.user)
        self.endpoint = reverse("documents_list_create")

    def test_create_document_forbidden_for_non_admin_user(self):
        file_content = io.BytesIO(b"sample content")
        file_content.name = "test_file.txt"

        payload = {
            "title": "test document",
            "file": file_content,
        }

        response = self.client.post(self.endpoint, payload, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
