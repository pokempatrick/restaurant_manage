from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from authentification.models import User
from budgets.models import Budgets, DishBudgets
from dishes.models import ItemIngredients
from procurement.models import Procurements
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


class TestProcurementViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.budget_url = reverse('budgets-list')
        self.procurement_url = reverse('procurements-list')
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

        # create a budget

        self.item_ingredient = ItemIngredients.objects.create(
            ingredient_name="tomate rouge",
            quantity=250,
            unit_price=1,
        )
        self.budget = Budgets.objects.create(
            description="Test de fonctionnement",
            statut="ACQUISITION")

        self.dish_budget = DishBudgets.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            budget=self.budget
        )
        self.dish_budget.itemingredients_set.add(self.item_ingredient)

        self.procurement = Procurements.objects.create(
            budget=Budgets.objects.create(
                description="Test de fonctionnement 2",
                statut="ACQUISITION"),
            comment="everything is ok")

    def test_create_procurement(self):
        response = self.client.post(
            self.budget_url+f'{self.budget.id}/procurements/',
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

    def test_update_procurement(self):
        response = self.client.put(
            self.procurement_url+f'{self.procurement.id}/',
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

    def test_partial_update_procurement(self):
        response = self.client.patch(
            self.procurement_url+f'{self.procurement.id}/',
            json.dumps({
                "statut": "SUBMITTED",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["statut"], "SUBMITTED")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_procurement(self):
        response = self.client.get(
            self.procurement_url+f'{self.procurement.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_procurement(self):
        response = self.client.get(
            self.procurement_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_procurement(self):
        response = self.client.delete(
            self.procurement_url+f'{self.procurement.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ValidationsView(TestCase):

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

        self.procurement_created = Procurements.objects.create(
            budget=Budgets.objects.create(
                description="Test de fonctionnement 2",
                statut="ACQUISITION"),
            comment="Test de fonctionnement",
            statut="CREATED")

        self.procurement_submitted = Procurements.objects.create(
            budget=Budgets.objects.create(
                description="Test de fonctionnement 2",
                statut="ACQUISITION"),
            comment="Test de fonctionnement",
            statut="SUBMITTED")
        ItemIngredients.objects.create(
            ingredient_name="tomate rouge",
            quantity=5,
            unit_price=500,
            procurement=self.procurement_submitted
        )

        self.validation_url_procurement_created = reverse(
            'validations_procurements', args=[self.procurement_created.id])

        self.validation_url_procurement_submitted = reverse(
            'validations_procurements', args=[self.procurement_submitted.id])

    def test_add_validation(self):
        """ create validation for procurement """
        response = self.client.post(
            self.validation_url_procurement_submitted,
            json.dumps({
                "statut": True,
                "comment": "everything is ok",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_validation_with_wrong_role(self):
        response = self.client.post(
            self.validation_url_procurement_submitted,
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
            self.validation_url_procurement_created,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
