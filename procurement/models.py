from django.db import models

from authentification.models import User
from budgets.models import Budgets, RootModel
# Create your models here.


class Procurements(RootModel):
    pass

    # updated_by = models.ForeignKey(
    #     User, related_name="update_procurement",
    #     on_delete=models.SET_NULL,
    #     blank=True, null=True)
    # budget = models.OneToOneField(
    #     Budgets, on_delete=models.CASCADE)

    # comment = models.TextField()

    # @property
    # def total_price(self):
    #     ingredient_list = self.itemingredients_set.all()
    #     total = 0
    #     for ingredient in ingredient_list:
    #         total += ingredient.total_price
    #     return total
