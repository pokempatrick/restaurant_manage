from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from budgets.models import Budgets, DishBudgets, ItemIngredientRoots, ItemIngredients


class ItemIngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemIngredients
        fields = ('ingredient_name', 'quantity', 'unit_price', 'total_price')


class ItemIngredientRootsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemIngredientRoots
        fields = ('ingredient_name', 'quantity')


class DishBudgetsDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)

    itemingredients_set = [ItemIngredientsSerializer()]

    class Meta:
        model = DishBudgets
        fields = '__all__'


class DishBudgetsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DishBudgets
        fields = ('id', 'dish_name', 'dish_quantity', 'total_price')


class BudgetsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Budgets
        fields = ('id', 'statut', 'total_price',
                  'start_date', 'end_date', 'added_by')


class BudgetsDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    dishbudgets_set = [DishBudgetsSerializer()]

    class Meta:
        model = Budgets
        fields = '__all__'
