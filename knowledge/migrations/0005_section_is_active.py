# Generated by Django 3.0.9 on 2021-09-20 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0004_auto_20210920_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Is active'),
        ),
    ]
