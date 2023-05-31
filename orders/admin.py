from django.contrib import admin

# Register your models here.
from orders.models import Orders

admin.site.register(Orders)
