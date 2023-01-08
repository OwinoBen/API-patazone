from django.urls import path

from socialAuth import views

app_name = 'socialAuth'

urlpatterns = [
    path('google-auth', views.GoogleAuthView.as_view(), name="google-auth")
]
