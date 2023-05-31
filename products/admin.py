from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from products.models import Product, Brands, \
    ProductImages


class CategoriesView(UserAdmin):
    list_display = ('id', 'category_name', 'date_created')
    search_fields = ('category_name',)
    readonly_fields = ('date_created',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


admin.site.register(Product)
admin.site.register(Brands)
admin.site.register(ProductImages)
