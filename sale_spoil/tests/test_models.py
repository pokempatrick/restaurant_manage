from rest_framework.test import APITestCase
from sale_spoil.models import DishList, SpoilIngredient, Sale, SpoilDish
from dishes.models import ItemIngredients
from datetime import datetime


class TestModel(APITestCase):
    @classmethod
    def setUp(self):

        self.item_ingredient = ItemIngredients.objects.create(
            ingredient_id=1,
            ingredient_name="viande de Boeuf",
            quantity=2,
            unit_price=3500
        )

    def test_create_dish_list(self):
        dish_list = DishList.objects.create(
            unit_price=200,
            dish_name="pomme pilé",
            dish_quantity=5,
            dish_id=14
        )
        self.assertIsInstance(dish_list, DishList)
        self.assertEqual(dish_list.total_price, 1000)

    def test_create_sale(self):
        sale = Sale.objects.create(
            customer_first_name="John",
            customer_last_name="Does"
        )
        DishList.objects.create(
            unit_price=1000,
            dish_name="pomme pilé",
            dish_quantity=2,
            dish_id=14,
            sale=sale,
        )
        self.assertIsInstance(sale, Sale)
        self.assertEqual(sale.total_price, 2000)

    def test_create_spoil_ingredient(self):
        spoil_ingredient = SpoilIngredient.objects.create(
            description="mauvaise conservation"
        )
        spoil_ingredient.itemingredients_set.add(self.item_ingredient)

        self.assertIsInstance(spoil_ingredient, SpoilIngredient)
        self.assertEqual(spoil_ingredient.total_price, 7000)

    def test_create_spoil_dish(self):
        spoil_dish = SpoilDish.objects.create(
            description="mauvaise conservation"
        )
        DishList.objects.create(
            unit_price=1000,
            dish_name="pomme pilé",
            dish_quantity=2,
            dish_id=14,
            spoil_dish=spoil_dish,
        )
        self.assertIsInstance(spoil_dish, SpoilDish)
        self.assertEqual(spoil_dish.total_price, 2000)
