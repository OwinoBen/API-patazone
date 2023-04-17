# Generated by Django 3.2.3 on 2023-04-16 21:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20230416_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brands',
            name='brand_id',
            field=models.UUIDField(default=uuid.UUID('9f12368e-d19f-4d4c-bb0d-af74191c669f'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.UUIDField(default=uuid.UUID('84a1413e-764d-4f87-a3c3-194e7eec682e'), primary_key=True, serialize=False, unique=True),
        ),
    ]
