# Generated by Django 4.2 on 2024-04-17 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_cart_tc_cartstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartstatus',
            name='status',
            field=models.CharField(choices=[('cancelled', 'Cancelled'), ('in_progress', 'In_progress'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='in_progress', max_length=14),
        ),
    ]