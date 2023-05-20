from dishes.models import ItemIngredients
from django.db.models import Sum, Count


def root_query_set(start_date, end_date, process):
    root_query = ItemIngredients.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date,).values(
        "ingredient_name").annotate(
        total_quantity=Sum("quantity"),
        total_ingredient_stock=Sum("ingredient_stock"),
        occurences=Count("ingredient_id")).order_by("-ingredient_id")
    if process == "inventory":
        return root_query.filter(inventory__statut="APPROVED")
    if process == "procurement":
        return root_query.filter(procurement__statut="CLOSED")
    if process == "spoil_ingredient":
        return root_query.filter(spoil_ingredient__id__gte=0)
    if process == "dish_list_result":
        return root_query.filter(dish_list_result__dish_result__statut="APPROVED")
