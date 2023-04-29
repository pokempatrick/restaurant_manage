from django.test import TestCase, Client
from django.urls import reverse
import json
import jwt
from django.contrib.auth.hashers import make_password
from rest_framework import status
from authentification.models import User
from datetime import datetime, timedelta
from django.conf import settings


class TestViews(TestCase):
    @classmethod
    def setUp(self):

        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.user_url = reverse('user')
        self.email_sign_url = reverse('email_sign')
        self.email_code_url = reverse('email_code')

        # creation d'un utilisateur
        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password')

        # generate recover token
        self.recover_token = jwt.encode(
            {
                'username': self.user.username,
                'email': self.user.email,
                'user_id': self.user.id,
                'code': make_password("1234"),
                'exp': datetime.utcnow()+timedelta(hours=1)
            }, settings.SECRET_KEY2, algorithm='HS256')

    def test_registration(self):
        response = self.client.post(
            self.register_url,
            json.dumps({
                "username": "johndoes",
                "email": "jonhdoes@yahoo.fr",
                "password": "casho 15",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_good_credential(self):
        response = self.client.post(
            self.login_url,
            json.dumps({
                "email": "cyretruly@gmail.com",
                "password": "1234password",
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_bad_credential(self):
        response = self.client.post(
            self.login_url,
            json.dumps({
                "email": "cyretruly@gmail.com",
                "password": "123password",
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sign_in_email_with_existing_email(self):
        response = self.client.post(
            self.email_sign_url,
            json.dumps({
                "email": "cyretruly@gmail.com",
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_in_email_with_non_existing_email(self):
        response = self.client.post(
            self.email_sign_url,
            json.dumps({
                "email": "cyretruely@gmail.com",
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_code_email_with_bad_code(self):

        response = self.client.post(
            self.email_code_url,
            json.dumps({"code": 1245, }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.recover_token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_code_email_checking(self):

        response = self.client.post(
            self.email_code_url,
            json.dumps({"code": 1234, }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.recover_token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestUserViews(TestCase):
    @classmethod
    def setUp(self):

        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.users_url = reverse('users-list')
        # creation d'un utilisateur
        self.user = User.objects.create(
            username='cyrce',
            email='cyretruly@gmail.com',
            first_name="john",
            last_name="does",
            password='1234password',
            role_name="ROLE_MANAGER"
        )

        # create another user
        self.user2 = User.objects.create(
            username='cyrce12',
            email='cyretruly12@gmail.com',
            first_name="john1",
            last_name="does1",
            password='12343password',
            role_name="ROLE_ANONYME"
        )

    def test_create_user(self):
        response = self.client.post(
            self.users_url,
            json.dumps({
                "username": "johndoes",
                "email": "jonhdoes@yahoo.fr",
                "password": "casho 15",
                "first_name": "john",
                "last_name": "does",
                "role_name": "ROLE_ANONYME"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        response = self.client.put(
            self.users_url+f'{self.user2.id}/',
            json.dumps({
                "username": "jeanedoes",
                "email": "jonhdoes@yahoo.fr",
                "password": "casho 15",
                "first_name": "jeane",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_by_manager_role(self):
        response = self.client.put(
            self.users_url+f'{self.user2.id}/',
            json.dumps({
                "role_name": "ROLE_ADMIN"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user(self):
        response = self.client.get(
            self.users_url+f'{self.user2.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users(self):
        response = self.client.get(
            self.users_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['count'] == 2)

    def test_delete_user(self):
        response = self.client.delete(
            self.users_url+f'{self.user2.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_his_own_password(self):
        response = self.client.put(
            self.users_url+f'{self.user2.id}/set_password/',
            json.dumps({
                "password": "123456"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user2.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_somebody_else_password(self):
        response = self.client.put(
            self.users_url+f'{self.user2.id}/set_password/',
            json.dumps({
                "password": "123456"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
