from rest_framework.test import APITestCase
from dishes.models import ItemIngredients
from procurement.models import Procurements
from budgets.models import Budgets


class TestModel(APITestCase):
    @classmethod
    def setUp(self):
        self.budget = Budgets.objects.create(
            description="Test de fonctionnement 1",
            statut="nouveau")

    def test_create_procurement(self):
        procurement = Procurements.objects.create(
            budget=self.budget,
            comment="everything is ok")
        ItemIngredients.objects.create(
            ingredient_name="tomate",
            ingredient_id=2,
            quantity=20,
            unit_price=100,
            procurement=procurement,
        )

        self.assertIsInstance(procurement, Procurements)
        self.assertEqual(procurement.total_price, 2000)
