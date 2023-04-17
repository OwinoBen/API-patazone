# Generated by Django 3.2.3 on 2023-04-14 13:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('apiV1', '0008_auto_20230414_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('2765cede-d153-4bb7-bd2e-ce4ff1ad63df'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('adec3ff7-e3b1-4f1a-ab43-650398f84eef'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='subsubcategories',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0a5c56cc-0a43-4852-b2f1-e04c158ad7f8'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
