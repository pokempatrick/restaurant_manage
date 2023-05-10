from django.db import models
from django.core.validators import MinValueValidator

from helpers.models import DishListRoot, TrakingModel
from authentification.models import User


class Sale(TrakingModel):
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)

    updated_by = models.ForeignKey(
        User, related_name="update_sale",
        on_delete=models.SET_NULL,
        blank=True, null=True)

    customer_first_name = models.CharField(max_length=150, default="anonyme")
    customer_last_name = models.CharField(
        max_length=150, blank=True, null=True)

    @property
    def total_price(self):
        dish_sold_list = self.dishlist_set.all()
        total = 0
        for dish_sold in dish_sold_list:
            total += dish_sold.total_price
        return total


class SpoilDish(TrakingModel):
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)

    updated_by = models.ForeignKey(
        User, related_name="update_spoil",
        on_delete=models.SET_NULL,
        blank=True, null=True)

    description = models.TextField()

    @property
    def total_price(self):
        dish_spoil_list = self.dishlist_set.all()
        total = 0
        for dish_spoil in dish_spoil_list:
            total += dish_spoil.total_price
        return total


class SpoilIngredient(TrakingModel):
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)

    updated_by = models.ForeignKey(
        User, related_name="update_ingredient_spoil",
        on_delete=models.SET_NULL,
        blank=True, null=True)

    description = models.TextField()

    @property
    def total_price(self):
        item_ingredient_list = self.itemingredients_set.all()
        total = 0
        for item_ingredient in item_ingredient_list:
            total += item_ingredient.total_price
        return total


class DishList(DishListRoot):
    unit_price = models.IntegerField(
        validators=[MinValueValidator(limit_value=0)]
    )

    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE, null=True,
        blank=True
    )

    spoil_dish = models.ForeignKey(
        SpoilDish, on_delete=models.CASCADE, null=True,
        blank=True
    )

    @property
    def total_price(self):
        return self.unit_price*self.dish_quantity
