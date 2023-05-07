from django.db import models
from datetime import timedelta
from django.utils import timezone

from authentification.models import User
from helpers.models import TrakingModel
from helpers.constant import STATUT
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
