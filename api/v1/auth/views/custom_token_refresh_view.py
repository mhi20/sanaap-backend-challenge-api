from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        summary="Refresh JWT token",
        request=TokenRefreshSerializer,
        responses={ 200: TokenRefreshSerializer },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)