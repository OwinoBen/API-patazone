from django.db import models
from django_prometheus.models import ExportModelOperationsMixin
from products.models import imagePath


# Create your models here.

class SystemSetting(ExportModelOperationsMixin('systemsetting'), models.Model):
    name = models.CharField(null=False, max_length=200)
    email = models.EmailField(null=True)
    phone = models.CharField(null=True, max_length=100)
    address = models.TextField(null=True, max_length=500)
    logo = models.ImageField(upload_to=imagePath, null=True)
    copyrightTxt = models.TextField(null=True, max_length=500)

    def delete(self, *args, **kwargs):
        self.logo.delete(save=False)
        super(SystemSetting, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            this = SystemSetting.objects.get(id=self.id)
            if this.logo != self.logo:
                this.logo.delete()
        except:
            pass
        super(SystemSetting, self).save(*args, **kwargs)
