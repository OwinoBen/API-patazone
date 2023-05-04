from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .models import Categories, Subcategories, SubsubCategories


class CategoriesView(UserAdmin):
    list_display = ('id', 'category_name','category_thumbnail', 'date_created')
    search_fields = ('category_name',)
    readonly_fields = ('date_created', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


admin.site.register(Categories, CategoriesView)
admin.site.register(Subcategories)
admin.site.register(SubsubCategories)
