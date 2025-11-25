from rest_framework import serializers
from archives.models.document import Document
from api.v1.documents.validators.document import validate_document_file_size


class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(required=True)
    file = serializers.FileField(required=True, validators=[validate_document_file_size])

    class Meta:
        model = Document
        fields = ["id", "title", "file", "created_at", "updated_at"]
