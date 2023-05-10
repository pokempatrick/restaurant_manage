from rest_framework.test import APITestCase
from dish_list.models import DishResult, DishListResult
from dishes.models import ItemIngredientRoots
from datetime import datetime


class TestModel(APITestCase):
    @classmethod
    def setUp(self):

        self.item_ingredient_root = ItemIngredientRoots.objects.create(
            ingredient_id=1,
            ingredient_name="tomate",
            quantity=200,
        )

    def test_create_dish_list_result(self):
        dish_list_result = DishListResult.objects.create(
            dish_name="pomme pilé",
            dish_quantity=5,
            dish_id=14
        )
        dish_list_result.itemingredientroots_set.add(self.item_ingredient_root)

        self.assertIsInstance(dish_list_result, DishListResult)
        self.assertEqual(dish_list_result.dish_name, "pomme pilé")

    def test_create_dish_result(self):
        dish_list_result = DishListResult.objects.create(
            dish_name="pomme pilé",
            dish_quantity=5,
            dish_id=14
        )
        dish_list_result.itemingredientroots_set.add(self.item_ingredient_root)
        dish_result = DishResult.objects.create(
            comment="test de fonctionnement",
        )
        dish_result.dishlistresult_set.add(dish_list_result)
        self.assertEqual(dish_result.statut, "CREATED")
        self.assertIsInstance(dish_result, DishResult)
