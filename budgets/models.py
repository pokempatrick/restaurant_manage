from django.db import models
import os
import uuid
from datetime import timedelta
from django.utils import timezone
from django.core.validators import FileExtensionValidator

from authentification.models import User
from helpers.models import TrakingModel
from helpers.constant import STATUT
from helpers.validator import validate_file_size
# Create your models here.


class RootModel(TrakingModel):
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Budgets(RootModel):

    description = models.TextField()
    updated_by = models.ForeignKey(
        User, related_name="update_budget", on_delete=models.SET_NULL, blank=True, null=True)
    start_date = models.DateTimeField(
        blank=False, null=False, default=timezone.now)
    end_date = models.DateTimeField(
        blank=False, null=False, default=timezone.now()+timedelta(days=7))
    statut = models.CharField(
        max_length=150, choices=STATUT, default="CREATED", blank=False)

    def __str__(self) -> str:
        return f'{self.total_price} - {self.description} - {self.created_at} '

    @property
    def total_price(self):

        # dish_budget_list = DishBudgets.objects.filter(budget=self)
        dish_budget_list = self.dishbudgets_set.all()
        total = 0
        for budget_list in dish_budget_list:
            total += budget_list.total_price
        return total


class DishBudgets(RootModel):

    updated_by = models.ForeignKey(
        User, related_name="update_dish_budget", on_delete=models.SET_NULL, blank=True, null=True)
    budget = models.ForeignKey(
        Budgets, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=255)
    dish_id = models.IntegerField(blank=True, null=True)
    dish_quantity = models.IntegerField()

    @property
    def total_price(self):
        # ingredient_list = ItemIngredients.objects.filter(dish_budget=self)
        ingredient_list = self.itemingredients_set.all()
        total = 0
        for ingredient in ingredient_list:
            total += ingredient.total_price
        return total


class ItemIngredientRoots(models.Model):

    ingredient_name = models.CharField(max_length=255)
    ingredient_id = models.CharField(max_length=255, null=False, blank=False)
    quantity = models.IntegerField()


class ItemIngredients(ItemIngredientRoots):

    unit_price = models.IntegerField()
    dish_budget = models.ForeignKey(
        DishBudgets, on_delete=models.CASCADE, blank=True, null=True)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self) -> str:
        return f'{self.total_price} - {self.unit_price} - {self.dish_budget} '


class Ingredient(RootModel):

    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('documents/', filename)

    description = models.TextField()
    updated_by = models.ForeignKey(
        User, related_name="update_ingredient", on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, unique=True,)
    measure_unit = models.CharField(max_length=10)
    unit_price = models.IntegerField()
    image = models.ImageField(
        upload_to=get_file_path,
        max_length=100, blank=True, null=True,
        validators=[validate_file_size,
                    FileExtensionValidator(['jpg', 'png', 'jpeg'])]
    )


class Dish(RootModel):

    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('documents/', filename)

    name = models.CharField(max_length=100, unique=True,)
    description = models.TextField()
    unit_price = models.IntegerField()
    updated_by = models.ForeignKey(
        User, related_name="update_dish", on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(
        upload_to=get_file_path,
        max_length=100, blank=True, null=True,
        validators=[validate_file_size,
                    FileExtensionValidator(['jpg', 'png', 'jpeg'])]
    )


class Validations(RootModel):

    comment = models.TextField()
    statut = models.BooleanField(default=True)
    assign_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, related_name="assign_user")
    budgets = models.ForeignKey(
        Budgets,  on_delete=models.CASCADE, blank=True, null=True,
    )
