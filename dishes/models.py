from django.db import models
import os
import uuid
from django.core.validators import FileExtensionValidator

from budgets.models import DishBudgets, RootModel, Budgets
from dishes.constant import INGREDIENTGROUP, INGREDIENTGROUPLIST
from helpers.models import TrakingModel
from procurement.models import Procurements
from dish_list.models import DishListResult, DishResult
from authentification.models import User
from helpers.validator import validate_file_size


class ItemIngredientRoots(TrakingModel):

    ingredient_name = models.CharField(max_length=255)
    ingredient_id = models.CharField(max_length=255, null=False, blank=False)
    quantity = models.IntegerField()
    dish_list_result = models.ForeignKey(
        DishListResult, on_delete=models.CASCADE, blank=True, null=True)


class ItemIngredients(ItemIngredientRoots):

    unit_price = models.IntegerField()
    dish_budget = models.ForeignKey(
        DishBudgets, on_delete=models.CASCADE, blank=True, null=True)
    procurement = models.ForeignKey(
        Procurements, on_delete=models.CASCADE, blank=True, null=True)

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

    group = models.CharField(
        max_length=150, choices=INGREDIENTGROUP, default=INGREDIENTGROUPLIST["Autres"], blank=False)
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
    procurements = models.ForeignKey(
        Procurements, on_delete=models.CASCADE, blank=True, null=True)
    dish_result = models.ForeignKey(
        DishResult, on_delete=models.CASCADE, blank=True, null=True)
