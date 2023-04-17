# Generated by Django 3.2.3 on 2023-04-16 21:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('apiV1', '0015_auto_20230416_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('d2b93fdb-3920-453d-889f-3c9e592a511a'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('4bf795bc-e50d-4ce4-a741-0744dc3ea9ac'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subsubcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b5b4c09a-a9f1-49c5-a863-3325b2391c45'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
