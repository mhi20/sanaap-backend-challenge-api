from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from api.v1.documents.permissions import UserDocumentPermission
from api.v1.documents.serializers.document import DocumentSerializer
from api.v1.documents.services.documents.update import ServiceDocumentUpdate
from archives.models.document import Document
from django.utils.translation import gettext_lazy as _


class DocumentDetail(APIView):
    permission_classes = [UserDocumentPermission]

    @extend_schema(
        summary="Show a document",
        description="Get a document by ID.",
        responses={200: DocumentSerializer}
    )
    def get(self, _, pk):
        document = get_object_or_404(Document, pk=pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Update a document",
        description="Update the title & file by ID.",
        request=DocumentSerializer,
        responses={
            200: OpenApiResponse(
                response=DocumentSerializer,
                description="Document updated successfully",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={"id": 1, "message": "Document updated successfully"},
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Validation error",
                examples=[
                    OpenApiExample(
                        "Validation Error",
                        value={"file": ["File size cannot exceed 10 MB."]},
                    )
                ],
            ),
            404: OpenApiResponse(description="Document not found")
        },
    )
    def put(self, request, pk):
        result_service = ServiceDocumentUpdate(request, pk).process()

        if not result_service.success:
            return Response(result_service.get_error_messages(), status=result_service.status_code)

        document = result_service.data

        return Response(
            {"id": document.id, "message": _("Document updated successfully")},
            status=result_service.status_code,
        )


    @extend_schema(
        summary="Delete a document",
        description="Delete a document by ID",
        responses={
            204: OpenApiResponse(description="Document deleted successfully"),
            404: OpenApiResponse(description="Document not found")
        },
    )
    def delete(self, _, pk):
        document = get_object_or_404(Document, pk=pk)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

