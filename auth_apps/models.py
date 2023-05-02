from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from api import settings

AUTH_PROVIDERS = {
    'email': 'email', 'google': 'google', 'twitter': 'twitter', 'facebook': 'facebook'
}


class apiAccount(BaseUserManager):
    def create_user(self, email, password, firstname, lastname, phone, auth_provider=AUTH_PROVIDERS.get('email')):
        if not email or not self.normalize_email(email):
            raise ValueError('Users must have a valid email address')
        if not firstname:
            raise ValueError('Firstname is required')
        if not lastname:
            raise ValueError('Lastname is required')
        if not phone:
            raise ValueError('Phone number is required')
        if not auth_provider:
            raise ValueError('Auth provider is required')
        user = self.model(
            email=self.normalize_email(email),
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            auth_provider=auth_provider
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password, firstname, lastname):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            phone=phone,
            firstname=firstname,
            lastname=lastname,
        )
        user.auth_provider = AUTH_PROVIDERS.get('email')
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_vendor = False
        user.save()
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = None
    firstname = models.CharField(max_length=30, null=True, blank=True)
    lastname = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=255, blank=True, null=True, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'firstname', 'lastname']

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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
