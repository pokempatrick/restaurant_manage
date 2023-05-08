from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from procurement.models import Procurements
from helpers.serializers import TrackingSerializer
from budgets.serializers import BudgetsSerializer
from dishes.models import ItemIngredients
from dishes.serializers import ItemIngredientsSerializer, ValidationSerializer


class ValidationProcSerializer(ValidationSerializer):
    def validate(self, value):
        procurements = self.context["procurements"]
        if procurements.statut == "SUBMITTED" and procurements.total_price > 0:
            return value
        else:
            raise serializers.ValidationError(
                "The statut of should be submitted with some items.")


class ProcurementsListSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Procurements
        fields = ('id', 'total_price',
                  'created_at', 'added_by', 'comment', 'statut')


class ProcurementsDetailsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)
    updated_by = RegisterSerilizer(
        read_only=True, default=None)
    budget = BudgetsSerializer(
        read_only=True, default=None)
    validations_set = ValidationSerializer(
        read_only=True, default=None, many=True)
    itemingredients_set = ItemIngredientsSerializer(many=True)

    class Meta:
        model = Procurements
        fields = '__all__'


class ProcurementsPostSerializer(TrackingSerializer):

    itemingredients_set = ItemIngredientsSerializer(many=True)

    RootObject = Procurements

    NestedObject = ItemIngredients

    nested_attribut = "itemingredients_set"

    root_object = "procurement"

    class Meta:
        model = Procurements
        fields = '__all__'
