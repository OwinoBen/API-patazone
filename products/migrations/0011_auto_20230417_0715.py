# Generated by Django 3.2.3 on 2023-04-17 07:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20230417_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brands',
            name='brand_id',
            field=models.UUIDField(default=uuid.UUID('cdc8c542-b663-4f2c-81ef-95c83aec26bc'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.UUIDField(default=uuid.UUID('0dd39422-f4e7-46e9-9921-0ba5bb316e55'), primary_key=True, serialize=False, unique=True),
        ),
    ]