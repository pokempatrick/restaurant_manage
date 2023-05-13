# Generated by Django 4.2 on 2023-05-13 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dish_list', '0008_alter_dishresult_end_date'),
        ('dishes', '0008_itemingredients_inventory_validations_inventory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemingredientroots',
            name='dish_list_result',
        ),
        migrations.AddField(
            model_name='itemingredients',
            name='dish_list_result',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dish_list.dishlistresult'),
        ),
    ]
