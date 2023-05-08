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

    # def test_update_procurement(self):
    #     response = self.client.put(
    #         self.procurement_url+f'{self.procurement.id}/',
    #         json.dumps({
    #             "comment": "Test de fonctionnement 2",
    #             "statut": "CREATED",
    #             "itemingredients_set": [{
    #                 "ingredient_name": "tomate",
    #                 "quantity": 200,
    #                 "unit_price": 1,
    #                 "ingredient_id": 1,
    #             }],
    #         }, cls=DjangoJSONEncoder),
    #         **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
    #         content_type="application/json"
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)


# class ValidationsView(TestCase):

#     @classmethod
#     def setUp(self):

#         self.client = Client()
#         # creation d'un utilisateur
#         self.user_manager = User.objects.create(
#             username='cyrce',
#             email='cyretruly@gmail.com',
#             first_name="john",
#             last_name="does",
#             password='1234password',
#             role_name="ROLE_MANAGER"
#         )
#         self.user_technician = User.objects.create(
#             username='cyrce12',
#             email='cyretruly12@gmail.com',
#             first_name="john1",
#             last_name="does1",
#             password='12343password',
#             role_name="ROLE_TECHNICIAN"
#         )

#         self.budget_created = Budgets.objects.create(
#             description="Test de fonctionnement",
#             statut="CREATED")

#         self.budget_submitted = Budgets.objects.create(
#             description="Test de fonctionnement",
#             statut="SUBMITTED")
#         DishBudgets.objects.create(
#             dish_name="sauce tomate",
#             dish_quantity=20,
#             budget=self.budget_submitted
#         ).itemingredients_set.add(
#             ItemIngredients.objects.create(
#                 ingredient_name="tomate rouge",
#                 quantity=250,
#                 unit_price=1,
#             ))

#         self.validation_url_budget_created = reverse(
#             'validations_budget', args=[self.budget_created.id])

#         self.validation_url_budget_submitted = reverse(
#             'validations_budget', args=[self.budget_submitted.id])

#     def test_add_validation(self):
#         """ create validation for budget """
#         response = self.client.post(
#             self.validation_url_budget_submitted,
#             json.dumps({
#                 "statut": False,
#                 "comment": "we don't have enough money",
#                 "assign_user": self.user_technician.id,
#             }),
#             **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_add_validation_with_wrong_role(self):
#         response = self.client.post(
#             self.validation_url_budget_submitted,
#             json.dumps({
#                 "statut": False,
#                 "comment": "we don't have enough money",
#                 "assign_user": self.user_technician.id,
#             }),
#             **{'HTTP_AUTHORIZATION': f'Bearer {self.user_technician.token}'},
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def test_add_validation_with_wrong_initial_statut(self):
#         """ reject validation since the statut is not submitted """
#         response = self.client.post(
#             self.validation_url_budget_created,
#             json.dumps({
#                 "statut": False,
#                 "comment": "we don't have enough money",
#                 "assign_user": self.user_manager.id,
#             }),
#             **{'HTTP_AUTHORIZATION': f'Bearer {self.user_manager.token}'},
#             content_type="application/json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
