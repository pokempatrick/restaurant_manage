from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from authentification.models import User
from dish_list.models import DishResult, DishListResult
from dishes.models import ItemIngredientRoots
from datetime import timedelta, datetime
from django.conf import settings
from dish_list.constant import DISHLISTSTATUTHUMAN


class TestDishResultViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.dish_result_url = reverse('dish_result-list')
        # creation d'un utilisateur
        self.user_cooker = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_COOKER"
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

        # create a dish_result

        self.dish_result = DishResult.objects.create(
            comment="Test de fonctionnement",
            statut=DISHLISTSTATUTHUMAN["nouveau"])
        self.dish_result_submitted = DishResult.objects.create(
            comment="Test de fonctionnement",
            statut=DISHLISTSTATUTHUMAN["Soumis"])
        self.dish_list_result = self.dish_result.dishlistresult_set.create(
            dish_name="sauce tomate",
            dish_quantity=20,
        )

    def test_create_dish_result(self):
        response = self.client.post(
            self.dish_result_url,
            json.dumps({
                "comment": "Test de fonctionnement 2",
                "statut": DISHLISTSTATUTHUMAN["nouveau"],
                "end_date": datetime.now(),
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_dish_result_with_bad_role(self):
        response = self.client.post(
            self.dish_result_url,
            json.dumps({
                "comment": "Test de fonctionnement 2",
                "statut": "VALIDATED",
                "end_date": datetime.now()
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_dish_result(self):
        response = self.client.patch(
            self.dish_result_url+f'{self.dish_result.id}/',
            json.dumps({
                "comment": "Test de fonctionnement 2",
                "statut": DISHLISTSTATUTHUMAN["nouveau"],
                "start_date": datetime.now(),
                "end_date": datetime.now()+timedelta(days=5),
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.data["statut"],
                         DISHLISTSTATUTHUMAN["nouveau"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_dish_result_statut(self):
        response = self.client.patch(
            self.dish_result_url+f'{self.dish_result.id}/',
            json.dumps({
                "statut": DISHLISTSTATUTHUMAN["Validé"],
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["statut"],
                         DISHLISTSTATUTHUMAN["Validé"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_dish_result(self):
        response = self.client.get(
            self.dish_result_url+f'{self.dish_result.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_dish_results(self):
        response = self.client.get(
            self.dish_result_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_dish_result(self):
        response = self.client.delete(
            self.dish_result_url+f'{self.dish_result.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_non_editable_dish_result(self):
        response = self.client.patch(
            self.dish_result_url+f'{self.dish_result_submitted.id}/',
            json.dumps({
                "statut": "VALIDATED",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_dish_list_results(self):
        response = self.client.post(
            self.dish_result_url+f'{self.dish_result.id}/dish_list_result/',
            json.dumps({
                "dish_name": "sauce tomate",
                "dish_quantity": 20,
                "dish_id": 5,
                "itemingredientroots_set": [{
                    "ingredient_name": "tomate",
                    "quantity": 200,
                    "ingredient_id": 1,
                }],
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data['dish_name'], "sauce tomate")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestDishListResultView(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.dish_list_result_url = reverse('dish_list_result-list')
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

        self.item_ingredient_root = ItemIngredientRoots.objects.create(
            ingredient_name="tomate rouge",
            quantity=250,
        )
        self.dish_result = DishResult.objects.create(
            comment="Test de fonctionnement",
            statut=DISHLISTSTATUTHUMAN["nouveau"])

        self.dish_list_result = DishListResult.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            dish_result=self.dish_result
        )

        self.dish_list_result.itemingredientroots_set.add(
            self.item_ingredient_root)
        self.dish_list_result_with_non_editatble_dish_result = DishListResult.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            dish_result=DishResult.objects.create(
                comment="Test de fonctionnement",
                statut="SUBMITTED")
        )

    def test_get_dish_list_result(self):
        response = self.client.get(
            self.dish_list_result_url+f'{self.dish_list_result.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_dish_list_results(self):
        response = self.client.get(
            self.dish_list_result_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_dish_list_result(self):
        response = self.client.put(
            self.dish_list_result_url+f'{self.dish_list_result.id}/',
            json.dumps({
                "dish_name": "sauce tomate",
                "dish_quantity": 30,
                "dish_id": 4,
                "itemingredientroots_set": [{
                    "id": 1,
                    "ingredient_name": "haricot",
                    "ingredient_id": 1,
                    "quantity": 200,
                }, {
                    "ingredient_name": "tomate",
                    "quantity": 20,
                    "ingredient_id": 2,
                },],
                "dish_result": self.dish_result.id,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_dish_list_result(self):
        response = self.client.patch(
            self.dish_list_result_url+f'{self.dish_list_result.id}/',
            json.dumps({
                "dish_quantity": 10,
                "itemingredientroots_set": [{
                    "id": 1,
                    "ingredient_id": 1,
                    "quantity": 200,
                }, {
                    "quantity": 20,
                    "ingredient_id": 2,
                },],
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["dish_quantity"], 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_dish_list_result(self):
        response = self.client.delete(
            self.dish_list_result_url+f'{self.dish_list_result.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_dish_list_result_with_non_editable_dish_result(self):
        response = self.client.patch(
            self.dish_list_result_url +
            f'{self.dish_list_result_with_non_editatble_dish_result.id}/',
            json.dumps({
                "dish_quantity": 158,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestValidationsView(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        # creation d'un utilisateur
        self.user_manager = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_MANAGER"
        )
        self.user_technician = User.objects.create(
            username='cyrce12',
            email='cyretruly12@gmail.com',
            first_name="john1",
            last_name="does1",
            password='12343password',
            role_name="ROLE_TECHNICIAN"
        )

        self.dish_result_created = DishResult.objects.create(
            comment="Test de fonctionnement",
            statut=DISHLISTSTATUTHUMAN["nouveau"])

        self.dish_result_submitted = DishResult.objects.create(
            comment="Test de fonctionnement",
            statut="SUBMITTED")
        DishListResult.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            dish_result=self.dish_result_submitted
        ).itemingredientroots_set.add(
            ItemIngredientRoots.objects.create(
                ingredient_name="tomate rouge",
                quantity=250,
            ))

        self.validation_url_dish_result_created = reverse(
            'validations_dish_result', args=[self.dish_result_created.id])

        self.validation_url_dish_result_submitted = reverse(
            'validations_dish_result', args=[self.dish_result_submitted.id])

    def test_add_validation(self):
        """ create validation for dish_result """
        response = self.client.post(
            self.validation_url_dish_result_submitted,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_validation_with_wrong_role(self):
        response = self.client.post(
            self.validation_url_dish_result_submitted,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_validation_with_wrong_initial_statut(self):
        """ reject validation since the statut is not submitted """
        response = self.client.post(
            self.validation_url_dish_result_created,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
                "assign_user": self.user_manager.id,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
