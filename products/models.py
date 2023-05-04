import random

from django.db import models
import uuid
import os
import random
# Create your models here.
from django.utils.text import slugify

from categories.models import Categories, SubsubCategories, Subcategories
from apiV1.models import PtzCategories


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


class PtzMultipleimgs(models.Model):
    product_id = models.IntegerField()
    img_url = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_multipleimgs'

    def __str__(self):
        return self.img_url


class Brands(models.Model):
    brand_id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4())
    category_id = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
    brand_title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    brand_image = models.ImageField(upload_to="brands")
    is_major = models.BooleanField(default=False,blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.brand_id)


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4())
    product_title = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category")
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, related_name="subcategory")
    subsubcategory = models.ForeignKey(SubsubCategories, on_delete=models.CASCADE, related_name="subsubcategory")
    product_tags = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=255, blank=True)
    product_qty = models.IntegerField(default=0)
    selling_price = models.FloatField(max_length=255)
    discount_price = models.FloatField(max_length=255, default=0.0, blank=True, null=True)
    variation = models.JSONField(blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)
    product_thumbnail = models.ImageField(upload_to=imagePath)
    hot_deals = models.BooleanField(default=False, blank=True, null=True)
    featured = models.BooleanField(default=False, blank=True, null=True)
    recommended = models.BooleanField(default=False, blank=True, null=True)
    short_description = models.TextField()
    product_specification = models.TextField(blank=True, null=True)
    long_description = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        insku = random.randint(1, 1000000)
        sku = 'SKUPTZ' + str(insku)
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


class PtzProducts(models.Model):
    product_id = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=255, blank=True, null=True)
    product_title = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True, null=True)
    brand_id = models.IntegerField()
    category_id = models.IntegerField()
    subcategory_id = models.IntegerField()
    sub_subcategory_id = models.IntegerField(blank=True, null=True)
    product_tags = models.CharField(max_length=255)
    # product_gallery = models.ForeignKey(PtzMultipleimgs, null=True, blank=True, on_delete=models.CASCADE)
    product_sku = models.CharField(max_length=255, blank=True)
    product_qty = models.CharField(max_length=255)
    selling_price = models.CharField(max_length=255)
    discount_price = models.CharField(max_length=255, blank=True, null=True)
    product_size = models.CharField(max_length=255)
    product_color = models.CharField(max_length=255, blank=True, null=True)
    product_material = models.CharField(max_length=255, blank=True, null=True)
    end_date = models.CharField(max_length=255, blank=True, null=True)
    product_thumbnail = models.CharField(max_length=255)
    hot_deals = models.CharField(max_length=255, blank=True, null=True)
    featured = models.CharField(max_length=255, blank=True, null=True)
    is_recomended = models.IntegerField(blank=True, null=True)
    special_offer = models.CharField(max_length=255, blank=True, null=True)
    special_deals = models.CharField(max_length=255, blank=True, null=True)
    value_of_the_day = models.IntegerField(blank=True, null=True)
    weekly_offers = models.IntegerField(blank=True, null=True)
    new_arrivals = models.IntegerField(blank=True, null=True)
    short_description = models.TextField()
    product_specification = models.TextField(blank=True, null=True)
    long_description = models.TextField()
    is_varified = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    updated_date = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'ptz_products'
        ordering = ['-id']

    def __str__(self):
        return self.product_title


class PtzMainslidersettings(models.Model):
    category = models.ForeignKey(PtzCategories, models.DO_NOTHING, blank=True, null=True)
    slider_image = models.CharField(max_length=255)
    is_active = models.IntegerField()
    main_slider = models.IntegerField(blank=True, null=True)
    customer_slider = models.IntegerField(blank=True, null=True)
    others = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.IntegerField()
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_mainslidersettings'

    def __str__(self):
        return self.slider_image


class PtzBrands(models.Model):
    category_id = models.IntegerField()
    brand_title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    brand_image = models.CharField(max_length=255)
    is_major = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_brands'

    def __str__(self):
        return self.brand_title
