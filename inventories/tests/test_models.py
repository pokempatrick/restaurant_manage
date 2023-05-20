from rest_framework.test import APITestCase
from inventories.models import Inventories
from dishes.models import ItemIngredients


class TestModel(APITestCase):
    @classmethod
    def setUp(self):

        self.item_ingredient = ItemIngredients.objects.create(
            ingredient_id=1,
            ingredient_name="viande de Boeuf",
            quantity=2,
            unit_price=3500
        )

    def test_create_spoil_ingredient(self):
        inventory = Inventories.objects.create(
            comment="mauvaise conservation"
        )
        inventory.itemingredients_set.add(self.item_ingredient)

        self.assertIsInstance(inventory, Inventories)
        self.assertEqual(inventory.total_price, 7000)
