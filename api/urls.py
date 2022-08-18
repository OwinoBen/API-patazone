from django.contrib import admin
from django.urls import path, include

from apiV1 import views
# from rest_framework.authtoken.views import obtain_auth_token,

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="main"),
    path('api/', include('apiV1.urls')),
    path('o/', include('oauth2_provider.urls')),
    path('oauthlogin', views.user_login),
    path('registeruser', views.TokenView.as_view()),
    path('reg', views.RefreshToken.as_view()),

]
