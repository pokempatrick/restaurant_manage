from rest_framework.test import APITestCase


class TestModel(APITestCase):
    @classmethod
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
