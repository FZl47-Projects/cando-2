# Generated by Django 4.2 on 2024-03-10 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_basicproduct_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='description',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='title',
        ),
    ]
