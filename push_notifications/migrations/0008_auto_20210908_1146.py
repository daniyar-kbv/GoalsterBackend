# Generated by Django 3.0.9 on 2021-09-08 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0007_auto_20210908_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noncustomizablenotificationtype',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(3, 'Об окончании периода'), (2, 'За 3 дня до окончания периода'), (4, 'Комментарий наставнику'), (5, 'Комментарий наблюдателю'), (1, 'Если пользователь не заходит 3 дня')], verbose_name='Type'),
        ),
    ]
