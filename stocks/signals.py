from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete
from django.shortcuts import get_object_or_404
from procurement.models import Procurements
from dishes.models import Ingredient, Dish, ItemIngredients
from dish_list.models import DishResult
from inventories.models import Inventories
from stocks.models import Stocks
from sale_spoil.models import DishList


def update_ingredient_quantity(added_number, ingredient):
    """ increase ingredient number"""
    stock_ingredient = Stocks.objects.filter(ingredient=ingredient).first()

    if (stock_ingredient):
        stock_ingredient.quantity += added_number
        stock_ingredient.save()
    else:
        Stocks.objects.create(
            ingredient=ingredient,
            quantity=added_number
        )


def update_dish_quantity(added_number, dish):
    """ increase dish number"""
    stock_dish = Stocks.objects.filter(dish=dish).first()

    if (stock_dish):
        stock_dish.quantity += added_number
        stock_dish.save()
    else:
        Stocks.objects.create(
            dish=dish,
            quantity=added_number
        )


@receiver(post_save, sender=Procurements)
def post_save_procurement(sender, instance, **kwargs):
    """ update for add procurement """
    if instance.statut == "CLOSED":
        item_ingredients = instance.itemingredients_set.all()
        for item_ingredient in item_ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=item_ingredient.ingredient_id)
            update_ingredient_quantity(item_ingredient.quantity, ingredient)


@receiver(post_save, sender=DishResult)
def post_save_dish_result(sender, instance, **kwargs):
    """ update for add dish result """
    if instance.statut == "APPROVED":
        dish_list_results = instance.dishlistresult_set.all()
        for dish_list_result in dish_list_results:
            dish = get_object_or_404(
                Dish, id=dish_list_result.dish_id)
            update_dish_quantity(dish_list_result.dish_quantity, dish)
            for item_ingredient in dish_list_result.itemingredients_set.all():
                ingredient = get_object_or_404(
                    Ingredient, id=item_ingredient.ingredient_id)
                update_ingredient_quantity(
                    -item_ingredient.quantity, ingredient)


@receiver(post_save, sender=Inventories)
def post_save_inventories(sender, instance, **kwargs):
    """ update for add inventories """
    if instance.statut == "APPROVED":
        item_ingredients = instance.itemingredients_set.all()
        for item_ingredient in item_ingredients:
            # item_ingredient gap to be added
            ingredient = get_object_or_404(
                Ingredient, id=item_ingredient.ingredient_id)
            update_ingredient_quantity(item_ingredient.gap, ingredient)


@receiver(pre_save, sender=DishList)
def pre_save_dish_list(sender, instance, **kwargs):
    if instance.id and (bool(instance.sale or instance.spoil_dish)):
        prev_instance = DishList.objects.filter(id=instance.id).first()
        dish = get_object_or_404(
            Dish, id=instance.dish_id)
        update_dish_quantity(prev_instance.dish_quantity, dish)


@receiver(post_save, sender=DishList)
def post_save_dish_list(sender, instance, **kwargs):
    if (bool(instance.sale or instance.spoil_dish)):
        dish = get_object_or_404(
            Dish, id=instance.dish_id)
        update_dish_quantity(-instance.dish_quantity, dish)


@receiver(pre_delete, sender=DishList)
def pre_delete_dish_list(sender, instance, **kwargs):
    if (bool(instance.sale or instance.spoil_dish)):
        dish = get_object_or_404(
            Dish, id=instance.dish_id)
        update_dish_quantity(instance.dish_quantity, dish)


@receiver(pre_save, sender=ItemIngredients)
def pre_save_spoil_ingredient(sender, instance, **kwargs):
    if instance.id and bool(instance.spoil_ingredient):
        prev_instance = ItemIngredients.objects.filter(id=instance.id).first()
        ingredient = get_object_or_404(
            Ingredient, id=instance.ingredient_id)
        update_ingredient_quantity(prev_instance.quantity, ingredient)


@receiver(post_save, sender=ItemIngredients)
def post_save_spoil_ingredient(sender, instance, **kwargs):
    if (bool(instance.spoil_ingredient)):
        ingredient = get_object_or_404(
            Ingredient, id=instance.ingredient_id)
        update_ingredient_quantity(-instance.quantity, ingredient)


@receiver(pre_delete, sender=ItemIngredients)
def pre_delete_spoil_ingredient(sender, instance, **kwargs):
    if (bool(instance.spoil_ingredient)):
        ingredient = get_object_or_404(
            Ingredient, id=instance.ingredient_id)
        update_ingredient_quantity(instance.quantity, ingredient)
