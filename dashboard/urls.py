from django.urls import path, include

from .views import DashboardView


urlpatterns = [
    path('/view', DashboardView.as_view(), name="view")
]