# Generated by Django 4.2 on 2023-05-13 22:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish_list', '0008_alter_dishresult_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishresult',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 20, 22, 14, 52, 87129, tzinfo=datetime.timezone.utc)),
        ),
    ]
