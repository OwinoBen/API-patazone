from django.urls import path
from orders import views

app_name = 'orders'
urlpatterns = [
    path('placeorder', views.placeOrder, name="place-order"),
    path('messages/<phone>', views.is_phone_number_valid, name="messages"),
    path('customer-orders', views.getUserOrders, name="customer-orders")
]
