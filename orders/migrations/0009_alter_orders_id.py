# Generated by Django 3.2.3 on 2023-04-16 21:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20230416_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6ccb7cbd-6bec-4406-b03f-3dc1fe2c87ef'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]