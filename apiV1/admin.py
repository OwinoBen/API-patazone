from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from auth_apps.models import PtzAccountUsers, Account
from .models import PtzCustomers, PtzAddress, Categories, Subcategories, SubsubCategories


class AccountUsers(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'date_registered')
    search_fields = ('email', 'phone')
    readonly_fields = ('date_registered', 'is_email_varified')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class AccountCustomers(UserAdmin):
    list_display = ('email', 'firstname', 'lastname', 'phone', 'date_created')
    search_fields = ('email', 'phone')
    readonly_fields = ('date_created', 'is_verified')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class Accounts(UserAdmin):
    list_display = ('email', 'phone','date_joined', 'auth_provider')
    search_fields = ('email', 'phone')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


class CategoriesView(UserAdmin):
    list_display = ('id', 'category_name', 'date_created')
    search_fields = ('category_name',)
    readonly_fields = ('date_created', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ()


admin.site.register(PtzCustomers, AccountCustomers)
admin.site.register(PtzAccountUsers, AccountUsers)
admin.site.register(Account, Accounts)
admin.site.register(PtzAddress)
admin.site.register(Categories)
admin.site.register(Subcategories)
admin.site.register(SubsubCategories)