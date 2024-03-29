# Generated by Django 3.2.3 on 2023-04-16 19:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20230416_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a70e9724-6d64-4502-8d1b-f877b9ac5f9f'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('57b2f9c9-046c-4c74-a946-22decd7ab349'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subsubcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('eabb74d6-bc73-45c5-900b-d56a31dece76'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
