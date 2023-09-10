# Generated by Django 3.0.9 on 2023-09-09 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0004_auto_20230909_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='transaction',
            name='remaining_amount',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='remaining_period',
            field=models.PositiveIntegerField(null=True),
        ),
    ]