# Generated by Django 3.2.3 on 2023-04-16 19:30

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20230416_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.UUIDField(default=uuid.UUID('ce92b7bf-e8d0-4132-82a0-2edddf689c96'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]