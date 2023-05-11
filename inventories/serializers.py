from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from inventories.models import Inventories
from helpers.serializers import TrackingSerializer
from dishes.models import ItemIngredients
from dishes.serializers import ItemIngredientsSerializer, ValidationSerializer


class ValidationInvSerializer(ValidationSerializer):
    def validate(self, value):
        inventory = self.context["inventory"]
        if inventory.statut == "SUBMITTED" and inventory.total_price > 0:
            return value
        else:
            raise serializers.ValidationError(
                "The statut of should be submitted with some items.")


class InventoriesListSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Inventories
        fields = ('id', 'total_price',
                  'created_at', 'added_by', 'comment', 'statut')


class InventoriesDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    validations_set = ValidationSerializer(
        read_only=True, default=None, many=True)
    itemingredients_set = ItemIngredientsSerializer(many=True)

    class Meta:
        model = Inventories
        fields = '__all__'


class InventoriesPostSerializer(TrackingSerializer):

    itemingredients_set = ItemIngredientsSerializer(many=True)

    RootObject = Inventories

    NestedObject = ItemIngredients

    nested_attribut = "itemingredients_set"

    root_object = "inventory"

    class Meta:
        model = Inventories
        fields = '__all__'
