from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from archives.models.document import Document

class DocumentDetailShowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="adminuser", password="password123")
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.document = Document.objects.create(title="Test Document", uploaded_by=self.user)
        self.endpoint = reverse("documents_details", kwargs={"pk": self.document.id})

    def test_get_document_success(self):
        response = self.client.get(self.endpoint)
        response_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["id"], str(self.document.id))
        self.assertEqual(response_data["title"], self.document.title)

    def test_get_document_not_found(self):
        endpoint = reverse("documents_details", kwargs={"pk": 9999})
        response = self.client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)