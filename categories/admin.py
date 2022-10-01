from django.contrib import admin

# Register your models here.
from apiV1.models import PtzCategories, PtzSubcategories, PtzSubsubcategories

# admin.site.register(PtzCategories)
admin.site.register(PtzSubcategories)
admin.site.register(PtzSubsubcategories)