# Generated by Django 3.0.9 on 2021-09-15 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('celebrities', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celebritygoal',
            name='user',
        ),
    ]
