from django.dispatch import receiver
from django.db.models.signals import post_save
from procurement.models import Procurements
from dishes.models import Ingredient


@receiver(post_save, sender=Procurements)
def save_post(sender, instance, **kwargs):
    """ update ingredient unit_price with procurement validation """
    if instance.statut == "CLOSED":
        for item_ingredient in instance.itemingredients_set.all():
            ingredient = Ingredient.objects.get(
                id=item_ingredient.ingredient_id)
            ingredient.unit_price = item_ingredient.unit_price
            ingredient.save
