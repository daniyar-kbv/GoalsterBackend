# Generated by Django 3.0.9 on 2020-08-06 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200806_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='goal',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='observation', to='main.Goal', verbose_name='Goal'),
        ),
    ]
