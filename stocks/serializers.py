from rest_framework import serializers
from stocks.models import Stocks
from dishes.serializers import IngredientListSerializer, DishRetrieveListSerializer


class StocksSerializer(serializers.ModelSerializer):

    ingredient = IngredientListSerializer(
        read_only=True, default=None)
    dish = DishRetrieveListSerializer(
        read_only=True, default=None)

    class Meta:
        model = Stocks
        fields = '__all__'
