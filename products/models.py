from django.db import models

# Create your models here.
from apiV1.models import PtzCategories


class PtzMultipleimgs(models.Model):
    product_id = models.IntegerField()
    img_url = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_multipleimgs'

    def __str__(self):
        return self.img_url


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
    product_sku = models.CharField(max_length=255)
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
