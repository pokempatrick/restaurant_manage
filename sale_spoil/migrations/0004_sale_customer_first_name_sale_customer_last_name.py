# Generated by Django 4.2 on 2023-05-10 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale_spoil', '0003_alter_sale_updated_by_spoilingredient_spoildish_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='customer_first_name',
            field=models.CharField(default='anonyme', max_length=150),
        ),
        migrations.AddField(
            model_name='sale',
            name='customer_last_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
