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


class Oauth2ProviderAccesstoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    scope = models.TextField()
    application = models.ForeignKey('Oauth2ProviderApplication', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Apiv1Account, models.DO_NOTHING, blank=True, null=True)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    source_refresh_token = models.OneToOneField('Oauth2ProviderRefreshtoken', models.DO_NOTHING, blank=True, null=True)
    id_token = models.OneToOneField('Oauth2ProviderIdtoken', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_accesstoken'


class Oauth2ProviderApplication(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.CharField(unique=True, max_length=100)
    redirect_uris = models.TextField()
    client_type = models.CharField(max_length=32)
    authorization_grant_type = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(Apiv1Account, models.DO_NOTHING, blank=True, null=True)
    skip_authorization = models.IntegerField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    algorithm = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_application'


class Oauth2ProviderGrant(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.CharField(unique=True, max_length=255)
    expires = models.DateTimeField()
    redirect_uri = models.TextField()
    scope = models.TextField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(Apiv1Account, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    code_challenge = models.CharField(max_length=128)
    code_challenge_method = models.CharField(max_length=10)
    nonce = models.CharField(max_length=255)
    claims = models.TextField()

    class Meta:
        managed = False
        db_table = 'oauth2_provider_grant'


class Oauth2ProviderIdtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    jti = models.CharField(unique=True, max_length=32)
    expires = models.DateTimeField()
    scope = models.TextField()
    created = models.DateTimeField()
    updated = models.DateTimeField()
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(Apiv1Account, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_idtoken'


class Oauth2ProviderRefreshtoken(models.Model):
    id = models.BigAutoField(primary_key=True)
    token = models.CharField(max_length=255)
    access_token = models.OneToOneField(Oauth2ProviderAccesstoken, models.DO_NOTHING, blank=True, null=True)
    application = models.ForeignKey(Oauth2ProviderApplication, models.DO_NOTHING)
    user = models.ForeignKey(Apiv1Account, models.DO_NOTHING)
    created = models.DateTimeField()
    updated = models.DateTimeField()
    revoked = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth2_provider_refreshtoken'
        unique_together = (('token', 'revoked'),)


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
    is_online = models.IntegerField()
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
    user = models.ForeignKey('PtzCustomers', models.DO_NOTHING)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    street = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
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


class PtzAdvert(models.Model):
    image = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255)
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_advert'


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
    user_id = models.CharField(max_length=255)
    product = models.ForeignKey('PtzProducts', models.DO_NOTHING)
    order = models.ForeignKey('PtzOrders', models.DO_NOTHING)
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
    soft_delete = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ptz_cart'


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


class PtzCategorybunners(models.Model):
    category = models.ForeignKey(PtzCategories, models.DO_NOTHING)
    bunner_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_categorybunners'


class PtzColor(models.Model):
    product = models.ForeignKey('PtzProducts', models.DO_NOTHING)
    color_id = models.IntegerField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_color'


class PtzContacts(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=65, blank=True, null=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_contacts'


class PtzCounties(models.Model):
    id = models.IntegerField(blank=True, null=True)
    county_name = models.CharField(max_length=255)
    county_code = models.IntegerField(primary_key=True)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_counties'


class PtzCoupons(models.Model):
    code = models.CharField(max_length=255)
    type_discount = models.IntegerField()
    discount = models.IntegerField()
    no_of_use = models.IntegerField()
    who_can_use = models.CharField(max_length=255)
    active = models.CharField(max_length=255)
    expiry_date = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_coupons'


class PtzCustomeremails(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=100)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=100)  # Field name made lowercase.
    customer_email = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_customeremails'


class PtzCustomers(models.Model):
    auth_id = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    county = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    shipping_fee = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    profile_image = models.TextField()
    date_created = models.DateTimeField()
    last_login = models.CharField(max_length=255)
    is_verified = models.CharField(max_length=30)
    is_correct = models.CharField(max_length=100, blank=True, null=True)
    verification_key = models.CharField(max_length=255)
    google_login = models.IntegerField()
    soft_delete = models.IntegerField()

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


class PtzGuests(models.Model):
    guest_id = models.CharField(max_length=255)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_guests'


class PtzLipalater(models.Model):
    customer_id = models.CharField(max_length=255)
    order_id = models.CharField(primary_key=True, max_length=35)
    payment_id = models.CharField(max_length=35)
    amount_paid = models.IntegerField()
    payment_mode = models.CharField(max_length=30)
    order_status = models.CharField(max_length=20)
    user_type = models.CharField(max_length=65)

    class Meta:
        managed = False
        db_table = 'ptz_lipalater'


class PtzLipalaterCart(models.Model):
    order = models.ForeignKey(PtzLipalater, models.DO_NOTHING)
    item_type = models.CharField(max_length=255)
    item_brand = models.CharField(max_length=80)
    store_key = models.CharField(max_length=30)
    delivery_option = models.CharField(max_length=50)
    preferred_option = models.CharField(max_length=100)
    item_decription = models.CharField(max_length=255)
    facility_plan = models.CharField(max_length=255)
    item_code = models.CharField(max_length=60)
    item_value = models.IntegerField()
    item_quantity = models.IntegerField()
    item_topup = models.CharField(max_length=255)
    topup_ref = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_lipalater_cart'


class PtzLipalaterOrderedProducts(models.Model):
    order = models.ForeignKey(PtzLipalater, models.DO_NOTHING)
    loan_product_id = models.CharField(max_length=100)
    loan_application_detail_id = models.CharField(max_length=100)
    item_decription = models.CharField(max_length=100, blank=True, null=True)
    item_code = models.CharField(max_length=100)
    item_value = models.IntegerField()
    purchase_id = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    item_brand = models.CharField(max_length=100)
    delivery_option = models.CharField(max_length=100)
    preferred_option = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    store_name = models.CharField(max_length=100)
    facility_status = models.CharField(max_length=100)
    facility_plan = models.IntegerField()
    partner_store_id = models.CharField(max_length=100)
    upfront_fees = models.IntegerField()
    loan_duration = models.IntegerField()
    markup = models.IntegerField()
    item_topup = models.IntegerField()
    topup_ref = models.CharField(max_length=100, blank=True, null=True)
    invoice_amount = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.CharField(max_length=100)
    last_modified_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_lipalater_ordered_products'


class PtzLipalatercustomers(models.Model):
    customer_id = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    amount = models.IntegerField()
    date_created = models.DateTimeField()
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_lipalatercustomers'


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


class PtzMaterials(models.Model):
    product_id = models.IntegerField()
    material_id = models.IntegerField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_materials'


class PtzMobileLogo(models.Model):
    logo_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_mobile_logo'


class PtzMpesa(models.Model):
    resultdesc = models.CharField(db_column='resultDesc', max_length=250)  # Field name made lowercase.
    resultcode = models.IntegerField(db_column='resultCode')  # Field name made lowercase.
    merchantrequestid = models.CharField(db_column='merchantRequestID', max_length=200)  # Field name made lowercase.
    checkoutrequestid = models.CharField(db_column='checkoutRequestID', max_length=200)  # Field name made lowercase.
    amount = models.CharField(max_length=50)
    mpesareceiptnumber = models.CharField(db_column='mpesaReceiptNumber', primary_key=True, max_length=255)  # Field name made lowercase.
    transactiondate = models.CharField(db_column='transactionDate', max_length=100)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='phoneNumber', max_length=50)  # Field name made lowercase.
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_mpesa'


class PtzMultipleimgs(models.Model):
    product = models.ForeignKey('PtzProducts', models.DO_NOTHING)
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


class PtzNotifications(models.Model):
    vendor_id = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    sound_status = models.IntegerField()
    view_status = models.CharField(max_length=50)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_notifications'


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
    date_created = models.DateTimeField()
    soft_delete = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ptz_orders'


class PtzOrderzz(models.Model):
    order_id = models.CharField(max_length=100, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    payment_id = models.IntegerField(blank=True, null=True)
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
    date_updated = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_orderzz'


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


class PtzProductPercentage(models.Model):
    company_name = models.CharField(max_length=255)
    percentage = models.IntegerField()
    end_date = models.DateTimeField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_product_percentage'


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
    vendor_id = models.CharField(max_length=255)
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
    cost_price = models.FloatField(blank=True, null=True)
    selling_price = models.CharField(max_length=255)
    discount_price = models.CharField(max_length=255, blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    product_size = models.CharField(max_length=255, blank=True, null=True)
    product_color = models.CharField(max_length=255, blank=True, null=True)
    product_material = models.CharField(max_length=255, blank=True, null=True)
    end_date = models.CharField(max_length=255, blank=True, null=True)
    product_thumbnail = models.CharField(max_length=255)
    unit_size = models.TextField()
    flash_sale = models.CharField(max_length=255, blank=True, null=True)
    best_sale = models.CharField(max_length=255, blank=True, null=True)
    hot_deals = models.IntegerField(blank=True, null=True)
    featured = models.IntegerField(blank=True, null=True)
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
    is_lipalater = models.IntegerField(blank=True, null=True)
    is_sevi = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()
    updated_date = models.CharField(max_length=255, blank=True, null=True)
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_products'


class PtzProductstatistics(models.Model):
    product = models.ForeignKey(PtzProducts, models.DO_NOTHING)
    user = models.ForeignKey(PtzCustomers, models.DO_NOTHING, blank=True, null=True)
    clicks = models.IntegerField()
    date_created = models.DateTimeField()
    date_updated = models.DateTimeField()
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_productstatistics'


class PtzRegions(models.Model):
    county_code = models.ForeignKey(PtzCounties, models.DO_NOTHING, db_column='county_code')
    region_name = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_regions'


class PtzReviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(PtzCustomers, models.DO_NOTHING)
    product = models.ForeignKey(PtzProducts, models.DO_NOTHING)
    user_rating = models.IntegerField()
    user_review = models.TextField()
    datetime = models.DateTimeField()
    is_approved = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'ptz_reviews'


class PtzSlidersettings(models.Model):
    category = models.ForeignKey(PtzCategories, models.DO_NOTHING)
    slider_image = models.CharField(max_length=255)
    is_active = models.IntegerField()
    main_slider = models.IntegerField(blank=True, null=True)
    customer_slider = models.IntegerField(blank=True, null=True)
    smartphones = models.IntegerField(blank=True, null=True)
    electronics = models.IntegerField(blank=True, null=True)
    tablets = models.IntegerField(blank=True, null=True)
    laptops = models.IntegerField(blank=True, null=True)
    groceries = models.IntegerField(blank=True, null=True)
    fushion = models.IntegerField(blank=True, null=True)
    cosmetics = models.IntegerField(blank=True, null=True)
    others = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.IntegerField()
    soft_delete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ptz_slidersettings'


class PtzStatisticsnoti(models.Model):
    user = models.ForeignKey(PtzCustomers, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_statisticsnoti'


class PtzStore(models.Model):
    store_id = models.CharField(primary_key=True, max_length=255)
    vendor = models.ForeignKey('PtzVendor', models.DO_NOTHING)
    store_name = models.CharField(unique=True, max_length=255)
    kra_pin = models.CharField(max_length=65)
    business_type = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_store'


class PtzStreets(models.Model):
    county = models.ForeignKey(PtzCounties, models.DO_NOTHING)
    region = models.ForeignKey(PtzRegions, models.DO_NOTHING)
    street_name = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_streets'


class PtzSubcategories(models.Model):
    category = models.ForeignKey(PtzCategories, models.DO_NOTHING)
    subcategory_name = models.CharField(max_length=255)
    subcategory_image = models.CharField(max_length=255, blank=True, null=True)
    is_major = models.IntegerField(blank=True, null=True)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ptz_subcategories'


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


class PtzVendor(models.Model):
    vendor_id = models.CharField(primary_key=True, max_length=255)
    national_id = models.CharField(db_column='national_ID', max_length=255)  # Field name made lowercase.
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=65)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    id_image = models.CharField(max_length=255)
    profile_image = models.CharField(max_length=255)
    gender = models.CharField(max_length=7)
    is_active = models.IntegerField()
    is_email_verified = models.IntegerField()
    is_online = models.IntegerField()
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_vendor'


class PtzWhiteLogo(models.Model):
    logo_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()
    date_updated = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'ptz_white_logo'


class PtzWishlist(models.Model):
    customer = models.ForeignKey(PtzCustomers, models.DO_NOTHING)
    product = models.ForeignKey(PtzProducts, models.DO_NOTHING)
    product_title = models.CharField(max_length=255)
    selling_price = models.CharField(max_length=255)
    discount_price = models.CharField(max_length=255, blank=True, null=True)
    product_number = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    product_image = models.CharField(max_length=255)
    date_created = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ptz_wishlist'
