from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from authentification.models import User
from dishes.models import ItemIngredients, Ingredient
from inventories.models import Inventories
from django.core.serializers.json import DjangoJSONEncoder


class TestInventoriesViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.inventories_url = reverse('inventories-list')
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

        # create a inventories

        self.item_ingredient = ItemIngredients.objects.create(
            ingredient_name="tomate rouge",
            quantity=250,
            unit_price=1,
        )
        self.inventories = Inventories.objects.create(
            comment="Test de fonctionnement",
            added_by=self.user_technician,
        )
        self.inventories.itemingredients_set.add(self.item_ingredient)

        """ inventory setup for summary """
        self.inventories_approved = Inventories.objects.create(
            comment="Test de fonctionnement",
            added_by=self.user_technician,
            statut="APPROVED"
        )
        self.inventories_approved.itemingredients_set.add(
            ItemIngredients.objects.create(
                ingredient_name="tomate rouge",
                quantity=20,
                unit_price=1000,
                ingredient_id=Ingredient.objects.create(
                    name="oignoin",
                    description="une très bonne sauce",
                    unit_price=100,
                    measure_unit="kg",).id
            ))

    def test_create_inventories(self):
        response = self.client.post(
            self.inventories_url,
            json.dumps({
                "comment": "Test de fonctionnement 2",
                "statut": "CREATED",
                "itemingredients_set": [{
                    "ingredient_name": "tomate",
                    "quantity": 200,
                    "unit_price": 1,
                    "ingredient_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_inventories(self):
        response = self.client.put(
            self.inventories_url+f'{self.inventories.id}/',
            json.dumps({
                "comment": "Test de fonctionnement 2",
                "statut": "CREATED",
                "itemingredients_set": [{
                    "ingredient_name": "tomate",
                    "quantity": 200,
                    "unit_price": 1,
                    "ingredient_id": 1,
                }],
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_inventories(self):
        response = self.client.patch(
            self.inventories_url+f'{self.inventories.id}/',
            json.dumps({
                "statut": "SUBMITTED",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["statut"], "SUBMITTED")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_summary_inventories(self):
        response = self.client.get(
            self.inventories_url +
            f'summary/?start_date=2022-05-13T00:00TZ&ingredient_ids={json.dumps([1,2])}',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_inventories(self):
        response = self.client.get(
            self.inventories_url+f'{self.inventories.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_inventories(self):
        response = self.client.get(
            self.inventories_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_inventories(self):
        response = self.client.delete(
            self.inventories_url+f'{self.inventories.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_inventories_by_wrong_user(self):
        response = self.client.delete(
            self.inventories_url+f'{self.inventories.id}/',
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

        self.inventories_created = Inventories.objects.create(
            comment="Test de fonctionnement",
            statut="CREATED")

        self.inventories_submitted = Inventories.objects.create(
            comment="Test de fonctionnement",
            statut="SUBMITTED")
        ItemIngredients.objects.create(
            ingredient_name="tomate rouge",
            quantity=5,
            unit_price=500,
            inventory=self.inventories_submitted,
            ingredient_id=Ingredient.objects.create(
                description="De la viande de boeuf en kg",
                name="Viande de boeuf",
                unit_price=3500,
                measure_unit="kg",
                group="MEET",
            ).id
        )

        self.validation_url_inventories_created = reverse(
            'validations_inventories', args=[self.inventories_created.id])

        self.validation_url_inventories_submitted = reverse(
            'validations_inventories', args=[self.inventories_submitted.id])

    def test_add_validation(self):
        """ create validation for inventories """
        response = self.client.post(
            self.validation_url_inventories_submitted,
            json.dumps({
                "statut": True,
                "comment": "everything is ok",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_validation_rejected(self):
        """ create validation for inventories """
        response = self.client.post(
            self.validation_url_inventories_submitted,
            json.dumps({
                "statut": False,
                "comment": "the quantity is not good",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_validation_with_wrong_role(self):
        response = self.client.post(
            self.validation_url_inventories_submitted,
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
            self.validation_url_inventories_created,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
