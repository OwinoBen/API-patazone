# Generated by Django 3.2.3 on 2022-09-22 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PtzProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=255)),
                ('vendor_id', models.CharField(blank=True, max_length=255, null=True)),
                ('product_title', models.CharField(max_length=255)),
                ('shop_name', models.CharField(max_length=255)),
                ('slug', models.CharField(blank=True, max_length=255, null=True)),
                ('brand_id', models.IntegerField()),
                ('category_id', models.IntegerField()),
                ('subcategory_id', models.IntegerField()),
                ('sub_subcategory_id', models.IntegerField(blank=True, null=True)),
                ('product_tags', models.CharField(max_length=255)),
                ('product_sku', models.CharField(max_length=255)),
                ('product_qty', models.CharField(max_length=255)),
                ('selling_price', models.CharField(max_length=255)),
                ('discount_price', models.CharField(blank=True, max_length=255, null=True)),
                ('product_size', models.CharField(max_length=255)),
                ('product_color', models.CharField(blank=True, max_length=255, null=True)),
                ('product_material', models.CharField(blank=True, max_length=255, null=True)),
                ('end_date', models.CharField(blank=True, max_length=255, null=True)),
                ('product_thumbnail', models.CharField(max_length=255)),
                ('hot_deals', models.CharField(blank=True, max_length=255, null=True)),
                ('featured', models.CharField(blank=True, max_length=255, null=True)),
                ('is_recomended', models.IntegerField(blank=True, null=True)),
                ('special_offer', models.CharField(blank=True, max_length=255, null=True)),
                ('special_deals', models.CharField(blank=True, max_length=255, null=True)),
                ('value_of_the_day', models.IntegerField(blank=True, null=True)),
                ('weekly_offers', models.IntegerField(blank=True, null=True)),
                ('new_arrivals', models.IntegerField(blank=True, null=True)),
                ('short_description', models.TextField()),
                ('product_specification', models.TextField(blank=True, null=True)),
                ('long_description', models.TextField()),
                ('is_varified', models.CharField(max_length=255)),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'ptz_products',
                'ordering': ['-id'],
            },
        ),
    ]
