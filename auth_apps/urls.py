from django.urls import path, include
from auth_apps import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'auth_apps'

urlpatterns = [
    path('social-auth/', include('socialAuth.urls')),

    path('social', views.UserRegistrationView.as_view(), name='register'),
    path('signin', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
