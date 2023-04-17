from django.contrib import admin

# Register your models here.
from orders.models import PtzOrders, PtzCart, Orders

admin.site.register(PtzOrders)
admin.site.register(PtzCart)
admin.site.register(Orders)