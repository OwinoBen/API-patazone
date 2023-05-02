import datetime
import math
import random

from django.db import models
import uuid
from django.conf import settings
from django.db.models import Sum, Avg, Count
from django.urls import reverse
from django.utils import timezone

from address.models import Address
from auth_apps.models import Account
from products.models import PtzProducts, Product


# Create your models here.

class OrderManagementQuerySet(models.QuerySet):
    def recentOrders(self):
        return self.order_by('-updated_at', '-created_at')

    def getSells_breakdown(self):
        recent = self.recentOrders().not_refunded()
        recent_orders = recent.recentOrders()
        recent_cart_data = recent.getCartData()
        shipped = recent.not_refunded().getOrderByStatus(status='shipped')
        shipped_orders = shipped.orderTotal()
        paid = recent.getOrderByStatus(status='paid')
        paid_orders = paid.orderTotal()

        data = {
            'recent': recent,
            'recent_orders': recent_orders,
            'recent_cart_data': recent_cart_data,
            'shipped': shipped,
            'shipped_orders': shipped_orders,
            'paid': paid,
            'paid_orders': paid_orders
        }

        return data

    def not_refunded(self):
        return self.exclude(status='refunded')

    def getOrdersByWeeksRange(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7
        days_ago_end = days_ago_start - (number_of_weeks * 7)
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end)
        return self.getOrderByRange(start_date, end_date=end_date)

    def getOrderByRange(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated_at__gte=start_date)
        return self.filter(updated_at__gte=start_date).filter(updated_at__lte=end_date)

    def getOrderByDate(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated_at__day__gte=now.day)

    def orderTotal(self):
        return self.aggregate(Sum("total_amount"), Avg("total_amount"))

    def getCartData(self):
        return self.aggregate(
            Sum("items__product__discount_price"),
            Avg("items__product__discount_price"),
            Count("items__product")
        )

    def getOrderByStatus(self, status='shipped'):
        return self.filter(status=status)

    def getNotCreatedOrders(self):
        return self.exclude(status='created')


class OrderManager(models.Manager):
    def new(self, user=None):
        user_object = None
        if user is not None:
            if user.is_authenticated:
                user_object = user
        return self.model.objects.create(user=user_object)

    def get_queryset(self):
        return OrderManagementQuerySet(self.model, using=self._db)

    def getSells_breakdown(self):
        return self.get_queryset().getSells_breakdown()

    def getOrderByRange(self, start_date, end_date=None):
        return self.get_queryset().getOrderByRange(start_date, end_date)

    def getOrdersByWeeksRange(self, weeks_ago, number_of_weeks):
        return self.get_queryset().getOrdersByWeeksRange(weeks_ago=weeks_ago, number_of_weeks=number_of_weeks)


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    order_id = models.CharField(max_length=125, unique=True, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    payment = models.CharField(max_length=255, blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    amount_paid = models.FloatField(default=0.00, blank=True, null=True)
    total_amount = models.FloatField(default=0.00)
    # cart = models.ManyToManyField(OrderItems)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='shipping_address', null=True,
                                         blank=True)
    status = models.CharField(max_length=120, default='ordered')
    ordered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    shipping_total = models.FloatField(default=100.00)
    active = models.BooleanField(default=True)
    payment_mode = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    soft_delete = models.BooleanField(default=False)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    # @property
    # def items(self):
    #     return self.items.set.all()

    def save(self, *args, **kwargs):
        orderId = 'PTZORD' + str(random.randint(1, 1000000))
        self.order_id = orderId
        super().save(*args, **kwargs)

    def subTotal(self):
        subtotal = 0
        for ordersItem in self.items.all():
            subtotal += ordersItem.getTotalItemPrice()
        return subtotal

    def getTotal(self):
        total = 0
        for item in self.items.all():
            total += item.getFinalOrderAmount()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def getAbsoluteUrl(self):
        return reverse("order:detail", kwargs={'order_id': self.order_id})

    def getStatus(self) -> str:
        if self.status == 'refunded':
            return 'Refunded order'
        elif self.status == 'shipped':
            return "Shipped"
        return 'Shipping soon'

    def update_total(self):
        cart_total = self.getTotal()
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total, shipping_total])
        formatted_total = format(new_total, '.2f')
        self.total_amount = formatted_total
        self.save()
        return new_total

    def update_purchased_product(self):
        for item in self.items.all():
            bj, created = PurchesedProducts.objects.get_or_create(
                order=self.order_id,
                product=item
            )
            return PurchesedProducts.objects.filter(order=self.order_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            self.status = 'paid'
            self.save()
            self.update_purchased_product()
        return self.status


class OrderItems(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="items")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer',
                                 blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_title}"

    def save(self, *args, **kwargs):
        self.order.total_amount = self.getFinalOrderAmount()
        super().save(*args, **kwargs)

    def getTotalItemPrice(self) -> float:
        return self.quantity * self.product.selling_price

    def getTotalDiscountPrice(self) -> float:
        return self.quantity * self.product.discount_price

    def getOrderAmountSaved(self):
        return self.getTotalItemPrice() - self.getTotalDiscountPrice()

    def getFinalOrderAmount(self):
        if self.product.discount_price:
            return self.getTotalDiscountPrice()
        return self.getTotalItemPrice()


class PurchasedProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)


class PurchasedProductManager(models.Manager):
    def get_queryset(self):
        return PurchasedProductQuerySet(self.model, using=self._db)

    def getAll(self):
        return self.get_queryset().active()


class PurchesedProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    refunded = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    object = PurchasedProductManager

    def __str__(self):
        return self.product.product_title


class Refund(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='order_refund')
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='refund_user')
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True)

    def __str__(self):
        return f"{self.user.firstname} {self.user.lastname}"


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
    order = models.ForeignKey(PtzOrders, on_delete=models.CASCADE)
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
