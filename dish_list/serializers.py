from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from dish_list.models import DishResult, DishListResult
from helpers.serializers import TrackingSerializer
from dishes.models import ItemIngredients
from dishes.serializers import ItemIngredientsSerializer, ValidationSerializer


class DishResultSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = DishResult
        fields = ('id', 'statut',
                  'start_date', 'end_date', 'added_by', 'created_at', 'comment')


class ValidationDishResultSerializer(ValidationSerializer):
    def validate(self, value):
        dish_result = self.context["dish_result"]
        if dish_result.statut == "SUBMITTED" and dish_result.dish_quantity > 0:
            return value
        else:
            raise serializers.ValidationError(
                "The statut of should be submitted with some items.")


class DishListResultSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = DishListResult
        fields = ('id', 'dish_name', 'dish_quantity', 'dish_id',
                  'created_at', 'added_by', 'dish_result',)


class DishResultDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    dishlistresult_set = DishListResultSerializer(
        read_only=True, default=None, many=True)
    validations_set = ValidationSerializer(
        read_only=True, default=None, many=True)

    class Meta:
        model = DishResult
        fields = '__all__'


class DishListResultDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    dish_result = DishResultSerializer(
        read_only=True, default=None)
    itemingredients_set = ItemIngredientsSerializer(many=True)

    class Meta:
        model = DishListResult
        fields = '__all__'


class DishListResultPostSerializer(TrackingSerializer):

    itemingredients_set = ItemIngredientsSerializer(many=True)

    RootObject = DishListResult

    NestedObject = ItemIngredients

    nested_attribut = "itemingredients_set"

    root_object = "dish_list_result"

    class Meta:
        model = DishListResult
        fields = '__all__'
