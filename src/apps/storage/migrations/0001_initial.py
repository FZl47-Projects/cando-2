# Generated by Django 4.2 on 2024-04-17 18:12

import apps.core.mixins.models
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
            bases=(apps.core.mixins.models.RemovePastFileMixin, models.Model),
        ),
    ]
