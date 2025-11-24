from django.urls import path
from api.v1.auth.views.custom_token_obtain_pair_view import CustomTokenObtainPairView
from api.v1.auth.views.custom_token_refresh_view import CustomTokenRefreshView

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]