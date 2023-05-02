from django.urls import path, include
from orders import views
from rest_framework import routers

app_name = 'orders'

router = routers.DefaultRouter(trailing_slash=False)
router.register('order', views.OrderView)

urlpatterns = [
    path('', include(router.urls)),
    path('placeorder', views.placeOrder, name="place-order"),
    path('messages/<phone>', views.is_phone_number_valid, name="messages"),
    path('customer-orders', views.getUserOrders, name="customer-orders"),
    path('orderItems/<orderid>', views.getOrderItems, name="order-items"),
    path('list', views.getOrders, name="orders-list")
]
