from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from sale_spoil.models import DishList, Sale, SpoilDish, SpoilIngredient
from helpers.serializers import TrackingSerializer
from dishes.models import ItemIngredients
from dishes.serializers import ItemIngredientsSerializer


class SaleSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Sale
        fields = ('id', 'total_price', 'added_by', 'created_at', 'updated_at')


class SpoilDishSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = SpoilDish
        fields = ('id', 'total_price', 'added_by', 'created_at', 'updated_at')


class SpoilIngredientSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = SpoilIngredient
        fields = ('id', 'total_price', 'added_by', 'created_at', 'updated_at')


class DishListSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = DishList
        fields = '__all__'


class SaleDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    dishlist_set = DishListSerializer(
        read_only=True, default=None, many=True)

    class Meta:
        model = Sale
        fields = '__all__'


class SpoilDishDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    dishlist_set = DishListSerializer(
        read_only=True, default=None, many=True)

    class Meta:
        model = SpoilDish
        fields = '__all__'


class SpoilIngredientDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    itemingredients_set = ItemIngredientsSerializer(
        read_only=True, default=None, many=True)

    class Meta:
        model = SpoilIngredient
        fields = '__all__'


class SalePostSerializer(TrackingSerializer):

    dishlist_set = DishListSerializer(many=True)

    RootObject = Sale

    NestedObject = DishList

    nested_attribut = "dishlist_set"

    root_object = "sale"

    class Meta:
        model = Sale
        fields = '__all__'


class SpoilDishPostSerializer(TrackingSerializer):

    dishlist_set = DishListSerializer(many=True)

    RootObject = SpoilDish

    NestedObject = DishList

    nested_attribut = "dishlist_set"

    root_object = "spoil_dish"

    class Meta:
        model = SpoilDish
        fields = '__all__'


class SpoilIngredientPostSerializer(TrackingSerializer):

    itemingredients_set = ItemIngredientsSerializer(many=True)

    RootObject = SpoilIngredient

    NestedObject = ItemIngredients

    nested_attribut = "itemingredients_set"

    root_object = "spoil_ingredient"

    class Meta:
        model = SpoilIngredient
        fields = '__all__'


class DishListSummarySerializer(serializers.ModelSerializer):

    total_quantity = serializers.IntegerField()
    total_cost = serializers.IntegerField()
    occurences = serializers.IntegerField()

    class Meta:
        model = DishList
        fields = ('dish_name', 'occurences', 'total_cost', 'total_quantity')
