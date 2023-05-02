from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apiV1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="main"),
    path('api/', include('apiV1.urls')),
    path('o/', include('oauth2_provider.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handling error 404 and 500 (the error view is configured under utils folder)
handler404 = 'utils.views.error_404'
handler500 = 'utils.views.error_500'
