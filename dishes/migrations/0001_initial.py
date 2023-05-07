# Generated by Django 4.2 on 2023-05-07 09:27

import dishes.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import helpers.validator


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('budgets', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemIngredientRoots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_name', models.CharField(max_length=255)),
                ('ingredient_id', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Validations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField()),
                ('statut', models.BooleanField(default=True)),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('assign_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assign_user', to=settings.AUTH_USER_MODEL)),
                ('budgets', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.budgets')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('name', models.CharField(max_length=100, unique=True)),
                ('measure_unit', models.CharField(max_length=10)),
                ('unit_price', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=dishes.models.Ingredient.get_file_path, validators=[helpers.validator.validate_file_size, django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])])),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_ingredient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('unit_price', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=dishes.models.Dish.get_file_path, validators=[helpers.validator.validate_file_size, django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])])),
                ('added_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_dish', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItemIngredients',
            fields=[
                ('itemingredientroots_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dishes.itemingredientroots')),
                ('unit_price', models.IntegerField()),
                ('dish_budget', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='budgets.dishbudgets')),
            ],
            bases=('dishes.itemingredientroots',),
        ),
    ]
