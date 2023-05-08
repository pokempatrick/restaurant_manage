from django.db import models

from authentification.models import User
from budgets.models import Budgets
from helpers.models import TrakingModel
from helpers.constant import PROCUREMENT_STATUT
# Create your models here.


class Procurements(TrakingModel):

    updated_by = models.ForeignKey(
        User, related_name="update_procurement",
        on_delete=models.SET_NULL,
        blank=True, null=True)

    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)

    budget = models.OneToOneField(
        Budgets, on_delete=models.CASCADE, blank=True, null=True)

    comment = models.TextField()

    statut = models.CharField(
        max_length=150, choices=PROCUREMENT_STATUT, default="CREATED")

    @property
    def total_price(self):
        ingredient_list = self.itemingredients_set.all()
        total = 0
        for ingredient in ingredient_list:
            total += ingredient.total_price
        return total

    class Meta:
        ordering = ('-created_at',)
