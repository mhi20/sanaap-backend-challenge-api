import django_filters
from archives.models.document import Document

class DocumentFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title",lookup_expr="icontains")
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Document
        fields = ["title", "created_at", "uploaded_by"]
