# Generated by Django 2.0.5 on 2018-06-21 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventarioCEI', '0004_auto_20180621_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AlterField(
            model_name='profile',
            name='mail',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
