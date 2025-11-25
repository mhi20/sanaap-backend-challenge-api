from rest_framework import status
from api.v1.documents.serializers.document import DocumentSerializer
from core.services.base import BaseServiceObject
from core.services.service_result import ServiceResult

class ServiceDocumentCreate(BaseServiceObject):
    def __init__(self, request, user):
        super().__init__()
        self.request = request
        self.user = user
        self.document = None
        self.service_result = None

    def process(self) -> ServiceResult:
       self.__save_document()

       return self.service_result

    @BaseServiceObject.service_step
    def __save_document(self):
        serializer = self.__serializer()

        if serializer.is_valid():
            document = serializer.save(uploaded_by=self.user)

            self.service_result = ServiceResult(
                success=True,
                data=document,
                status_code=status.HTTP_201_CREATED,
            )
            return

        self.service_result = ServiceResult(
            success=False,
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    def __serializer(self):
        return DocumentSerializer(
            data=self.request.data
        )
