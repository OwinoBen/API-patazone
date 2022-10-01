from django.db import models

from products.models import PtzProducts


# Create your models here.
class tbl_orders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=255)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    payment_id = models.CharField(max_length=255)
    coupon_id = models.IntegerField(blank=True, null=True)
    amount_paid = models.CharField(max_length=255, blank=True, null=True)
    shipping_fee = models.CharField(max_length=255, blank=True, null=True)
    discount = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.IntegerField(default=0, max_length=10)
    order_notes = models.TextField(blank=True, null=True)
    payment_mode = models.CharField(max_length=255, blank=True, null=True)
    order_status = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_created=True)
    soft_delete = models.CharField(max_length=50)


class PtzOrders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=255)
    user_id = models.CharField(max_length=255, blank=True, null=True)
    payment_id = models.CharField(max_length=255)
    coupon_id = models.IntegerField(blank=True, null=True)
    amount_paid = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    shipping_fee = models.CharField(max_length=255, blank=True, null=True)
    discount = models.CharField(max_length=255, blank=True, null=True)
    is_paid = models.IntegerField()
    order_notes = models.TextField(blank=True, null=True)
    payment_mode = models.CharField(max_length=255, blank=True, null=True)
    order_status = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    soft_delete = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ptz_orders'

    def __str__(self):
        return self.order_id


class PtzCart(models.Model):
    user_id = models.CharField(max_length=255)
    product = models.ForeignKey(PtzProducts, models.CASCADE)
    order = models.ForeignKey(PtzOrders, models.CASCADE)
    product_name = models.CharField(max_length=255)
    product_qty = models.IntegerField()
    product_price = models.CharField(max_length=255)
    product_size = models.CharField(max_length=255, blank=True, null=True)
    product_color = models.CharField(max_length=255, blank=True, null=True)
    ordered = models.IntegerField()
    discounted_amount = models.CharField(max_length=255, blank=True, null=True)
    discount_price = models.CharField(max_length=255, blank=True, null=True)
    shop_name = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.CharField(max_length=255)
    product_material = models.CharField(max_length=255, blank=True, null=True)
    product_number = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=255)
    product_slug = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    soft_delete = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ptz_cart'

    def __str__(self):
        return self.product_name
