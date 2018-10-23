from django.contrib.auth.hashers import make_password
from django.test import TestCase

from core.models import Developer, User, Manager

import datetime


DATE = datetime.datetime.now()


class TestCreateUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        developer_user = User.objects.create(username="uvik_dev",
                                             password=make_password("some_password"), user_type="DEVELOPER")
        manager_user = User.objects.create(username="uvik_man",
                                           password=make_password("some_password"), user_type="MANAGER")

        dev = Developer.objects.create(
            name="John",
            surname="Doe",
            email="some@some.com",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=50),
            monthly_salary=1000,
            user=developer_user
        )

        man = Manager.objects.create(
            name="some_name",
            surname="some_surname",
            email="manager_email@uvik.net",
            position="manager",
            address="some_address",
            company_name="UVIK",
            user=manager_user
        )

    def test_create_user_unauthorized(self):
        response = self.client.post('/users/', {'user_name': 'User_dev', 'password': 'user_password',
                                                'user_role': 'DEVELOPER', 'first_name': 'DEV_0',
                                                'last_name': 'Familia_0', 'email': 'ome@ome.com', 'hourly_rate': 15,
                                                'birthday_date': '1998-10-20', 'monthly_salary': 1500})
        self.assertEqual(response.status_code, 401)

    def test_create_user_developer(self):
        user = User.objects.get(username='uvik_dev')
        login = self.client.login(username=user.username, password="some_password")
        try:
            response_1 = self.client.post('/users/', {'user_name': '', 'password': '', 'user_role': 'DEVELOPER',
                                                      'first_name': 'DEV_1', 'last_name': 'Familia_1',
                                                      'email': 'so@so.com', 'hourly_rate': 15,
                                                      'birthday_date': '1999-10-20', 'monthly_salary': 1500})
        except (Developer.DoesNotExist, User.DoesNotExist):
            pass
        else:
            self.assertEqual(len(Developer.objects.all()), 1)
            self.assertEqual(len(User.objects.all()), 2)
            self.assertEqual(response_1.status_code, 200)

        response_2 = self.client.post('/users/', {'user_name': 'User_dev', 'password': 'user_password',
                                                  'user_role': 'DEVELOPER', 'first_name': 'DEV_2',
                                                  'last_name': 'Familia_2', 'email': 'so@so.com', 'hourly_rate': 15,
                                                  'birthday_date': '1998-10-20', 'monthly_salary': 1500})

        user_dev = Developer.objects.get(user__username='User_dev')
        dev_user = User.objects.get(username='User_dev')

        self.assertEqual(user_dev.user.username, 'User_dev')
        self.assertEqual(user_dev.user.user_type, 'DEVELOPER')
        self.assertEqual(dev_user.developer_set.get(surname='Familia_2').surname, 'Familia_2')
        self.assertEqual(dev_user.developer_set.get(name='DEV_2').name, 'DEV_2')
        self.assertEqual(response_2.status_code, 201)

    def test_create_user_manager(self):
        user = User.objects.get(username='uvik_man')
        login = self.client.login(username=user.username, password="some_password")
        try:
            response_1 = self.client.post('/users/', {'user_name': '', 'password': '', 'user_role': 'MANAGER',
                                                      'first_name': 'MAN_1', 'last_name': 'Familia_1',
                                                      'email': 'som@som.com', 'position': 'marketing manager',
                                                      'address': 'some_address', 'company_name': 'UVIK'})
        except (Manager.DoesNotExist, User.DoesNotExist):
            pass
        else:
            self.assertEqual(len(Manager.objects.all()), 1)
            self.assertEqual(len(User.objects.all()), 2)
            self.assertEqual(response_1.status_code, 200)

        response_2 = self.client.post('/users/', {'user_name': 'User_man', 'password': 'user_password',
                                                  'user_role': 'MANAGER', 'first_name': 'MAN_2',
                                                  'last_name': 'Familia_2', 'email': 'som@som.com',
                                                  'position': 'marketing manager', 'address': 'some_address',
                                                  'company_name': 'UVIK'})

        user_man = Manager.objects.get(user__username='User_man')
        man_user = User.objects.get(username='User_man')

        self.assertEqual(user_man.user.username, 'User_man')
        self.assertEqual(user_man.user.user_type, 'MANAGER')
        self.assertEqual(man_user.manager_set.get(surname='Familia_2').surname, 'Familia_2')
        self.assertEqual(man_user.manager_set.get(name='MAN_2').name, 'MAN_2')
        self.assertEqual(response_2.status_code, 201)
