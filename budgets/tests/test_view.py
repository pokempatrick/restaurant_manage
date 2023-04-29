from django.test import TestCase, Client
from django.urls import reverse
import json
from rest_framework import status
from django.utils import timezone
from authentification.models import User
from budgets.models import Budgets
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

        # create another budget
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
        response = self.client.put(
            self.budgets_url+f'{self.budget.id}/',
            json.dumps({
                "description": "Test de fonctionnement 2",
                "statut": "VALIDATED",
                "start_date": datetime.now(),
                "end_date": datetime.now()+timedelta(days=5),
            }, cls=DjangoJSONEncoder),
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
        self.assertTrue(response.data['count'] == 1)

    def test_delete_budget(self):
        response = self.client.delete(
            self.budgets_url+f'{self.budget.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user_cooker.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
