from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


# Create your models here.
# from .models import PtzMultipleimgs


class apiAccount(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Username is required')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = apiAccount()

    def __str__(self):
        return self.email

    # for checking permissions to keep. All admins have ALL permissions
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # does this user have permissions to view the app
    def has_module_perms(self, app_label):
        return True


class PtzAccountUsers(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    id_image = models.CharField(max_length=255, blank=True, null=True)
    business_type = models.CharField(max_length=255, blank=True, null=True)
    second_phone = models.CharField(max_length=255, blank=True, null=True)
    shop_address = models.CharField(max_length=255, blank=True, null=True)
    kra_pin = models.CharField(max_length=255, blank=True, null=True)
    store_number = models.CharField(max_length=255, blank=True, null=True)
    store_name = models.CharField(max_length=255, blank=True, null=True)
    national_id = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.IntegerField()
    is_superuser = models.IntegerField()
    is_vendor = models.IntegerField()
    is_active = models.IntegerField()
    vendor_id = models.CharField(max_length=255, blank=True, null=True)
    is_email_varified = models.CharField(max_length=255)
    varification_key = models.CharField(max_length=255, blank=True, null=True)
    user_image = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    date_registered = models.DateTimeField()
    date_updated = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_account_users'


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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
    subcategory_id = models.IntegerField()
    sub_subcategory_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_subsubcategories'
        ordering = ['-id']

    def __str__(self):
        return self.sub_subcategory_name


class PtzAddress(models.Model):
    user_id = models.IntegerField()
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    is_default = models.IntegerField(db_column='is-default')  # Field renamed to remove unsuitable characters.
    address_type = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_address'
        ordering = ['-id']

    def __str__(self):
        return self.firstname


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
        return  self.slider_image

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
