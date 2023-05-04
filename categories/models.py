from django.db import models
import uuid


# Create your models here.
class Categories(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4())
    category_name = models.CharField(max_length=30)
    category_image = models.ImageField(upload_to="categories", default="", null=True, blank=True)
    category_thumbnail = models.ImageField(upload_to="categories", default="", null=True, blank=True)
    is_topcategory = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    soft_delete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Subcategories(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4())
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categories")
    subcategory_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)


class SubsubCategories(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4())
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categoryID")
    subcategory = models.ForeignKey(Subcategories, on_delete=models.CASCADE, related_name="subcategoryID")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="categories", default="", blank=True, null=True)
    is_major = models.BooleanField(default=False)
    ftype = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.id)
