# Generated by Django 4.1.7 on 2023-07-03 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_category_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoriteitem',
            name='man',
        ),
    ]
