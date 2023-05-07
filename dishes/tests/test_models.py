from rest_framework.test import APITestCase
from dishes.models import ItemIngredients, Validations


class TestModel(APITestCase):
    @classmethod
    def setUp(self):

        self.item_ingredient = ItemIngredients.objects.create(
            ingredient_name="tomate",
            quantity=200,
            unit_price=1,
        )

    def test_create_item_ingredient(self):
        item_ingredient = ItemIngredients.objects.create(
            ingredient_name="tomate",
            ingredient_id=25,
            quantity=200,
            unit_price=1,
        )
        self.assertIsInstance(item_ingredient, ItemIngredients)
        self.assertEqual(item_ingredient.total_price, 200)

    def test_create_validation(self):
        validation = Validations.objects.create(
            comment="everything is ok",
            statut=True,
        )
        self.assertIsInstance(validation, Validations)
