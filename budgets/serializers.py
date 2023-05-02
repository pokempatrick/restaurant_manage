from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from budgets.models import Budgets, DishBudgets, ItemIngredientRoots, ItemIngredients, Dish, Ingredient
from helpers.serializers import TrackingSerializer


class ItemIngredientsSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemIngredients
        fields = '__all__'


class ItemIngredientRootsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemIngredientRoots
        fields = ('ingredient_name', 'quantity')


class BudgetsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Budgets
        fields = ('id', 'statut', 'total_price',
                  'start_date', 'end_date', 'added_by', 'created_at', 'description')


class DishBudgetsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = DishBudgets
        fields = ('id', 'dish_name', 'dish_quantity',
                  'total_price', 'created_at', 'added_by')


class BudgetsDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    dishbudgets_set = DishBudgetsSerializer(
        read_only=True, default=None, many=True)

    class Meta:
        model = Budgets
        fields = '__all__'


class DishBudgetsDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    budget = BudgetsSerializer(
        read_only=True, default=None)

    itemingredients_set = ItemIngredientsSerializer(many=True)

    class Meta:
        model = DishBudgets
        fields = '__all__'


class DishBudgetsPostSerializer(TrackingSerializer):

    itemingredients_set = ItemIngredientsSerializer(many=True)

    RootObject = DishBudgets

    NestedObject = ItemIngredients

    nested_attribut = "itemingredients_set"

    root_object = "dish_budget"

    class Meta:
        model = DishBudgets
        fields = '__all__'


# class DishBudgetsOtherSerializer(serializers.ModelSerializer):

#     itemingredients_set = ItemIngredientsSerializer(many=True)

#     class Meta:
#         model = DishBudgets
#         exclude = ['budget']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class DishDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Dish
        fields = '__all__'


class DishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('name', 'unit_price', 'created_at')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'unit_price', 'created_at')
