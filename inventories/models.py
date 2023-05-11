from django.db import models
from helpers.models import TrakingModel
from inventories.constant import INVENTORY_STATUT_HUMAN, INVENTORY_STATUT
from authentification.models import User

# Create your models here.


class Inventories(TrakingModel):
    added_by = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        blank=True, null=True)

    updated_by = models.ForeignKey(
        User, related_name="update_inventories",
        on_delete=models.SET_NULL,
        blank=True, null=True)
    statut = models.CharField(max_length=150, choices=INVENTORY_STATUT,
                              default=INVENTORY_STATUT_HUMAN["nouveau"])
    comment = models.TextField()

    @property
    def total_price(self):
        item_ingredient_list = self.itemingredients_set.all()
        total = 0
        for item_ingredient in item_ingredient_list:
            total += item_ingredient.total_price
        return total
