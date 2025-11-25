from rest_framework import status, exceptions
from api.v1.documents.serializers.document import DocumentSerializer
from archives.models.document import Document
from core.services.base import BaseServiceObject
from core.services.service_result import ServiceResult


class ServiceDocumentUpdate(BaseServiceObject):
    def __init__(self, request, document_id):
        super().__init__()
        self.request = request
        self.document_id = document_id
        self.document = None
        self.service_result = None


    def process(self) -> ServiceResult:
       self.__find_document()
       self.__save_document()

       return self.service_result

    @BaseServiceObject.service_step
    def __find_document(self):
        self.document = Document.objects.filter(pk=self.document_id).first()

        if not self.document:
            raise exceptions.NotFound()

    def __save_document(self):
        serializer = self.__serializer()

        if serializer.is_valid():
            kwargs = {}
            if 'file' in self.request.FILES:
                kwargs['uploaded_by'] = self.request.user

            updated_document = serializer.save(**kwargs)

            self.service_result = ServiceResult(
                success=True,
                data=updated_document,
                status_code=status.HTTP_200_OK,
            )
            return

        self.service_result = ServiceResult(
            success=False,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def __serializer(self):
        return DocumentSerializer(
            instance=self.document,
            data=self.request.data,
            partial=True
        )
