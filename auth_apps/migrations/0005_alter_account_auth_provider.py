# Generated by Django 3.2.3 on 2023-04-16 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_apps', '0004_account_is_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='auth_provider',
            field=models.CharField(blank=True, default='email', max_length=255, null=True),
        ),
    ]
