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
        spoil_ingredient = Inventories.objects.create(
            comment="mauvaise conservation"
        )
        spoil_ingredient.itemingredients_set.add(self.item_ingredient)

        self.assertIsInstance(spoil_ingredient, Inventories)
        self.assertEqual(spoil_ingredient.total_price, 7000)
