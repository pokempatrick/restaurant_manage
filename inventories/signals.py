from django.dispatch import receiver
from django.db.models.signals import pre_save
from dishes.models import ItemIngredients
from stocks.models import Stocks


@receiver(pre_save, sender=ItemIngredients)
def pre_save_item_ingredient_for_inventories(sender, instance, **kwargs):
    """ update for add inventories """
    if instance.inventory:
        if (instance.ingredient_id):
            stock_quantity = Stocks.objects.filter(
                ingredient__id=instance.ingredient_id).first()
            if stock_quantity:
                instance.ingredient_stock = stock_quantity.quantity
