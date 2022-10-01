from django.urls import path
from categories import views

app_name = 'categories'


urlpatterns = [
    path('product/categories', views.getCategories, name="categories"),
    path('subcategories', views.getSubcategories, name="subcategories"),
    path('subcategory/<categoryid>', views.getSingleSubcategory, name="subcategory"),
    path('sub-subcategory', views.getSubsubCategory, name="sub-subcategory"),
    path('sub-subcategories/<categoryid>', views.getSingleSubsubcategory, name="sub-subcategories"),
]