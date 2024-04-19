# Generated by Django 4.2 on 2024-04-17 00:51

import apps.product.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0013_productsold'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tc',
            field=models.CharField(default=apps.product.models.cart_tc_code, max_length=14),
        ),
        migrations.CreateModel(
            name='CartStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('cancelled', 'Cancelled'), ('in_progress', 'In_progress'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], max_length=14)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.cart')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
