# Generated by Django 4.2 on 2024-03-15 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('product', '0020_alter_factorcakeimage_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factorcakeimage',
            name='images',
            field=models.ManyToManyField(blank=True, to='core.image'),
        ),
    ]
