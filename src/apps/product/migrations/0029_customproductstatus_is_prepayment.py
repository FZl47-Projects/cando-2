# Generated by Django 4.2 on 2024-12-19 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0028_productattrgroup_type_of_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='customproductstatus',
            name='is_prepayment',
            field=models.BooleanField(default=True),
        ),
    ]
