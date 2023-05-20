from sale_spoil.models import DishList
from django.db.models import Sum, Count, F


def root_query_summary(start_date, end_date, process):
    root_query = DishList.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date,).values(
        "dish_name").annotate(
        total_quantity=Sum("dish_quantity"),
        total_cost=Sum(F('unit_price')*F('dish_quantity')),
        occurences=Count("dish_name")).order_by("-dish_id")
    if process == "sale":
        return root_query.filter(sale__id__gt=0)
    else:
        return root_query.filter(spoil_dish__id__gt=0)
