# Generated by Django 3.2.3 on 2023-04-16 21:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('apiV1', '0012_auto_20230416_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('def92a29-7c54-402d-892b-7e4ec95a1d60'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('509835b6-227a-4c94-960a-17ae7a567f48'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subsubcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('11c307d8-5139-42e8-87fc-6aaf43b89e76'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
