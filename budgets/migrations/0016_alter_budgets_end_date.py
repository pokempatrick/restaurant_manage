# Generated by Django 4.2 on 2023-04-29 13:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0015_alter_budgets_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budgets',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 6, 13, 24, 10, 826018, tzinfo=datetime.timezone.utc)),
        ),
    ]
