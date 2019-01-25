from django.contrib.auth.hashers import make_password
from django.test import TransactionTestCase

from apps.core.models import Developer, Manager, Owner, BankInfo

import datetime


DATE = datetime.datetime.now()


class TestCreateUser(TransactionTestCase):

    def setUp(self):

        bank_info_owner_1 = BankInfo.objects.create(bank_name="PAT UkrSibBank", bank_account_number="3244224242121",
                                                    bank_address="111111, Ukraine, Chernivetska obl., "
                                                                 "m. Chernivtsi, vul. Kupsa, 44",
                                                    bank_code="345098")

        bank_info_owner_2 = BankInfo.objects.create(bank_name="PAT Privatbank", bank_account_number="6677567567565",
                                                    bank_address="111111, Ukraine, Chernivetska obl., "
                                                                 "m. Chernivtsi, vul. Mupsa, 244",
                                                    bank_code="678543")

        bank_info_dev = BankInfo.objects.create(bank_name="PAT VSbank", bank_account_number="68787797565656",
                                                bank_address="111111, Ukraine, Chernivetska obl., "
                                                             "m. Chernivtsi, vul. Kino, 66",
                                                bank_code="235467")

        self.owner_1 = Owner.objects.create(
            first_name="Owner_1",
            last_name="Surname_1",
            father_name="Fname_1",
            address="100 Main Street, Nowhere city",
            tax_number="123456789",
            num_contract_with_dev="14/9",
            date_contract_with_dev=DATE - datetime.timedelta(days=365),
            bank_info=bank_info_owner_1,
        )

        self.owner_2 = Owner.objects.create(
            first_name="Owner_2",
            last_name="Surname_2",
            father_name="Fname_2",
            address="200 Main Street, Nowhere city",
            tax_number="0987654321",
            num_contract_with_dev="20/9",
            date_contract_with_dev=DATE - datetime.timedelta(days=365),
            bank_info=bank_info_owner_2,
        )

        self.dev = Developer.objects.create(
            username="uvik_dev_1",
            password=make_password("some_password"),
            type="DEVELOPER",
            email="some1@some1.com",
            last_name="Familia_1",
            first_name="DEV_1",
            father_name="Fname_1",
            address="65 Main Street, Nowhere city",
            tax_number="993456789",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=30),
            monthly_salary=1000,
            bank_info=bank_info_dev,
        )

        self.man = Manager.objects.create(
            username="uvik_man",
            password=make_password("some_password"),
            type="MANAGER",
            first_name="some_name",
            last_name="some_surname",
            email="manager_email@uvik.net",
            position="manager",
            address="some_address",
            company_name="UVIK",
        )

    def test_get_owner_unauthorized(self):
        response_from_get = self.client.get('/set_owner/')

        response_from_post = self.client.post('/set_owner/', {'name': 'OWNER', 'surname': 'Surname_owner', 'father_name': 'F_name',
                                                              'address': '2000 Main Street, Nowhere city',
                                                              'tax_number': '56756565656', 'contract_num': '100/9',
                                                              'contract_date': '2018-01-01', 'bank_name': 'PAT VSbank',
                                                              'bank_account_number': '8675767676767',
                                                              'bank_address': '111111, Ukraine, Chernivetska obl., '
                                                                              'm. Chernivtsi, vul. Kino, 666',
                                                              'bank_code': '235467'})

        self.assertEqual(response_from_get.status_code, 401)
        self.assertEqual(response_from_post.status_code, 401)

    def test_get_owner_authorized_without_perms(self):
        user = self.dev
        login = self.client.login(username=user.username, password="some_password")
        response_from_get = self.client.get('/set_owner/')

        response_from_post = self.client.post('/set_owner/', {'first_name': 'OWNER', 'last_name': 'Surname_owner', 'father_name': 'F_name',
                                                              'address': '2000 Main Street, Nowhere city',
                                                              'tax_number': '56756565656', 'contract_num': '100/9',
                                                              'contract_date': '2018-01-01', 'bank_name': 'PAT VSbank',
                                                              'bank_account_number': '8675767676767',
                                                              'bank_address': '111111, Ukraine, Chernivetska obl., '
                                                                              'm. Chernivtsi, vul. Kino, 666',
                                                              'bank_code': '235467'})

        resp_from_get_json = response_from_get.json()
        resp_from_post_json = response_from_post.json()

        self.assertEqual(resp_from_get_json['detail'], 'You do not have permission to perform this action.')
        self.assertEqual(resp_from_post_json['detail'], 'You do not have permission to perform this action.')
        self.assertEqual(response_from_get.status_code, 403)
        self.assertEqual(response_from_post.status_code, 403)

    def test_get_owner_with_perms(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.get('/set_owner/')
        resp_json = response.json()

        self.assertEqual(resp_json['data'][0]['first_name'], 'Owner_1')
        self.assertEqual(resp_json['data'][0]['bank_name'], 'PAT UkrSibBank')
        self.assertEqual(resp_json['data'][1]['first_name'], 'Owner_2')
        self.assertEqual(resp_json['data'][1]['bank_name'], 'PAT Privatbank')
        self.assertEqual(response.status_code, 200)

    def test_get_specific_owner_with_perms(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        response_1 = self.client.get('/set_owner/?id=1')
        response_2 = self.client.get('/set_owner/?id=2')
        resp_1_json = response_1.json()
        resp_2_json = response_2.json()

        self.assertEqual(resp_1_json["data"]["first_name"], 'Owner_1')
        self.assertEqual(resp_1_json["data"]["bank_name"], 'PAT UkrSibBank')
        self.assertEqual(resp_2_json["data"]["first_name"], 'Owner_2')
        self.assertEqual(resp_2_json["data"]["bank_name"], 'PAT Privatbank')
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)

    def test_post_owner_with_perms(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.post('/set_owner/', {'first_name': 'OWNER', 'last_name': 'Surname_owner', 'father_name': 'F_name',
                                                    'address': '2000 Main Street, Nowhere city',
                                                    'tax_number': '56756565656', 'contract_num': '100/9',
                                                    'contract_date': '2018-01-01', 'bank_name': 'PAT VSbank',
                                                    'bank_account_number': '8675767676767',
                                                    'bank_address': '111111, Ukraine, Chernivetska obl., '
                                                                     'm. Chernivtsi, vul. Kino, 666',
                                                    'bank_code': '235467'})

        owner_obj = Owner.objects.get(id=3)

        self.assertEqual(owner_obj.first_name, 'OWNER')
        self.assertEqual(owner_obj.bank_info.bank_account_number, '8675767676767')
        self.assertEqual(len(Owner.objects.all()), 3)
        self.assertEqual(response.status_code, 201)

    def test_post_owner_with_perms_without_some_fields(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.post('/set_owner/', {'first_name': 'OWNER', 'last_name': 'Surname_owner', 'father_name': 'F_name',
                                                    'address': '2000 Main Street, Nowhere city',
                                                    'tax_number': '56756565656', 'contract_num': '100/9',
                                                    'contract_date': '2018-01-01', 'bank_name': '',
                                                    'bank_account_number': '8675767676767',
                                                    'bank_address': '111111, Ukraine, Chernivetska obl., '
                                                                     'm. Chernivtsi, vul. Kino, 666',
                                                    'bank_code': '235467'})

        resp_json = response.json()

        self.assertEqual(resp_json['message'], 'You must fill all fields')
        self.assertEqual(len(Owner.objects.all()), 2)
        self.assertEqual(response.status_code, 200)

    def test_put_owner_with_perms(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        owner = Owner.objects.get(id=1)
        response = self.client.put('/set_owner/', {'id': owner.id, 'first_name': 'SUPER_OWNER', 'bank_name': 'PAT Superbank',
                                                   'bank_account_number': '11111111111111', 'bank_code': '000001'},
                                   content_type='application/json')

        owner_put = Owner.objects.get(id=owner.id)

        self.assertEqual(owner_put.first_name, 'SUPER_OWNER')
        self.assertEqual(owner_put.bank_info.bank_name, 'PAT Superbank')
        self.assertEqual(owner_put.bank_info.bank_account_number, '11111111111111')
        self.assertEqual(len(Owner.objects.all()), 2)
        self.assertEqual(response.status_code, 200)

    def test_put_owner_with_perms_without_id(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.put('/set_owner/', {'first_name': 'SUPER_OWNER', 'bank_name': 'PAT Superbank',
                                                   'bank_account_number': '11111111111111', 'bank_code': '000001'},
                                   content_type='application/json')

        resp_json = response.json()

        self.assertEqual(resp_json['message'], 'You must provide Owner ID')
        self.assertEqual(response.status_code, 200)

    def test_delete_owner_with_perms(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")

        response_del_1 = self.client.delete('/set_owner/', {'id': self.owner_1.id}, content_type='application/json')
        response_del_2 = self.client.delete('/set_owner/', {'id': self.owner_2.id}, content_type='application/json')

        self.assertEqual(len(Owner.objects.all()), 0)
        self.assertEqual(response_del_1.status_code, 204)
        self.assertEqual(response_del_2.status_code, 204)

    def test_delete_owner_with_perms_without_id(self):
        user = self.man
        login = self.client.login(username=user.username, password="some_password")

        response = self.client.delete('/set_owner/', {'first_name': 'Owner_1'}, content_type='application/json')

        resp_json = response.json()

        self.assertEqual(resp_json['message'], 'Please provide owner id')
        self.assertEqual(len(Owner.objects.all()), 2)
        self.assertEqual(response.status_code, 200)
