from django.db import models
from datetime import timedelta
from django.utils import timezone

from helpers.models import DishListRoot, TrakingModel
from authentification.models import User
from dish_list.constant import DISHLISTSTATUT, DISHLISTSTATUTHUMAN


class DishResult(TrakingModel):
    updated_by = models.ForeignKey(
        User, related_name="update_dish_result",
        on_delete=models.SET_NULL,
        blank=True, null=True)

    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)
    start_date = models.DateTimeField(
        blank=False, null=False, default=timezone.now)
    end_date = models.DateTimeField(
        blank=False, null=False, default=timezone.now()+timedelta(days=7))
    comment = models.TextField()
    statut = models.CharField(max_length=150, choices=DISHLISTSTATUT,
                              default=DISHLISTSTATUTHUMAN["nouveau"])

    @property
    def dish_quantity(self):
        dish_list_results = self.dishlistresult_set.all()
        total = 0
        for dish_list_result in dish_list_results:
            total += dish_list_result.dish_quantity
        return total

    @property
    def total_price(self):
        dish_list_results = self.dishlistresult_set.all()
        total = 0
        for dish_list_result in dish_list_results:
            total += dish_list_result.total_price
        return total


class DishListResult(DishListRoot):
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)

    updated_by = models.ForeignKey(
        User, related_name="update_dish_list_result",
        on_delete=models.SET_NULL,
        blank=True, null=True)

    dish_result = models.ForeignKey(
        DishResult, null=True, blank=True, on_delete=models.CASCADE)

    @property
    def total_price(self):
        ingredient_list = self.itemingredients_set.all()
        total = 0
        for ingredient in ingredient_list:
            total += ingredient.total_price
        return total
