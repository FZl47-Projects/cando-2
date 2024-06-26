# Generated by Django 4.2 on 2024-04-10 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_customproductstatus'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customproduct',
            options={'ordering': ('-id',)},
        ),
        migrations.CreateModel(
            name='CustomProductCart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.cart')),
                ('custom_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.customproduct')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
