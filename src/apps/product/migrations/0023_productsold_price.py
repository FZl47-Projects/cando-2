# Generated by Django 4.2 on 2024-04-22 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_productinventorydefault'),
    ]

    operations = [
        migrations.AddField(
            model_name='productsold',
            name='price',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
