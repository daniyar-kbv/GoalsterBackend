# Generated by Django 3.0.9 on 2020-09-30 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_transaction_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-created_at'], 'verbose_name': 'Transaction', 'verbose_name_plural': 'Transactions'},
        ),
    ]
