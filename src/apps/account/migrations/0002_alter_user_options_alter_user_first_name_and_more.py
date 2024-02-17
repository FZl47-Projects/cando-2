# Generated by Django 4.2.10 on 2024-02-17 20:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-id',), 'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default='بدون نام', max_length=128, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_phonenumber_confirmed',
            field=models.BooleanField(default=False, verbose_name='تایید شده'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='IR', unique=True, verbose_name='شماره تماس'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('normal_user', 'کاربر عادی'), ('operator_user', 'کاربر اپراتور'), ('super_user', 'ادمین ویژه')], default='normal_user', max_length=32, verbose_name='نقش کاربر'),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('melli_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='کد ملی')),
                ('gender', models.CharField(choices=[('unknown', 'نامشخص'), ('male', 'مرد'), ('female', 'زن')], default='unknown', max_length=16, verbose_name='جنسیت')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='زمان ویرایش')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پروفایل کاربر',
                'verbose_name_plural': 'پروفایل کاربران',
                'ordering': ('-id',),
            },
        ),
    ]
