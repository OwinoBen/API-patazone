from django.db import models
import uuid
import os
import random
# Create your models here.
from django.utils.text import slugify

from categories.models import Categories, SubsubCategories, Subcategories


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def imagePath(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = f'{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return f"productImages/{new_filename}/{final_filename}".format(
        new_filename=new_filename,
        final_filename=final_filename
    )


class Brands(models.Model):
    brand_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4())
    category_id = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    brand_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    brand_image = models.ImageField(upload_to="brands")
    is_major = models.BooleanField(default=False, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.brand_id)


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4())
    product_title = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category")
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, related_name="subcategory")
    subsubcategory = models.ForeignKey(SubsubCategories, on_delete=models.CASCADE, related_name="subsubcategory")
    meta_title = models.CharField(max_length=255, )
    meta_keywords = models.CharField(max_length=255, default='')
    meta_description = models.CharField(max_length=255, default='')
    product_sku = models.CharField(max_length=100, blank=True)
    product_qty = models.IntegerField(default=0)
    selling_price = models.FloatField(max_length=10)
    discount_price = models.FloatField(max_length=255, default=0.0, blank=True, null=True)
    variation = models.JSONField(blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    product_thumbnail = models.ImageField(upload_to=imagePath)
    hot_deals = models.BooleanField(default=False, blank=True, null=True)
    featured = models.BooleanField(default=False, blank=True, null=True)
    recommended = models.BooleanField(default=False, blank=True, null=True)
    new = models.BooleanField(default=False)
    returnable = models.BooleanField(default=True)
    replaceable = models.BooleanField(default=True)
    short_description = models.TextField()
    product_specification = models.TextField(blank=True, null=True)
    long_description = models.TextField()
    is_verified = models.BooleanField(default=False)
    live = models.CharField(default="Draft", max_length=10, )
    same_day_deliver = models.BooleanField(default=False)
    next_day_delivery = models.BooleanField(default=False)
    hyper_local_delivery = models.BooleanField(default=False)
    min_order_count = models.IntegerField(default=1)
    max_order_count = models.IntegerField(default=1)
    return_days = models.IntegerField(default=0)
    out_of_stock_sell = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        sku = 'SKU' + str(random.randint(1, 1000000))
        self.slug = slugify(self.product_title)
        self.product_sku = sku
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % self.product_title


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    img = models.ImageField(upload_to=imagePath, default="", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.product_id)
