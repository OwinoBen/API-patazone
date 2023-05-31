"""
Define all product routes
"""
from django.urls import path, include
from rest_framework import routers
from products import views
from .views import ProductsViewSet

APPNAME = 'products'

router = routers.DefaultRouter(trailing_slash=False)

router.register('product', ProductsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('list', views.ApiProductsView.as_view(), name="list"),
]
