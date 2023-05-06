from rest_framework.test import APITestCase
from budgets.models import Budgets, ItemIngredients, DishBudgets, Validations
from datetime import datetime


class TestModel(APITestCase):
    @classmethod
    def setUp(self):
        self.budget = Budgets.objects.create(
            description="Test de fonctionnement 1",
            statut="nouveau")

        self.item_ingredient = ItemIngredients.objects.create(
            ingredient_name="tomate",
            quantity=200,
            unit_price=1,
        )

    def test_create_budget(self):
        budget = Budgets.objects.create(
            description="Test de fonctionnement",
            statut="nouveau")
        self.assertIsInstance(budget, Budgets)
        self.assertEqual(budget.total_price, 0)

    def test_create_item_ingredient(self):
        item_ingredient = ItemIngredients.objects.create(
            ingredient_name="tomate",
            ingredient_id=25,
            quantity=200,
            unit_price=1,
        )
        self.assertIsInstance(item_ingredient, ItemIngredients)
        self.assertEqual(item_ingredient.total_price, 200)

    def test_create_dish_budget(self):
        dish_budget = DishBudgets.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            budget=self.budget
        )
        dish_budget.itemingredients_set.add(self.item_ingredient)
        self.assertIsInstance(dish_budget, DishBudgets)
        self.assertEqual(dish_budget.total_price, 200)

    def test_create_validation(self):
        validation = Validations.objects.create(
            comment="everything is ok",
            statut=True,
            budgets=self.budget
        )
        self.assertIsInstance(validation, Validations)
