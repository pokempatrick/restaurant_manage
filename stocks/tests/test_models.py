from rest_framework.test import APITestCase
from stocks.models import Stocks
from dishes.models import Ingredient, Dish


class TestModel(APITestCase):
    @classmethod
    def setUp(self):

        self.ingredient = Ingredient.objects.create(
            description="De la viande de boeuf en kg",
            name="Viande de boeuf",
            unit_price=3500,
            measure_unit="kg",
            group="MEET",
        )

        self.dish = Dish.objects.create(
            description="riz sauce bolonaise",
            name="Riz sauce arachide",
            unit_price=1500,
        )

    def test_create_stock_ingredient(self):
        stock_ingredient = Stocks.objects.create(
            ingredient=self.ingredient,
            quantity=5
        )
        self.assertIsInstance(stock_ingredient, Stocks)

    def test_create_stock_dish(self):
        stock_dish = Stocks.objects.create(
            dish=self.dish,
            quantity=5
        )
        self.assertIsInstance(stock_dish, Stocks)
