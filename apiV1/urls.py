from django.urls import path

from apiV1 import views

app_name = 'apiV1'

urlpatterns = [

    path('/', views.getAccountUsers, name="users"),
    path('products', views.viewProducts, name="products"),
    path('update', views.updateProducts, name="update"),
    path('delete', views.deleteProducts, name="delete"),
    path('createuser', views.registration_view, name="createuser"),
    path('login', views.ObatainAuthTokenView.as_view(), name="login"),
    path('list', views.ApiProductsView.as_view(), name="list"),
    path('update-account', views.update_account_view, name="update-account"),
    path('list-users', views.account_property_view, name="list-users"),
    path('categories', views.getCategories, name="categories"),
    path('subcategories', views.getSubcategories, name="subcategories"),
    path('subcategory/<categoryid>', views.getSingleSubcategoty, name="subcategory"),
    path('sub-subcategory', views.getSubsubCategory, name="sub-subcategory"),
    path('sub-subcategories/<subcategoryid>', views.getSingleSubsubcategory, name="sub-subcategories"),
    path('category-products/<category_id>', views.getProductsByCategoryID.as_view(), name="category-products"),
    path('subcategory-products/<subcateId>', views.getSubCategoryProducts.as_view(), name="subcategory-products"),
    path('<slug>', views.getSingleProductDetails, name="productdetail"),
    path('offerproducts', views.getOfferProducts.as_view(), name="offerproducts"),
    path('productgallery/<product_id>', views.getProductGallery, name="productgallery"),
    path('flashproducts', views.getFlashProducts.as_view(), name="flashproducts")
]
