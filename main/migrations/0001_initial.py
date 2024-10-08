# Generated by Django 3.0.9 on 2020-08-06 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sphere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Sphere')),
            ],
            options={
                'verbose_name': 'Sphere',
                'verbose_name_plural': 'Spheres',
            },
        ),
        migrations.CreateModel(
            name='SelectedSphere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Creation date')),
                ('expires_at', models.DateTimeField(blank=True, verbose_name='Expiration date')),
                ('sphere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_spheres', to='main.Sphere', verbose_name='Sphere')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selected', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Selected sphere',
                'verbose_name_plural': 'Selected spheres',
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Name')),
                ('date', models.DateField(verbose_name='Date')),
                ('time', models.PositiveSmallIntegerField(choices=[(1, 'Morning'), (2, 'Day'), (3, 'Evening')], default=1, verbose_name='Time of the day')),
                ('is_done', models.BooleanField(blank=True, default=False, verbose_name='Is done')),
                ('is_shared', models.BooleanField(blank=True, default=False, verbose_name='Is shared')),
                ('observer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shared_goals', to=settings.AUTH_USER_MODEL, verbose_name='Observer')),
            ],
        ),
    ]
