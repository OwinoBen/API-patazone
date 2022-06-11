# Generated by Django 4.0.4 on 2022-06-09 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiV1', '0004_ptzaddress_alter_ptzproducts_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PtzMultipleimgs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField()),
                ('img_url', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField()),
            ],
            options={
                'db_table': 'ptz_multipleimgs',
                'managed': False,
            },
        ),
    ]
