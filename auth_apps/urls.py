from django.urls import path, include
from auth_apps import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'auth_apps'

urlpatterns = [
    path('createuser', views.registration_view, name="createuser"),
    path('login', views.login_user, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('update-account', views.update_account_view, name="update-account"),
    path('list-users', views.account_property_view, name="list-users"),
    path('account/delete-user', views.CloseUserAccount, name="close-account"),
    path('social-auth/', include('socialAuth.urls')),

    path('social', views.UserRegistrationView.as_view(), name='register'),
    path('signin', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
