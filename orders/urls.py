from django.urls import path, include
from orders import views
from rest_framework import routers

app_name = 'orders'

router = routers.DefaultRouter(trailing_slash=False)
router.register('order', views.OrderView)

urlpatterns = [
    path('', include(router.urls)),
    path('messages/<phone>', views.is_phone_number_valid, name="messages"),
]
