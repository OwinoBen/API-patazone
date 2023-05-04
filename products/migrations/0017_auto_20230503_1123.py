# Generated by Django 3.2.3 on 2023-05-03 11:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20230503_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brands',
            name='brand_id',
            field=models.UUIDField(default=uuid.UUID('9068d29c-e9e5-40e6-b750-af66355b678a'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.UUIDField(default=uuid.UUID('dea8bf12-63eb-416b-a1da-52966d9e29a5'), primary_key=True, serialize=False, unique=True),
        ),
    ]
