# Generated by Django 4.2 on 2023-05-10 02:26

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dish_list', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dishresult',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 17, 2, 26, 25, 641373, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='dishresult',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]