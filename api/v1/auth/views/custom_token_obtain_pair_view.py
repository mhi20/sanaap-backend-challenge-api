from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        summary="Login with username and password",
        request=TokenObtainPairSerializer,
        responses={ 200: TokenObtainPairSerializer },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


