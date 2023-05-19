from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.shortcuts import get_object_or_404
from procurement.models import Procurements
from dishes.models import Ingredient, Dish
from dish_list.models import DishResult
from inventories.models import Inventories
from stocks.models import Stocks
from sale_spoil.models import Sale, SpoilDish, SpoilIngredient


def update_ingredient_quantity(added_number, ingredient):
    """ increase ingredient number"""
    stock_ingredient = Stocks.objects.filter(ingredient=ingredient).first()

    if (stock_ingredient):
        stock_ingredient.quantity = stock_ingredient.quantity + added_number
        stock_ingredient.save
    else:
        Stocks.objects.create(
            ingredient=ingredient,
            quantity=added_number
        )


def update_dish_quantity(added_number, dish):
    """ increase dish number"""
    stock_dish = Stocks.objects.filter(dish=dish).first()

    if (stock_dish):
        stock_dish.quantity = stock_dish.quantity + added_number
        stock_dish.save
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


@receiver(pre_save, sender=Sale)
def pre_save_sale(sender, instance, **kwargs):
    """ update for sale """
    if instance.id:
        prev_instance = Sale.objects.filter(id=instance.id).first()
        for dish_item in prev_instance.dishlist_set.all():
            dish = get_object_or_404(
                Dish, id=dish_item.dish_id)
            update_dish_quantity(-dish_item.dish_quantity, dish)


@receiver(post_save, sender=Sale)
def post_save_sale(sender, instance, **kwargs):
    for dish_item in instance.dishlist_set.all():
        dish = get_object_or_404(
            Dish, id=dish_item.dish_id)
        update_dish_quantity(dish_item.dish_quantity, dish)


@receiver(pre_delete, sender=Sale)
def pre_delete_sale(sender, instance, **kwargs):
    for dish_item in instance.dishlist_set.all():
        dish = get_object_or_404(
            Dish, id=dish_item.dish_id)
        update_dish_quantity(-dish_item.dish_quantity, dish)


@receiver(pre_save, sender=SpoilDish)
def pre_save_spoil_dish(sender, instance, **kwargs):
    """ update for spoil dish """
    if instance.id:
        prev_instance = SpoilDish.objects.filter(id=instance.id).first()
        for dish_item in prev_instance.dishlist_set.all():
            dish = get_object_or_404(
                Dish, id=dish_item.dish_id)
            update_dish_quantity(-dish_item.dish_quantity, dish)


@receiver(post_save, sender=SpoilDish)
def post_save_spoil_dish(sender, instance, **kwargs):
    for dish_item in instance.dishlist_set.all():
        dish = get_object_or_404(
            Dish, id=dish_item.dish_id)
        update_dish_quantity(dish_item.dish_quantity, dish)


@receiver(pre_delete, sender=SpoilDish)
def pre_delete_spoil_dish(sender, instance, **kwargs):
    for dish_item in instance.dishlist_set.all():
        dish = get_object_or_404(
            Dish, id=dish_item.dish_id)
        update_dish_quantity(-dish_item.dish_quantity, dish)


@receiver(pre_save, sender=SpoilIngredient)
def pre_save_spoil_ingredient(sender, instance, **kwargs):
    """ update for spoil ingredient """
    if instance.id:
        prev_instance = SpoilIngredient.objects.filter(id=instance.id).first()
        for item_ingredient in prev_instance.itemingredients_set.all():
            dish = get_object_or_404(
                Ingredient, id=item_ingredient.ingredient_id)
            update_ingredient_quantity(-item_ingredient.quantity, dish)


@receiver(post_save, sender=SpoilIngredient)
def post_save_spoil_ingredient(sender, instance, **kwargs):
    for item_ingredient in instance.itemingredients_set.all():
        ingredient = get_object_or_404(
            Ingredient, id=item_ingredient.ingredient_id)
        update_ingredient_quantity(item_ingredient.quantity, ingredient)


@receiver(pre_delete, sender=SpoilIngredient)
def pre_delete_spoil_ingredient(sender, instance, **kwargs):
    for item_ingredient in instance.itemingredients_set.all():
        ingredient = get_object_or_404(
            Ingredient, id=item_ingredient.ingredient_id)
        update_ingredient_quantity(-item_ingredient.quantity, ingredient)
