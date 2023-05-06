# Generated by Django 3.2.3 on 2023-05-03 11:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0014_alter_address_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.UUIDField(default=uuid.UUID('e105da89-7d91-42d0-9f34-03ba1c2b28ae'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]