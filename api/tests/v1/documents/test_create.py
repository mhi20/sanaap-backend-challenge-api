import io
from unittest import mock
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class DocumentCreateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        self.user.save()

        self.client.force_authenticate(user=self.user)
        self.endpoint = reverse("documents_list_create")

    @mock.patch("storages.backends.s3boto3.S3Boto3Storage._save")
    def test_create_document_success(self, mock_s3_save):
        mock_s3_save.side_effect = lambda name, content: name

        file_content = io.BytesIO(b"sample content")
        file_content.name = "test_file.txt"

        payload = {
            "title": "test doc",
            "file": file_content,
        }

        response = self.client.post(self.endpoint, payload, format="multipart")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response_data)
        self.assertEqual(response_data["message"], "Document created successfully")

    def test_create_document_missing_file(self):
        payload = {"title": "test doc"}

        response = self.client.post(self.endpoint, payload, format="multipart")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, ['file: No file was submitted.'])

    def test_create_document_file_too_large(self):
        large_content = io.BytesIO(b"m" * (10 * 1024 * 1024 + 1))
        large_content.name = "large_file.txt"

        payload = {
            "title": "large doc",
            "file": large_content,
        }

        response = self.client.post(self.endpoint, payload, format="multipart")
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, ['file: File size cannot exceed 10 MB.'])
