from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from dishes.models import Dish, Ingredient, Validations, ItemIngredientRoots, ItemIngredients
from helpers import constant


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


class ValidationSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    assign_user = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Validations
        fields = '__all__'


class ItemIngredientsSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemIngredients
        fields = '__all__'


class ItemIngredientRootsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemIngredientRoots
        fields = ('ingredient_name', 'quantity')
