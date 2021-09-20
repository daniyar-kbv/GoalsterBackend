# Generated by Django 3.0.9 on 2021-09-20 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('celebrities', '0005_celebrity_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='celebrity',
            options={'ordering': ['my_order'], 'verbose_name': 'Celebrity', 'verbose_name_plural': 'Celebrities'},
        ),
        migrations.AddField(
            model_name='celebrity',
            name='my_order',
            field=models.PositiveIntegerField(default=0, verbose_name='Order'),
        ),
    ]
