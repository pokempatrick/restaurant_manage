# Generated by Django 4.2 on 2023-05-18 12:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish_list', '0009_alter_dishresult_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishresult',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 25, 12, 54, 14, 588567, tzinfo=datetime.timezone.utc)),
        ),
    ]
