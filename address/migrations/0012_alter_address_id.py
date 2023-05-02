# Generated by Django 3.2.3 on 2023-04-23 17:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0011_alter_address_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.UUIDField(default=uuid.UUID('d7dbcd74-187d-47ec-aa25-31be82a38788'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
