# Generated by Django 3.2.3 on 2023-05-03 11:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0020_alter_orders_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.UUIDField(default=uuid.UUID('85607ab9-e9b3-45a4-9729-8398e2bfe559'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
