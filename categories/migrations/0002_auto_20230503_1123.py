# Generated by Django 3.2.3 on 2023-05-03 11:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('fc8a6f1a-00ff-4dd6-9465-255552bd198d'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('61ba2896-81bc-4c8b-831d-2739f865be26'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subsubcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('4aa14341-d331-45d9-abf0-358a2dbeeeea'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]