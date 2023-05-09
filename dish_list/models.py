from django.db import models

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

    comment = models.TextField()
    statut = models.CharField(max_length=150, choices=DISHLISTSTATUT,
                              default=DISHLISTSTATUTHUMAN["nouveau"])

    @property
    def dish_quantity(self):
        dish_result_lists = self.dishresultlist_set.all()
        total = 0
        for dish_result_list in dish_result_lists:
            total += dish_result_list.dish_quantity
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


class DishList(DishListRoot):
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)

    updated_by = models.ForeignKey(
        User, related_name="update_dish_list",
        on_delete=models.SET_NULL,
        blank=True, null=True)
    unit_price = models.IntegerField()

    @property
    def total_price(self):
        return self.unit_price*self.dish_quantity
