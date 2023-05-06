# Generated by Django 3.2.3 on 2023-04-16 21:35

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20230416_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitems',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.orders'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='id',
            field=models.UUIDField(default=uuid.UUID('3c1e06a9-905a-4e91-91d8-ec3a77aeb7b2'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]