from django.urls import path, include

from apiV1 import views

app_name = 'apiV1'

urlpatterns = [

    path('/', views.getAccountUsers, name="users"),
    path('auths/', include('auth_apps.urls')),
    path('maps/', include('googleMaps.urls')),
    path('v1/', include('products.urls')),
    path('v1/orders/', include('orders.urls')),
    path('v1/categories/', include('categories.urls')),
    path('customer/address/add', views.saveCustomerAddress, name="add-address"),
    path('customer/address/list', views.getAddressList, name="address-list")
]
