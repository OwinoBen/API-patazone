from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


from rest_framework.authtoken.models import Token


class PtzCustomers(AbstractBaseUser):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    county = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    shipping_fee = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.CharField(max_length=255)
    is_verified = models.CharField(max_length=30)
    verification_key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_customers'

class PtzAddress(models.Model):
    user_id = models.BigIntegerField()
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    county = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.IntegerField(db_column='is-default')  # Field renamed to remove unsuitable characters.
    address_type = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'ptz_address'
        ordering = ['-id']

    def __str__(self):
        return self.firstname


class PtzCategories(models.Model):
    category_name = models.CharField(max_length=30)
    category_image = models.CharField(max_length=100)
    category_thumbnail = models.CharField(max_length=100)
    is_topcategory = models.IntegerField()
    date_created = models.DateTimeField()
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_categories'

    def __str__(self):
        return self.category_name


class PtzSubcategories(models.Model):
    category_id = models.IntegerField()
    subcategory_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_subcategories'

    def __str__(self):
        return self.subcategory_name


class PtzSubsubcategories(models.Model):
    category_id = models.IntegerField()
    subcategory = models.ForeignKey(PtzSubcategories, models.DO_NOTHING)
    sub_subcategory_name = models.CharField(max_length=255)
    subsub_category_image = models.CharField(max_length=255, blank=True, null=True)
    is_major = models.IntegerField(blank=True, null=True)
    ftype = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_subsubcategories'
        ordering = ['-id']

    def __str__(self):
        return self.sub_subcategory_name

