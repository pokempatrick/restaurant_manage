from django.db import models

from helpers.models import TrakingModel
from dishes.models import Dish, Ingredient
# Create your models here.


class Stocks(TrakingModel):

    dish = models.OneToOneField(
        Dish, on_delete=models.CASCADE, blank=True, null=True)

    ingredient = models.OneToOneField(
        Ingredient, on_delete=models.CASCADE, blank=True, null=True)

    quantity = models.IntegerField(default=0)
