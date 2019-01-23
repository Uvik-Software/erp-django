from django.contrib.auth.hashers import make_password
from django.test import TestCase

from apps.core.models import Developer, User, Manager, Owner, BankInfo

import datetime

from unittest.mock import patch
''' unittest.mock don't work in this testing, because of setUpTestData 
(you must erase creation of Developer from setUpTestData and create 
Developer object in certain test methods)'''


DATE = datetime.datetime.now()


class TestCreateUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        # developer_user = User.objects.create(username="uvik_dev", password=make_password("some_password"),
        #                                      user_type="DEVELOPER", email="some@some.com", last_name="Doe",
        #                                      first_name="John")
        #
        # manager_user = User.objects.create(username="uvik_man",
        #                                    password=make_password("some_password"), user_type="MANAGER")

        bank_info_owner = BankInfo.objects.create(bank_name="PAT Privatbank",
                                                  bank_account_number="3244224242121",
                                                  bank_address="111111, Ukraine, Chernivetska obl., "
                                                               "m. Chernivtsi, vul. Kupsa, 44",
                                                  bank_code="345098")

        bank_info_dev = BankInfo.objects.create(bank_name="PAT VSbank",
                                                bank_account_number="68787797565656",
                                                bank_address="111111, Ukraine, Chernivetska obl., "
                                                             "m. Chernivtsi, vul. Kino, 66",
                                                bank_code="235467")

        # cls.admin = User.objects.create(username='admin', password='admin', is_staff=True)

        owner_rel_to_dev = Owner.objects.create(
            first_name="name_owner",
            last_name="surname_owner",
            father_name="some_fname",
            address="100 Main Street, Nowhere city",
            tax_number="0987654321",
            num_contract_with_dev="14/9",
            date_contract_with_dev=DATE - datetime.timedelta(days=365),
            bank_info=bank_info_owner,
        )

        cls.dev = Developer.objects.create(
            username="uvik_dev", password=make_password("some_password"),
            type="DEVELOPER",
            first_name="John",
            last_name="Doe",
            father_name="Joseph",
            email="some@some.com",
            address="65 Main Street, Nowhere city",
            tax_number="123456789",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=50),
            monthly_salary=1000,
            owner=owner_rel_to_dev,
            bank_info=bank_info_dev,
        )

        cls.man = Manager.objects.create(
            username="uvik_man", password=make_password("some_password"),
            type="MANAGER",
            first_name="some_name",
            last_name="some_surname",
            email="manager_email@uvik.net",
            position="manager",
            address="some_address",
            company_name="UVIK", is_staff=True
        )

    def setUp(self):
        self.dev.refresh_from_db()
        self.man.refresh_from_db()

    def test_create_user_unauthorized(self):
        response_from_get = self.client.get('/users/')

        response_from_post = self.client.post('/users/', {'user_name': 'User_dev', 'password': 'user_password',
                                                          'user_role': 'DEVELOPER', 'first_name': 'DEV_0',
                                                          'last_name': 'Familia_0', 'father_name': 'F_name',
                                                          'email': 'ome@ome.com', 'address': '45 Main Street, '
                                                                                             'Nowhere city',
                                                          'tax_number': '56756565656', 'hourly_rate': 15,
                                                          'birthday_date': '1998-10-20', 'monthly_salary': 1500,
                                                          'owner_id': 1, 'bank_name': 'PAT VSbank',
                                                          'bank_account_number': '68787797565656',
                                                          'bank_address': '111111, Ukraine, Chernivetska obl., '
                                                                          'm. Chernivtsi, vul. Kino, 66',
                                                          'bank_code': '235467'})

        self.assertEqual(response_from_get.status_code, 401)
        self.assertEqual(response_from_post.status_code, 401)

    def test_create_user_authorized_without_perms(self):
        user = self.dev
        login = self.client.login(username=user.username, password="some_password")
        response_from_get = self.client.get('/users/')

        response_from_post = self.client.post('/users/', {'user_name': 'User_dev', 'password': 'user_password',
                                                          'user_role': 'DEVELOPER', 'first_name': 'DEV_0',
                                                          'last_name': 'Familia_0', 'father_name': 'F_name',
                                                          'email': 'ome@ome.com', 'address': '45 Main Street, '
                                                                                             'Nowhere city',
                                                          'tax_number': '56756565656', 'hourly_rate': 15,
                                                          'birthday_date': '1998-10-20', 'monthly_salary': 1500,
                                                          'owner_id': 1, 'bank_name': 'PAT VSbank',
                                                          'bank_account_number': '68787797565656',
                                                          'bank_address': '111111, Ukraine, Chernivetska obl., '
                                                                          'm. Chernivtsi, vul. Kino, 66',
                                                          'bank_code': '235467'})

        self.assertEqual(response_from_get.status_code, 403)
        self.assertEqual(response_from_post.status_code, 403)

    def test_get_all_users_with_perms(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.get('/users/')
        resp_json = response.json()
        dev_user = User.objects.get(id=resp_json["data"][1]["id"])
        man_user = User.objects.get(id=resp_json["data"][0]["id"])
        self.assertEqual(dev_user.username, 'uvik_dev')
        self.assertEqual(man_user.username, 'uvik_man')
        self.assertEqual(dev_user.first_name, 'John')
        self.assertEqual(man_user.first_name, 'some_name')
        self.assertEqual(response.status_code, 200)

    def test_get_specific_user_with_perms(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        response_1 = self.client.get('/users/?id=1')
        response_2 = self.client.get('/users/?id=2')
        resp_1_json = response_1.json()
        resp_2_json = response_2.json()
        dev_user = User.objects.get(id=resp_1_json["data"]["id"])
        man_user = User.objects.get(id=resp_2_json["data"]["id"])
        self.assertEqual(dev_user.username, 'uvik_dev')
        self.assertEqual(man_user.username, 'uvik_man')
        self.assertEqual(dev_user.first_name, 'John')
        self.assertEqual(man_user.first_name, 'some_name')
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)

    @patch('core.signals.create_g_calendar_event')
    def test_post_user_manager(self, create_g_calendar_event_mock):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        try:
            response_1 = self.client.post('/users/', {'user_name': '', 'password': '', 'user_role': 'MANAGER',
                                                      'first_name': 'MAN_1', 'last_name': 'Familia_1',
                                                      'email': 's@s.com', 'position': 'marketing manager',
                                                      'address': 'some_address', 'company_name': 'UVIK'})
        except (Manager.DoesNotExist, User.DoesNotExist):
            pass
        else:
            self.assertEqual(len(Manager.objects.all()), 1)
            self.assertEqual(len(User.objects.all()), 2)
            self.assertEqual(response_1.status_code, 200)

        create_g_calendar_event_mock.return_value = 'Created event in google calendar'
        response_2 = self.client.post('/users/', {'user_name': 'User_man', 'password': 'user_password',
                                                  'user_role': 'MANAGER', 'first_name': 'MAN_2',
                                                  'last_name': 'Familia_2', 'email': 'som@som.com',
                                                  'position': 'marketing manager', 'address': 'some_address',
                                                  'company_name': 'UVIK'})

        user_man = Manager.objects.get(username='User_man')
        man_user = User.objects.get(username='User_man')

        self.assertEqual(user_man.username, 'User_man')
        self.assertEqual(user_man.type, 'MANAGER')
        self.assertEqual(man_user.last_name, 'Familia_2')
        self.assertEqual(man_user.first_name, 'MAN_2')
        self.assertEqual(response_2.status_code, 201)


    # Need to add logic for creating bank info with creating developer
    # @patch('core.signals.create_g_calendar_event')
    # def test_post_user_developer(self, create_g_calendar_event_mock):
    #     user = self.man
    #     login = self.client.login(username=user.username, password="some_password")
    #     try:
    #         response_1 = self.client.post('/users/', {'user_name': '', 'password': '', 'user_role': 'DEVELOPER',
    #                                                   'first_name': 'DEV_1', 'last_name': 'Familia_1',
    #                                                   'father_name': 'F_name', 'email': 'ome@ome.com',
    #                                                   'address': '45 Main Street, Nowhere city',
    #                                                   'tax_number': '56756565656', 'hourly_rate': 15,
    #                                                   'birthday_date': '1998-10-20', 'monthly_salary': 1500,
    #                                                   'owner_id': 1, 'bank_name': 'PAT VSbank',
    #                                                   'bank_account_number': '68787797565656',
    #                                                   'bank_address': '111111, Ukraine, Chernivetska obl., '
    #                                                                   'm. Chernivtsi, vul. Kino, 66',
    #                                                   'bank_code': '235467'})
    #     except (Developer.DoesNotExist, User.DoesNotExist):
    #         pass
    #     else:
    #         self.assertEqual(len(Developer.objects.all()), 1)
    #         self.assertEqual(len(User.objects.all()), 2)
    #         self.assertEqual(response_1.status_code, 200)
    #
    #     create_g_calendar_event_mock.return_value = 'Created event in google calendar'
    #     response_2 = self.client.post('/users/', {'user_name': 'User_dev', 'password': 'user_password',
    #                                               'user_role': 'DEVELOPER', 'first_name': 'DEV_2',
    #                                               'last_name': 'Familia_2', 'father_name': 'F_name',
    #                                               'email': 'ome@ome.com', 'address': '45 Main Street, Nowhere city',
    #                                               'tax_number': '56756565656', 'hourly_rate': 15,
    #                                               'birthday_date': '1998-10-20', 'monthly_salary': 1500,
    #                                               'owner_id': 1, 'bank_name': 'PAT VSbank',
    #                                               'bank_account_number': '68787797565656',
    #                                               'bank_address': '111111, Ukraine, Chernivetska obl., '
    #                                                               'm. Chernivtsi, vul. Kino, 66',
    #                                               'bank_code': '235467'})
    #
    #     user_dev = Developer.objects.get(username='User_dev')
    #     dev_user = User.objects.get(username='User_dev')
    #     bank_info = BankInfo.objects.get(developer__first_name='DEV_2')
    #
    #     self.assertEqual(user_dev.username, 'User_dev')
    #     self.assertEqual(user_dev.type, 'DEVELOPER')
    #     self.assertEqual(dev_user.last_name, 'Familia_2')
    #     self.assertEqual(dev_user.first_name, 'DEV_2')
    #     self.assertEqual(bank_info.developer.last_name, 'Familia_2')
    #     self.assertEqual(bank_info.developer.first_name, 'DEV_2')
    #     self.assertEqual(response_2.status_code, 201)

    def test_put_user_manager(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        resp_put = self.client.put('/users/', {'id': user.id, 'user_name': 'User_man',
                                               'password': 'user_password', 'user_role': 'MANAGER',
                                               'first_name': 'MAN_2', 'last_name': 'Familia_2', 'email': 'som@som.com',
                                               'position': 'marketing manager', 'address': 'some_address',
                                               'company_name': 'UVIK'},
                                   content_type='application/json')

        user_from_put = User.objects.get(id=user.id)

        self.assertEqual(user_from_put.username, 'User_man')
        self.assertEqual(user_from_put.first_name, 'MAN_2')
        self.assertEqual(resp_put.status_code, 200)

    def test_put_user_developer(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        get_dev = self.client.get('/users/?id=1')
        get_dev_json = get_dev.json()
        resp_put = self.client.put('/users/', {'id': get_dev_json['data']['id'], 'user_name': 'User_dev',
                                               'password': 'user_password', 'user_role': 'DEVELOPER',
                                               'first_name': 'DEV_2', 'last_name': 'Familia_2', 'father_name': 'F_name',
                                               'email': 'ome@ome.com', 'address': '45 Main Street, Nowhere city',
                                               'tax_number': '56756565656', 'hourly_rate': 15,
                                               'birthday_date': '1998-10-20', 'monthly_salary': 1500,
                                               'owner_id': 1, 'bank_name': 'PAT VSbank',
                                               'bank_account_number': '68787797565656',
                                               'bank_address': '111111, Ukraine, Chernivetska obl., '
                                                               'm. Chernivtsi, vul. Kino, 66',
                                               'bank_code': '235467'},
                                   content_type='application/json')

        user_from_put = User.objects.get(id=get_dev_json['data']['id'])

        self.assertEqual(get_dev_json['data']['username'], 'uvik_dev')
        self.assertEqual(user_from_put.username, 'User_dev')
        self.assertEqual(user_from_put.first_name, 'DEV_2')
        self.assertEqual(resp_put.status_code, 200)

    def test_put_user_without_id(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        resp_put = self.client.put('/users/', {'user_name': 'User_man', 'password': 'user_password',
                                               'user_role': 'MANAGER', 'first_name': 'MAN_2', 'last_name': 'Familia_2',
                                               'email': 'som@som.com', 'position': 'marketing manager',
                                               'address': 'some_address', 'company_name': 'UVIK'},
                                   content_type='application/json')

        resp_put_json = resp_put.json()
        user_man = User.objects.get(id=user.id)
        user_dev = User.objects.get(id=self.dev.id)

        self.assertEqual(resp_put_json['message'], "You must point 'User ID'")
        self.assertEqual(user_man.username, 'uvik_man')
        self.assertEqual(user_dev.username, 'uvik_dev')
        self.assertEqual(user_man.first_name, 'some_name')
        self.assertEqual(user_dev.first_name, 'John')

    def test_delete_user(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")

        get_dev = self.client.get('/users/?id=1')

        get_dev_json = get_dev.json()
        print(get_dev_json)

        resp_del_dev = self.client.delete('/users/', {'id': get_dev_json['data']['id']}, content_type='application/json')
        resp_del_man = self.client.delete('/users/', {'id': user.id}, content_type='application/json')

        self.assertEqual(len(User.objects.all()), 0)
        self.assertEqual(resp_del_dev.status_code, 204)
        self.assertEqual(resp_del_man.status_code, 204)

    def test_delete_user_without_id(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")

        resp_del = self.client.delete('/users/', {}, content_type='application/json')
        resp_del_json = resp_del.json()

        self.assertEqual(resp_del_json['message'], 'Please provide user id')
        self.assertEqual(len(User.objects.all()), 2)
        self.assertEqual(resp_del.status_code, 200)
