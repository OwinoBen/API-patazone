# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Apiv1Account(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    email = models.CharField(unique=True, max_length=60)
    username = models.CharField(unique=True, max_length=30)
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField()
    is_admin = models.IntegerField()
    is_active = models.IntegerField()
    is_staff = models.IntegerField()
    is_superuser = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'apiV1_account'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(Apiv1Account, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class CiSessions(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    ip_address = models.CharField(max_length=45)
    timestamp = models.PositiveIntegerField()
    data = models.TextField()

    class Meta:
        managed = False
        db_table = 'ci_sessions'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Apiv1Account, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class PtzAccountUsers(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
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


class PtzActivities(models.Model):
    activity_title = models.CharField(max_length=255)
    color = models.CharField(max_length=100, blank=True, null=True)
    type_activity = models.CharField(max_length=255)
    activity_color = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    activity_icon = models.CharField(max_length=100, blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_activities'


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


class PtzAddresses(models.Model):
    user_id = models.IntegerField()
    county = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.CharField(max_length=255)
    address_type = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_addresses'


class PtzAddrezz(models.Model):
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
        db_table = 'ptz_addrezz'


class PtzBrands(models.Model):
    brand_title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    brand_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_brands'


class PtzBunners(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    image = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_bunners'


class PtzCart(models.Model):
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    order_id = models.CharField(max_length=255)
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
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_cart'


class PtzCategories(models.Model):
    category_name = models.CharField(max_length=255)
    category_icon = models.CharField(max_length=255, blank=True, null=True)
    category_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_categories'


class PtzColor(models.Model):
    product_id = models.IntegerField()
    color_id = models.IntegerField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_color'


class PtzCounties(models.Model):
    county_name = models.CharField(max_length=255)
    county_code = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_counties'


class PtzCoupons(models.Model):
    couponcode = models.CharField(max_length=100)
    valid_per_user = models.IntegerField(blank=True, null=True)
    valid_for_user = models.IntegerField(blank=True, null=True)
    last_date = models.CharField(max_length=255, blank=True, null=True)
    flat_discount = models.IntegerField(blank=True, null=True)
    status = models.IntegerField()
    coupontype = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_coupons'


class PtzCustomers(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    county = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    shipping_fee = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    last_login = models.CharField(max_length=255)
    is_verified = models.CharField(max_length=30)
    is_correct = models.CharField(max_length=100, blank=True, null=True)
    verification_key = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_customers'


class PtzFavicon(models.Model):
    favicon_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_favicon'


class PtzMaterials(models.Model):
    product_id = models.IntegerField()
    material_id = models.IntegerField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_materials'


class PtzMpesa(models.Model):
    resultdesc = models.CharField(db_column='resultDesc', max_length=250)  # Field name made lowercase.
    resultcode = models.IntegerField(db_column='resultCode')  # Field name made lowercase.
    merchantrequestid = models.CharField(db_column='merchantRequestID', max_length=200)  # Field name made lowercase.
    checkoutrequestid = models.CharField(db_column='checkoutRequestID', max_length=200)  # Field name made lowercase.
    amount = models.CharField(max_length=50)
    mpesareceiptnumber = models.CharField(db_column='mpesaReceiptNumber', max_length=200)  # Field name made lowercase.
    transactiondate = models.CharField(db_column='transactionDate', max_length=100)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=50)  # Field name made lowercase.
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_mpesa'


class PtzMultipleimgs(models.Model):
    product_id = models.IntegerField()
    img_url = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_multipleimgs'


class PtzNewsletters(models.Model):
    customer_email = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_newsletters'


class PtzOrderItems(models.Model):
    product_id = models.IntegerField()
    order_id = models.IntegerField()
    product_name = models.CharField(max_length=255)
    product_price = models.CharField(max_length=255)
    product_qty = models.IntegerField()
    product_image = models.CharField(max_length=255)
    product_color = models.CharField(max_length=255)
    product_material = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_order_items'


class PtzOrderitems(models.Model):
    order_id = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_price = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_material = models.CharField(max_length=255)
    product_color = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_orderitems'


class PtzOrders(models.Model):
    order_id = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    payment_id = models.CharField(max_length=255, blank=True, null=True)
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
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_orders'


class PtzOthersliders(models.Model):
    slider_image = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_othersliders'


class PtzPatazonlogo(models.Model):
    logo_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_patazonlogo'


class PtzProductcolor(models.Model):
    color_name = models.CharField(max_length=255)
    color_code = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_productcolor'


class PtzProductmaterial(models.Model):
    material_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_productmaterial'


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
        managed = False
        db_table = 'ptz_products'


class PtzRegions(models.Model):
    county_code = models.IntegerField()
    region_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_regions'


class PtzReviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    user_rating = models.IntegerField()
    user_review = models.TextField()
    datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_reviews'


class PtzSlidersettings(models.Model):
    top_title = models.CharField(max_length=255, blank=True, null=True)
    slider_title = models.CharField(max_length=255, blank=True, null=True)
    amount = models.CharField(max_length=255, blank=True, null=True)
    percentage = models.CharField(max_length=255, blank=True, null=True)
    slider_image = models.CharField(max_length=255)
    is_active = models.IntegerField()
    animation = models.CharField(max_length=100)
    main_slider = models.IntegerField(blank=True, null=True)
    customer_slider = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_slidersettings'


class PtzStreets(models.Model):
    county_id = models.IntegerField()
    region_id = models.IntegerField()
    street_name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_streets'


class PtzSubcategories(models.Model):
    category_id = models.IntegerField()
    subcategory_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_subcategories'


class PtzSubsubcategories(models.Model):
    category_id = models.IntegerField()
    subcategory_id = models.IntegerField()
    sub_subcategory_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_subsubcategories'


class PtzWishlist(models.Model):
    customer_id = models.IntegerField()
    product_id = models.IntegerField()
    product_title = models.CharField(max_length=255)
    product_price = models.CharField(max_length=255)
    product_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_wishlist'
