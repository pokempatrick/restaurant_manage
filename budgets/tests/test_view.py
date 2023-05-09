from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from django.utils import timezone
from authentification.models import User
from budgets.models import Budgets, DishBudgets
from dishes.models import ItemIngredients, Dish, Ingredient
from datetime import timedelta, datetime
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder


class TestBudgetsViews(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.budgets_url = reverse('budgets-list')
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

        self.budget = Budgets.objects.create(
            description="Test de fonctionnement",
            statut="CREATED")
        self.budget_submitted = Budgets.objects.create(
            description="Test de fonctionnement",
            statut="SUBMITTED")
        self.dish_budget = self.budget.dishbudgets_set.create(
            dish_name="sauce tomate",
            dish_quantity=20,
        )

    def test_create_budget(self):
        response = self.client.post(
            self.budgets_url,
            json.dumps({
                "description": "Test de fonctionnement 2",
                "statut": "CREATED",
                "end_date": datetime.now(),
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_budget_with_bad_role(self):
        response = self.client.post(
            self.budgets_url,
            json.dumps({
                "description": "Test de fonctionnement 2",
                "statut": "VALIDATED",
                "end_date": datetime.now()
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_budget(self):
        response = self.client.patch(
            self.budgets_url+f'{self.budget.id}/',
            json.dumps({
                "description": "Test de fonctionnement 2",
                "statut": "CREATED",
                "start_date": datetime.now(),
                "end_date": datetime.now()+timedelta(days=5),
            }, cls=DjangoJSONEncoder),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.data["statut"], "CREATED")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_budget_statut(self):
        response = self.client.patch(
            self.budgets_url+f'{self.budget.id}/',
            json.dumps({
                "statut": "VALIDATED",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.data["statut"], "VALIDATED")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_budget(self):
        response = self.client.get(
            self.budgets_url+f'{self.budget.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_budgets(self):
        response = self.client.get(
            self.budgets_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_budget(self):
        response = self.client.delete(
            self.budgets_url+f'{self.budget.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_non_editable_budget(self):
        response = self.client.patch(
            self.budgets_url+f'{self.budget_submitted.id}/',
            json.dumps({
                "statut": "VALIDATED",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestDishBudgetsView(TestCase):

    @classmethod
    def setUp(self):

        self.client = Client()
        self.dishbudget_url = reverse('dish_budget-list')
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

        self.item_ingredient = ItemIngredients.objects.create(
            ingredient_name="tomate rouge",
            quantity=250,
            unit_price=1,
        )
        self.budget = Budgets.objects.create(
            description="Test de fonctionnement",
            statut="CREATED")

        self.dish_budget = DishBudgets.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            budget=self.budget
        )

        self.dish_budget.itemingredients_set.add(self.item_ingredient)
        self.dish_budget_with_non_editatble_budget = DishBudgets.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            budget=Budgets.objects.create(
                description="Test de fonctionnement",
                statut="SUBMITTED")
        )

    def test_add_dishbudgets(self):
        response = self.client.post(
            self.dishbudget_url,
            json.dumps({
                "dish_name": "sauce tomate",
                "dish_quantity": 20,
                "itemingredients_set": [{
                    "ingredient_name": "tomate",
                    "quantity": 200,
                    "unit_price": 1,
                    "ingredient_id": 1,
                }],
                "budget": self.budget.id,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data['dish_name'], "sauce tomate")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_dishbudget(self):
        response = self.client.get(
            self.dishbudget_url+f'{self.dish_budget.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_dishbudgets(self):
        response = self.client.get(
            self.dishbudget_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_dishbudget(self):
        response = self.client.put(
            self.dishbudget_url+f'{self.dish_budget.id}/',
            json.dumps({
                "dish_name": "sauce tomate",
                "dish_quantity": 30,
                "itemingredients_set": [{
                    "id": 1,
                    "ingredient_name": "haricot",
                    "ingredient_id": 1,
                    "quantity": 200,
                    "unit_price": 5,
                }, {
                    "ingredient_name": "tomate",
                    "quantity": 20,
                    "ingredient_id": 2,
                    "unit_price": 10,
                },],
                "budget": self.budget.id,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_dishbudget(self):
        response = self.client.patch(
            self.dishbudget_url+f'{self.dish_budget.id}/',
            json.dumps({
                "dish_quantity": 10,
                "itemingredients_set": [{
                    "id": 1,
                    "ingredient_id": 1,
                    "quantity": 200,
                    "unit_price": 5,
                }, {
                    "quantity": 20,
                    "ingredient_id": 2,
                    "unit_price": 10,
                },],
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.data["dish_quantity"], 10)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_dishbudget(self):
        response = self.client.delete(
            self.dishbudget_url+f'{self.dish_budget.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_dishbudget_with_non_editable_budget(self):
        response = self.client.patch(
            self.dishbudget_url +
            f'{self.dish_budget_with_non_editatble_budget.id}/',
            json.dumps({
                "dish_quantity": 158,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


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

        self.budget_created = Budgets.objects.create(
            description="Test de fonctionnement",
            statut="CREATED")

        self.budget_submitted = Budgets.objects.create(
            description="Test de fonctionnement",
            statut="SUBMITTED")
        DishBudgets.objects.create(
            dish_name="sauce tomate",
            dish_quantity=20,
            budget=self.budget_submitted
        ).itemingredients_set.add(
            ItemIngredients.objects.create(
                ingredient_name="tomate rouge",
                quantity=250,
                unit_price=1,
            ))

        self.validation_url_budget_created = reverse(
            'validations_budget', args=[self.budget_created.id])

        self.validation_url_budget_submitted = reverse(
            'validations_budget', args=[self.budget_submitted.id])

    def test_add_validation(self):
        """ create validation for budget """
        response = self.client.post(
            self.validation_url_budget_submitted,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
                "assign_user": self.user_technician.id,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_validation_with_wrong_role(self):
        response = self.client.post(
            self.validation_url_budget_submitted,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
                "assign_user": self.user_technician.id,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_validation_with_wrong_initial_statut(self):
        """ reject validation since the statut is not submitted """
        response = self.client.post(
            self.validation_url_budget_created,
            json.dumps({
                "statut": False,
                "comment": "we don't have enough money",
                "assign_user": self.user_manager.id,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
