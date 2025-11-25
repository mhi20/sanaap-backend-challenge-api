from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from api.v1.documents.filters import DocumentFilter
from archives.models.document import Document
from api.v1.documents.permissions import UserDocumentPermission
from api.v1.documents.serializers.document import DocumentSerializer
from api.v1.documents.services.documents.create import ServiceDocumentCreate
from django.utils.translation import gettext_lazy as _

class DocumentListCreate(APIView):
    permission_classes = [UserDocumentPermission]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination
    filterset_class = DocumentFilter

    @extend_schema(
        summary="List all documents",
        description="list of all documents",
        responses={
            200: DocumentSerializer(many=True),
        }
    )
    def get(self, request):
        documents = Document.objects.all()

        for backend in self.filter_backends:
            documents = backend().filter_queryset(request, documents, self)

        paginator = self.pagination_class()
        paginated_documents = paginator.paginate_queryset(documents, request)

        serializer = DocumentSerializer(paginated_documents, many=True)

        return paginator.get_paginated_response(serializer.data)


    @extend_schema(
        summary="Create a new document",
        description="Upload a new document with a title and file",
        request=DocumentSerializer,
        responses={
            201: OpenApiResponse(
                response=DocumentSerializer,
                description="Document successfully created",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={"id": 12, "message": "Document created successfully"},
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
        },
    )
    def post(self, request):
        result_service = ServiceDocumentCreate(request, request.user).process()

        if not result_service.success:
            return Response(result_service.get_error_messages(), status=result_service.status_code)

        document = result_service.data

        return Response(
            {"id": document.id, "message": _("Document created successfully")},
            status=result_service.status_code,
        )
