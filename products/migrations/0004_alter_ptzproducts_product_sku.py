# Generated by Django 3.2.3 on 2023-01-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_ptzproducts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ptzproducts',
            name='product_sku',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
