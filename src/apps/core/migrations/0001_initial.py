# Generated by Django 4.1 on 2023-12-08 20:44

import apps.storage.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=400, null=True, upload_to=apps.storage.models.upload_image_src)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
