# Generated by Django 3.0.9 on 2023-09-09 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20230909_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='created_at',
        ),
    ]
