# Generated by Django 3.2.3 on 2023-04-16 19:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brands',
            name='brand_id',
            field=models.UUIDField(default=uuid.UUID('b4eab162-1c4f-4a2d-b2f2-790dc3b6ef6b'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_id',
            field=models.UUIDField(default=uuid.UUID('47c49125-2120-40a0-b7d1-a9f3226cd71e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]