# Generated by Django 4.2.1 on 2023-05-30 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_apps', '0005_alter_account_auth_provider'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PtzAccountUsers',
        ),
    ]