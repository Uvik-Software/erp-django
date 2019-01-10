from django.contrib.auth.hashers import make_password
from django.test import TestCase

from core.models import Developer, User, Manager, Owner, BankInfo

import datetime


DATE = datetime.datetime.now()


class TestCreateUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        developer_user_1 = User.objects.create(username="uvik_dev_1", password=make_password("some_password"),
                                               user_type="DEVELOPER", email="some1@some1.com", last_name="Familia_1",
                                               first_name="DEV_1")

        developer_user_2 = User.objects.create(username="uvik_dev_2", password=make_password("some_password"),
                                               user_type="DEVELOPER", email="some2@some2.com", last_name="Familia_2",
                                               first_name="DEV_2")

        manager_user = User.objects.create(username="uvik_man",
                                           password=make_password("some_password"), user_type="MANAGER")

        bank_info_owner = BankInfo.objects.create(bank_name="PAT UkrSibBank")

        bank_info_dev_1 = BankInfo.objects.create(bank_name="PAT VSbank", bank_account_number="68787797565656",
                                                  bank_address="111111, Ukraine, Chernivetska obl., "
                                                               "m. Chernivtsi, vul. Kino, 66",
                                                  bank_code="235467")

        bank_info_dev_2 = BankInfo.objects.create(bank_name="PAT Privatbank", bank_account_number="3244224242121",
                                                  bank_address="111111, Ukraine, Chernivetska obl., "
                                                               "m. Chernivtsi, vul. Kupsa, 44",
                                                  bank_code="345098")

        owner_rel_to_dev = Owner.objects.create(
            name="name_owner",
            surname="surname_owner",
            father_name="some_fname",
            address="100 Main Street, Nowhere city",
            tax_number="00987654321",
            num_contract_with_dev="14/9",
            date_contract_with_dev=DATE - datetime.timedelta(days=365),
            bank_info=bank_info_owner,
            user_create=manager_user
        )

        cls.dev_1 = Developer.objects.create(
            name="DEV_1",
            surname="Familia_1",
            father_name="Fname_1",
            email="some1@some1.com",
            address="65 Main Street, Nowhere city",
            tax_number="123456789",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=30),
            monthly_salary=1000,
            owner=owner_rel_to_dev,
            bank_info=bank_info_dev_1,
            user=developer_user_1
        )

        cls.dev_2 = Developer.objects.create(
            name="DEV_2",
            surname="Familia_2",
            father_name="Fname_2",
            email="some2@some2.com",
            address="200 Main Street, Nowhere city",
            tax_number="987654321",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=50),
            monthly_salary=1000,
            owner=owner_rel_to_dev,
            bank_info=bank_info_dev_2,
            user=developer_user_2
        )

        cls.man = Manager.objects.create(
            name="some_name",
            surname="some_surname",
            email="manager_email@uvik.net",
            position="manager",
            address="some_address",
            company_name="UVIK",
            user=manager_user
        )

    def test_get_bank_info_unauthorized(self):
        response_from_get = self.client.get('/bank_info/')

        response_from_post = self.client.post('/bank_info/', {'user_name': 'User_dev', 'password': 'user_password',
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

    def test_get_bank_info_authorized_without_perms(self):
        fake_user = User.objects.create(username="fake_user", password=make_password("password"), user_type="CLIENT")

        fake_dev = Developer.objects.create(
            name="John",
            surname="Smith",
            email="js@js.com",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=50),
            monthly_salary=1000,
            user=fake_user
        )

        login = self.client.login(username=fake_user.username, password="password")
        response_from_get = self.client.get('/bank_info/')

        response_from_post = self.client.post('/bank_info/', {'user_name': 'User_dev', 'password': 'user_password',
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

        resp_from_get_json = response_from_get.json()
        resp_from_post_json = response_from_post.json()

        self.assertEqual(resp_from_get_json['detail'], 'You do not have permission to perform this action.')
        self.assertEqual(resp_from_post_json['detail'], 'You do not have permission to perform this action.')
        self.assertEqual(response_from_get.status_code, 403)
        self.assertEqual(response_from_post.status_code, 403)

    def test_get_all_bank_info_with_man_perms(self):
        user = self.man
        login = self.client.login(username=user.user.username, password="some_password")
        response = self.client.get('/bank_info/')
        resp_json = response.json()

        self.assertEqual(resp_json['data'][0]['dev_name'], 'DEV_1')
        self.assertEqual(resp_json['data'][0]['bank_name'], 'PAT VSbank')
        self.assertEqual(resp_json['data'][1]['dev_name'], 'DEV_2')
        self.assertEqual(resp_json['data'][1]['bank_name'], 'PAT Privatbank')
        self.assertEqual(response.status_code, 200)

    def test_get_all_bank_info_with_dev_perms(self):
        user = self.dev_1
        login = self.client.login(username=user.user.username, password="some_password")
        response = self.client.get('/bank_info/')
        resp_json = response.json()

        self.assertEqual(resp_json['message'], "You can't see banking information of other people. "
                                               "Please provide your own id.")
        self.assertEqual(response.status_code, 200)

    def test_get_specific_bank_info_with_man_perms(self):
        user = self.man
        login = self.client.login(username=user.user.username, password="some_password")
        response_1 = self.client.get('/bank_info/?id=1')
        response_2 = self.client.get('/bank_info/?id=2')
        resp_1_json = response_1.json()
        resp_2_json = response_2.json()

        self.assertEqual(resp_1_json["data"]["dev_name"], 'DEV_1')
        self.assertEqual(resp_1_json["data"]["bank_name"], 'PAT VSbank')
        self.assertEqual(resp_2_json["data"]["dev_name"], 'DEV_2')
        self.assertEqual(resp_2_json["data"]["bank_name"], 'PAT Privatbank')
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)

    def test_get_specific_bank_info_with_dev_perms(self):
        user = self.dev_1
        login = self.client.login(username=user.user.username, password="some_password")
        response_1 = self.client.get('/bank_info/?id=1')
        response_2 = self.client.get('/bank_info/?id=2')
        resp_1_json = response_1.json()
        resp_2_json = response_2.json()

        self.assertEqual(resp_1_json["data"]["dev_name"], 'DEV_1')
        self.assertEqual(resp_1_json["data"]["bank_name"], 'PAT VSbank')
        self.assertEqual(resp_2_json["message"], 'You are allowed to see only your banking information')
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)