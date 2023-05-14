from django.urls import path, include

from apiV1 import views

app_name = 'apiV1'

urlpatterns = [

    path('/', views.getAccountUsers, name="users"),
    path('auths/', include('auth_apps.urls', namespace="auth_apps")),
    path('maps/', include('googleMaps.urls', namespace='')),
    path('v1/', include('products.urls', namespace='')),
    path('v1/orders/', include('orders.urls', namespace='')),
    path('v1/categories/', include('categories.urls', namespace='')),
    path('customer/address/add', views.saveCustomerAddress, name="add-address"),
    path('customer/address/list', views.getAddressList, name="address-list"),
    path('dashboard', include('dashboard.urls', namespace=''))
]
