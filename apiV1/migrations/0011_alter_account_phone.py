# Generated by Django 3.2.3 on 2022-08-25 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apiV1', '0010_remove_account_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, unique=True),
        ),
    ]