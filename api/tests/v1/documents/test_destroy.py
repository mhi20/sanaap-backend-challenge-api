from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from archives.models.document import Document


class DocumentDetailDeleteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="adminuser", password="password123")
        admin_group, _ = Group.objects.get_or_create(name="admin")
        self.user.groups.add(admin_group)
        self.user.save()
        self.client.force_authenticate(user=self.user)

        self.document = Document.objects.create(title="Test Document", uploaded_by=self.user)
        self.endpoint = reverse("documents_details", kwargs={"pk": self.document.id})

    def test_delete_document_success(self):
        response = self.client.delete(self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Document.objects.filter(id=self.document.id).exists())

    def test_delete_document_not_found(self):
        endpoint = reverse("documents_details", kwargs={"pk": 9999})
        response = self.client.delete(endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
