# Generated by Django 3.2.3 on 2023-05-03 11:26

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0018_alter_orders_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7b6b4581-109a-454f-9813-f051ccbe3d8e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]