# Generated by Django 4.2 on 2024-04-14 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0012_discountcouponselected'),
        ('navigation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tracking_code', models.CharField(max_length=40)),
                ('bank_name', models.CharField(max_length=20)),
                ('price_paid', models.PositiveBigIntegerField()),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ManualInvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.PositiveBigIntegerField()),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.cart')),
                ('discount_selected', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.discountcouponselected')),
                ('purchase', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.purchaseinvoice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivery_time', models.CharField(choices=[('fastest', 'Fastest'), ('until_completed', 'Until completed')], max_length=20)),
                ('note', models.TextField(blank=True, null=True)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='navigation.address')),
                ('cart', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.cart')),
                ('discount_selected', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.discountcouponselected')),
                ('purchase', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='payment.purchaseinvoice')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
