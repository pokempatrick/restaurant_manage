from rest_framework.test import APITestCase
from procurement.models import Procurements
from budgets.models import ItemIngredients, Budgets


class TestModel(APITestCase):
    @classmethod
    def setUp(self):
        self.budget = Budgets.objects.create(
            description="Test de fonctionnement 1",
            statut="nouveau")

    def test_create_procurement(self):
        pass
        # procurement = Procurements.objects.create(
        #     budget=self.budget,
        #     comment="everything is ok").itemingredients_set.add(
        #         ItemIngredients.objects.create(
        #             ingredient_name="tomate",
        #             ingredient_id=2,
        #             quantity=20,
        #             unit_price=100,
        #         )
        # )

        # self.assertIsInstance(procurement, Procurements)
        # self.assertEqual(procurement.total_price, 2000)
