# Generated by Django 3.0.9 on 2020-08-18 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20200817_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='placeholder',
            field=models.CharField(max_length=500, null=True, verbose_name='Placeholder'),
        ),
    ]
