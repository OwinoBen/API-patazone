# Generated by Django 3.2.3 on 2023-04-16 21:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20230416_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.orders'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.UUIDField(default=uuid.UUID('a138c1ea-ad5b-4e4d-bc1f-5afca92f5b1e'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]