# Generated by Django 3.0.9 on 2023-09-09 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0003_auto_20230909_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]