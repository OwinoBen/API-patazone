# Generated by Django 3.2.3 on 2023-04-16 21:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0004_alter_address_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='id',
            field=models.UUIDField(default=uuid.UUID('49d98e96-44a2-495c-a1db-5be1f878314c'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
