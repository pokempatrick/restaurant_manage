from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from authentification.models import User
from dishes.models import ItemIngredients
from sale_spoil.models import Sale, SpoilIngredient, SpoilDish, DishList
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


class TestSaleViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.sale_url = reverse('sale-list')
        # creation d'un utilisateur
        self.user_accountant = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_ACCOUNTANT"
        )

        # create another user
        self.user_technician = User.objects.create(
            username='cyrce12',
            email='cyretruly12@gmail.com',
            first_name="john1",
            last_name="does1",
            password='12343password',
            role_name="ROLE_TECHNICIAN"
        )

        self.user_owner = User.objects.create(
            username='cyrce152',
            email='cyretruly512@gmail.com',
            first_name="john1",
            last_name="does1",
            password='12343password',
            role_name="ROLE_OWNER"
        )

        # create a sale
        self.sale = Sale.objects.create(
            customer_first_name="John",
            customer_last_name="Does"
        )
        self.dish_list = DishList.objects.create(
            dish_name="Ndolé",
            dish_id=1,
            dish_quantity=1,
            unit_price=1000,
            sale=self.sale,
        )

    def test_create_sale(self):
        response = self.client.post(
            self.sale_url,
            json.dumps({
                "customer_first_name": "John",
                "customer_last_name": "Does",
                "dishlist_set": [{
                    "dish_name": "Ndolé",
                    "dish_quantity": 2,
                    "unit_price": 1000,
                    "dish_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_accountant.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_sale(self):
        response = self.client.put(
            self.sale_url+f'{self.sale.id}/',
            json.dumps({
                "customer_first_name": "John 5",
                "customer_last_name": "Does",
                "dishlist_set": [{
                    "dish_name": "Ndolé",
                    "dish_quantity": 2,
                    "unit_price": 1000,
                    "dish_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_owner.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_sale(self):
        response = self.client.patch(
            self.sale_url+f'{self.sale.id}/',
            json.dumps({
                "customer_first_name": "Jeanne",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_owner.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["customer_first_name"], "Jeanne")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_sale(self):
        response = self.client.get(
            self.sale_url+f'{self.sale.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_accountant.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_summary(self):
        response = self.client.get(
            self.sale_url +
            f'summary/?start_date=2022-05-13T00:00TZ&dishes={json.dumps([1,2])}',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_accountant.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_sale_with_wrong_role(self):
        response = self.client.get(
            self.sale_url+f'{self.sale.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_sale(self):
        response = self.client.get(
            self.sale_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_accountant.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_sale(self):
        response = self.client.delete(
            self.sale_url+f'{self.sale.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_owner.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_sale_with_wrong_role(self):
        response = self.client.delete(
            self.sale_url+f'{self.sale.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_accountant.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSpoilDishViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.spoil_dish_url = reverse('spoil-dish-list')
        # creation d'un utilisateur
        self.user_coocker = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_COOKER"
        )

        self.user_coocker_2 = User.objects.create(
            username='cyprien',
            email='cyprien@gmail.com',
            first_name="jaene",
            last_name="flexible",
            password='1234password',
            role_name="ROLE_COOKER"
        )

        self.user_technician = User.objects.create(
            username='cyrcooe',
            email='cyretruooly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_TECHNICIAN"
        )

        # create a spoil_dish
        self.spoil_dish = SpoilDish.objects.create(
            description="le premier essai",
            added_by=self.user_coocker_2,
        )
        self.dish_list = DishList.objects.create(
            dish_name="Ndolé",
            dish_id=1,
            dish_quantity=1,
            unit_price=1000,
            spoil_dish=self.spoil_dish,
        )

    def test_create_spoil_dish(self):
        response = self.client.post(
            self.spoil_dish_url,
            json.dumps({
                "description": "test fonctionnel 1",
                "dishlist_set": [{
                    "dish_name": "Ndolé",
                    "dish_quantity": 2,
                    "unit_price": 1000,
                    "dish_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_spoil_dish_with_wrong_role(self):
        response = self.client.post(
            self.spoil_dish_url,
            json.dumps({
                "description": "test fonctionnel 1",
                "dishlist_set": [{
                    "dish_name": "Ndolé",
                    "dish_quantity": 2,
                    "unit_price": 1000,
                    "dish_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_spoil_dish(self):
        response = self.client.put(
            self.spoil_dish_url+f'{self.spoil_dish.id}/',
            json.dumps({
                "description": "test fonctionnel",
                "dishlist_set": [{
                    "dish_name": "Ndolé",
                    "dish_quantity": 2,
                    "unit_price": 1000,
                    "dish_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["description"], "test fonctionnel")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_spoil_dish(self):
        response = self.client.patch(
            self.spoil_dish_url+f'{self.spoil_dish.id}/',
            json.dumps({
                "description": "test fonctionnel 4",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["description"], "test fonctionnel 4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_spoil_dish(self):
        response = self.client.get(
            self.spoil_dish_url+f'{self.spoil_dish.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_spoil_dish(self):
        response = self.client.get(
            self.spoil_dish_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_spoil_dish(self):
        response = self.client.delete(
            self.spoil_dish_url+f'{self.spoil_dish.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker_2.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_spoil_dish_with_wrong_user(self):
        response = self.client.delete(
            self.spoil_dish_url+f'{self.spoil_dish.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSpoilIngredientViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.spoil_ingredient_url = reverse('spoil-ingredient-list')
        # creation d'un utilisateur
        self.user_coocker = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_COOKER"
        )

        self.user_coocker_2 = User.objects.create(
            username='cyprien',
            email='cyprien@gmail.com',
            first_name="jaene",
            last_name="flexible",
            password='1234password',
            role_name="ROLE_COOKER"
        )

        self.user_technician = User.objects.create(
            username='cyrcooe',
            email='cyretruooly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_TECHNICIAN"
        )

        # create a spoil_ingredient
        self.spoil_ingredient = SpoilIngredient.objects.create(
            description="le premier essai",
            added_by=self.user_coocker_2,
        )
        ItemIngredients.objects.create(
            ingredient_name="tomate rouge",
            quantity=25,
            unit_price=100,
            ingredient_id=2,
            spoil_ingredient=self.spoil_ingredient,
        )

    def test_create_spoil_ingredient(self):
        response = self.client.post(
            self.spoil_ingredient_url,
            json.dumps({
                "description": "test fonctionnel 1",
                "itemingredients_set": [{
                    "ingredient_name": "tomate",
                    "quantity": 2,
                    "unit_price": 1000,
                    "ingredient_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_spoil_ingredient(self):
        response = self.client.put(
            self.spoil_ingredient_url+f'{self.spoil_ingredient.id}/',
            json.dumps({
                "description": "test fonctionnel",
                "itemingredients_set": [{
                    "ingredient_name": "tomate",
                    "quantity": 5,
                    "unit_price": 1000,
                    "ingredient_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_spoil_ingredient(self):
        response = self.client.patch(
            self.spoil_ingredient_url+f'{self.spoil_ingredient.id}/',
            json.dumps({
                "description": "test fonctionnel 4",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["description"], "test fonctionnel 4")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_spoil_ingredient(self):
        response = self.client.get(
            self.spoil_ingredient_url+f'{self.spoil_ingredient.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_spoil_ingredient(self):
        response = self.client.get(
            self.spoil_ingredient_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_spoil_ingredient(self):
        response = self.client.delete(
            self.spoil_ingredient_url+f'{self.spoil_ingredient.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker_2.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_spoil_ingredient_with_wrong_user(self):
        response = self.client.delete(
            self.spoil_ingredient_url+f'{self.spoil_ingredient.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_coocker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
