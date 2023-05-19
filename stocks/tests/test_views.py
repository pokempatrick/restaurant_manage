from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from authentification.models import User
from dishes.models import Dish, Ingredient
from stocks.models import Stocks


class TestProcurementViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.stock_url = reverse('stocks-list')
        # creation d'un utilisateur
        self.user_cooker = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_COOKER"
        )
        Stocks.objects.create(
            ingredient=Ingredient.objects.create(
                description="De la viande de boeuf en kg",
                name="Viande de boeuf",
                unit_price=3500,
                measure_unit="kg",
                group="MEET",
            ),
            quantity=5
        )
        Stocks.objects.create(
            dish=Dish.objects.create(
                description="riz sauce bolonaise",
                name="Riz sauce arachide",
                unit_price=1500,
            ),
            quantity=10
        )

    def test_get_list_stocks(self):
        response = self.client.get(
            self.stock_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
