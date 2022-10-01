from django.urls import path

from  googleMaps import views
app_name = 'googleMaps'

urlpatterns = [
    path('config/geo-api/<lat>/<lng>', views.geocode_api, name="geo-api"),
    path('config/place-api-autocomplete/<search>', views.get_google_auto_complete_search, name="google-search-autocomplete"),
    path('config/place-api-details/<placeID>', views.get_google_place_details, name="google-places-details")
]