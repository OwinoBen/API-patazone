from django.urls import path, include

app_name = 'base'

urlpatterns = [

    path('auths/', include('auth_apps.urls', namespace="auth_apps")),
    path('maps/', include('googleMaps.urls', namespace='')),
    path('v1/', include('products.urls', namespace='')),
    path('v1/orders/', include('orders.urls', namespace='')),
    path('v1/categories/', include('categories.urls', namespace='')),
    path('dashboard', include('dashboard.urls', namespace=''))
]
