from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from budgets.models import Budgets, DishBudgets
from helpers.serializers import TrackingSerializer
from dishes.models import ItemIngredients
from dishes.serializers import ItemIngredientsSerializer, ValidationSerializer
from helpers import constant


class BudgetsSerializer(serializers.ModelSerializer):

    added_by = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Budgets
        fields = ('id', 'statut', 'total_price',
                  'start_date', 'end_date', 'added_by', 'created_at', 'description')


class ValidationBudSerializer(ValidationSerializer):
    def validate(self, value):
        budgets = self.context["budgets"]
        assign_user = self.context["assign_user"]
        if budgets.statut == "SUBMITTED" and budgets.total_price > 0:
            if assign_user.role_name in constant.ROLE_TECHNICIAN_HERITED:
                return value
            else:
                raise serializers.ValidationError(
                    "The assign user should be a technician or a cooker.")
        else:
            raise serializers.ValidationError(
                "The statut of should be submitted.")


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
    validations_set = ValidationSerializer(
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
