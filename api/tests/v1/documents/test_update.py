import io
from unittest import mock
from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from archives.models.document import Document


class DocumentDetailEditTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="adminuser", password="password123")
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.document = Document.objects.create(title="Test Document", uploaded_by=self.user)
        self.endpoint = reverse("documents_details", kwargs={"pk": self.document.id})

    @mock.patch("storages.backends.s3boto3.S3Boto3Storage._save")
    def test_update_document_success(self, mock_s3_save):
        mock_s3_save.side_effect = lambda name, content: name

        file_content = io.BytesIO(b"new file content")
        file_content.name = "updated_file.txt"
        payload = {"title": "Updated Title", "file": file_content}

        response = self.client.put(self.endpoint, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.document.refresh_from_db()
        self.assertEqual(self.document.title, "Updated Title")

    def test_update_document_validation_error(self):
        payload = {"title": ''}
        response = self.client.put(self.endpoint, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, ['title: This field may not be blank.'])
