# Generated by Django 3.0.9 on 2020-09-18 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_transaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainuser',
            name='notifications_enabled',
            field=models.BooleanField(blank=True, default=True, verbose_name='Notifications enabled'),
        ),
    ]
