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
    path('category-products/<category_id>', views.getProductsByCategoryID.as_view(),
         name="category-products"),
    path('subcategory-products/<subcateId>', views.getSubCategoryProducts.as_view(),
         name="subcategory-products"),
    path('sub-subcategory-products/<subsubcateId>', views.getSub_subCategoryProducts.as_view(),
         name="subsubcategory-products"),
    path('product/details/product-details/<slug>', views.getSingleProductDetails,
         name="productdetail"),
    path('products/offers/offerproducts', views.getOfferProducts.as_view(),
         name="offerproducts"),
    path('productgallery/<product_id>', views.getProductGallery,
         name="productgallery"),
    path('products/offer/flashproducts', views.getFlashProducts.as_view(),
         name="flashproducts"),
    path('products/recommended', views.getRecommendedProducts.as_view(),
         name="recommended"),
    path('sliders/mainbanners', views.getBannerSliders, name="mainsliders"),
    path('products/brands', views.getBrands, name="brands"),
    path('products/brands-products/<brand_id>', views.getProductsByBrands,
         name="brands-product"),

]
