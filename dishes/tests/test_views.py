from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from authentification.models import User
from dishes.models import Dish, Ingredient, ItemIngredients


class DishView(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.dish_url = reverse('dish-list')
        # creation d'un utilisateur
        self.user_cooker = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_COOKER"
        )
        self.user_technician = User.objects.create(
            username='cyrce12',
            email='cyretruly12@gmail.com',
            first_name="john1",
            last_name="does1",
            password='12343password',
            role_name="ROLE_TECHNICIAN"
        )

        self.dish = Dish.objects.create(
            name="sauce arachide",
            description="une très bonne sauce",
            unit_price=100,
        )

    def test_add_dish(self):
        response = self.client.post(
            self.dish_url,
            json.dumps({
                "name": "sauce tomate",
                "unit_price": 100,
                "description": "une bonne sauce",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data['name'], "sauce tomate")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_dish(self):
        response = self.client.get(
            self.dish_url+f'{self.dish.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_dish(self):
        response = self.client.get(
            self.dish_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_update_dish(self):
        response = self.client.put(
            self.dish_url+f'{self.dish.id}/',
            json.dumps({
                "name": "sauce tomate",
                "unit_price": 150,
                "description": "une bonne sauce",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_dish(self):
        response = self.client.patch(
            self.dish_url+f'{self.dish.id}/',
            json.dumps({
                "name": "sauce jaune",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["name"], "sauce jaune")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_dish(self):
        response = self.client.delete(
            self.dish_url+f'{self.dish.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class IngredientView(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.ingredient_url = reverse('ingredient-list')
        # creation d'un utilisateur
        self.user_cooker = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_COOKER"
        )
        self.user_technician = User.objects.create(
            username='cyrce12',
            email='cyretruly12@gmail.com',
            first_name="john1",
            last_name="does1",
            password='12343password',
            role_name="ROLE_TECHNICIAN"
        )

        self.ingredient = Ingredient.objects.create(
            name="sauce arachide",
            description="une très bonne sauce",
            unit_price=100,
            measure_unit="kg",
        )

    def test_add_ingredient(self):
        response = self.client.post(
            self.ingredient_url,
            json.dumps({
                "name": "sauce tomate",
                "unit_price": 100,
                "description": "une bonne sauce",
                "measure_unit": "kg",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data['name'], "sauce tomate")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_ingredient(self):
        response = self.client.get(
            self.ingredient_url+f'{self.ingredient.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_ingredient(self):
        response = self.client.get(
            self.ingredient_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 1)

    def test_update_ingredient(self):
        response = self.client.put(
            self.ingredient_url+f'{self.ingredient.id}/',
            json.dumps({
                "name": "sauce tomate",
                "unit_price": 150,
                "description": "une bonne sauce",
                "measure_unit": "kg",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_ingredient(self):
        response = self.client.patch(
            self.ingredient_url+f'{self.ingredient.id}/',
            json.dumps({
                "name": "sauce jaune",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["name"], "sauce jaune")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_ingredient(self):
        response = self.client.delete(
            self.ingredient_url+f'{self.ingredient.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_ingredient_with_wrong_access_right(self):
        response = self.client.delete(
            self.ingredient_url+f'{self.ingredient.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ItemIngredientView(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.item_ingredient_url = reverse('item_ingredient')
        # creation d'un utilisateur
        self.user_cooker = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_COOKER"
        )

        ItemIngredients.objects.create(
            ingredient_name="tomate rouge",
            quantity=25,
            unit_price=100,)

    def test_get_list_item_ingredient(self):
        response = self.client.get(
            self.item_ingredient_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
