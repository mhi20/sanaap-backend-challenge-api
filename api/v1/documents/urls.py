from django.urls import path

from api.v1.documents.views.document_detail import DocumentDetail
from api.v1.documents.views.list_create import DocumentListCreate

urlpatterns = [
    path("", DocumentListCreate.as_view(), name="documents_list_create"),
    path("<int:pk>", DocumentDetail.as_view(), name="documents_details"),
]