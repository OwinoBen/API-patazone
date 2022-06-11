# Generated by Django 4.0.4 on 2022-06-09 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiV1', '0003_ptzsubcategories_ptzsubsubcategories'),
    ]

    operations = [
        migrations.CreateModel(
            name='PtzAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('firstname', models.CharField(max_length=255)),
                ('lastname', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('county', models.CharField(max_length=255)),
                ('region', models.CharField(max_length=255)),
                ('street', models.CharField(max_length=255)),
                ('company_name', models.CharField(max_length=255)),
                ('is_default', models.IntegerField(db_column='is-default')),
                ('address_type', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField()),
            ],
            options={
                'db_table': 'ptz_address',
                'ordering': ['-id'],
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='ptzproducts',
            options={'managed': False, 'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='ptzsubsubcategories',
            options={'managed': False, 'ordering': ['-id']},
        ),
    ]
