# Generated by Django 4.2 on 2024-04-17 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_alter_basicproduct_image_cover_and_more'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]