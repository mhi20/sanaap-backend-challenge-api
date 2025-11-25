from uuid import uuid4
from django.contrib.auth.models import User
from django.db import models

def s3_file_path(_, filename: str):
    return f"{uuid4().hex}.{filename.split(".")[-1]}"

class Document(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    file = models.FileField(
        upload_to=s3_file_path,
        null=False,
        blank=False)

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="documents",
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

