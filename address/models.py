import uuid
from django.db import models
from auth_apps.models import Account


# Create your models here.
class Address(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    county = models.CharField(max_length=120, null=True, blank=True)
    region = models.CharField(max_length=120, null=True, blank=True)
    street = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    latitude = models.CharField(max_length=120, null=True, blank=True)
    longitude = models.CharField(max_length=120, null=True, blank=True)
    address_type = models.CharField(default='shipping', max_length=120, null=True, blank=True)
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.firstname
