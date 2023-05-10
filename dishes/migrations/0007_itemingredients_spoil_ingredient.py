# Generated by Django 4.2 on 2023-05-10 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sale_spoil', '0003_alter_sale_updated_by_spoilingredient_spoildish_and_more'),
        ('dishes', '0006_validations_dish_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemingredients',
            name='spoil_ingredient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sale_spoil.spoilingredient'),
        ),
    ]
