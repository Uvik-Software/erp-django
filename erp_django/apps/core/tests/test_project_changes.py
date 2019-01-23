from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.test import TestCase

from apps.core.models import User, Manager, Project, Client, Owner, BankInfo

import datetime

DATE = datetime.datetime.now()
TO_DATE = datetime.datetime.now() + datetime.timedelta(days=20)


class TestProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        bank_info_owner_1 = BankInfo.objects.create(bank_name="PAT UkrSibBank", bank_account_number="3244224242121",
                                                    bank_address="111111, Ukraine, Chernivetska obl., "
                                                                 "m. Chernivtsi, vul. Kupsa, 44",
                                                    bank_code="345098")

        cls.uvik_client = Client.objects.create(
            username='uvik_client',
            first_name='some_client',
            position='some_position',
            company_name='ABCD',
            address='some_address',
            email='po@po.com',
            phone='123456789',
            tax_number='0987654321',
        )

        manager = Manager.objects.create(
            username="uvik_man",
            password=make_password("some_password"),
            type="MANAGER",
            first_name="some_manager",
            last_name="some_surname",
            email="manager_email@uvik.net",
            position="manager",
            address="some_address",
            company_name="UVIK",
            is_staff=True
        )

        cls.owner_1 = Owner.objects.create(
            first_name="Owner_1",
            last_name="Surname_1",
            father_name="Fname_1",
            address="100 Main Street, Nowhere city",
            tax_number="123456789",
            num_contract_with_dev="14/9",
            date_contract_with_dev=DATE - datetime.timedelta(days=365),
            bank_info=bank_info_owner_1,
        )

    @patch('core.signals.create_g_calendar_event')
    def test_url_exists_get_unauthorized(self, create_g_calendar_event_mock):
        user_manager = Manager.objects.get(username='uvik_man')
        client = Client.objects.get(first_name='some_client')
        create_g_calendar_event_mock.return_value = 'Created event in google calendar'
        project = Project.objects.create(
            project_name='Project_1',
            project_type='OUTSTAFF',
            project_description='some_description',
            currency='euros',
            basic_price=4000,
            manager_info=user_manager,
            client=client,
            all_time_money_spent=1000,
            deadline=DATE + datetime.timedelta(days=50),
            project_started_date=DATE,
            owner=self.owner_1
        )
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 401)

    @patch('core.signals.create_g_calendar_event')
    def test_url_exists_get_authorized(self, create_g_calendar_event_mock):
        user = Manager.objects.get(username='uvik_man')
        login = self.client.login(username=user.username, password='some_password')
        client = Client.objects.get(first_name='some_client')
        create_g_calendar_event_mock.return_value = 'Created event in google calendar'
        project = Project.objects.create(
            project_name='Project_1',
            project_type='OUTSTAFF',
            project_description='some_description',
            currency='euros',
            basic_price=4000,
            manager_info=user,
            client=client,
            all_time_money_spent=1000,
            deadline=DATE + datetime.timedelta(days=50),
            project_started_date=DATE,
            owner=self.owner_1
        )
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)

    @patch('core.signals.gmail_sender')
    @patch('core.signals.create_g_calendar_event')
    @patch('core.signals.update_g_calendar_event')
    def test_changed_field_start_date_proj(self, update_g_calendar_event_mock,
                                           create_g_calendar_event_mock, gmail_sender_mock):
        user = User.objects.get(username='uvik_man')
        client = self.uvik_client
        login = self.client.login(username=user.username, password='some_password')
        create_g_calendar_event_mock.return_value = 'Created event in google calendar'
        response = self.client.post('/projects/', {'project_name': 'Project_2', 'project_type': 'OUTSTAFF',
                                                   'project_description': 'some_description_2',
                                                   'currency': 'dollars', 'basic_price': 4000,
                                                   'manager_info': user.id,
                                                   'client': client.id,
                                                   'all_time_money_spent': 1000, 'deadline': '2018-12-10',
                                                   'project_started_date': '2018-08-01', 'owner': self.owner_1.id})

        update_g_calendar_event_mock.return_value = 'Updated event in google calendar'
        project = Project.objects.get(project_name='Project_2')
        project.project_started_date = '2018-09-20'
        project.save()

        gmail_sender_mock.assert_called_once_with("Project started date for project 'Project_2' has changed",
                                                  "manager_email@uvik.net",
                                                  "Changes for project 'Project_2' started date", cc=[])

        self.assertEqual(response.status_code, 201)

    @patch('core.signals.gmail_sender')
    @patch('core.signals.create_g_calendar_event')
    @patch('core.signals.update_g_calendar_event')
    def test_changed_field_deadline_proj(self, update_g_calendar_event_mock,
                                         create_g_calendar_event_mock, gmail_sender_mock):
        user = User.objects.get(username='uvik_man')
        client = self.uvik_client
        login = self.client.login(username=user.username, password='some_password')
        create_g_calendar_event_mock.return_value = 'Created event in google calendar'
        response = self.client.post('/projects/', {'project_name': 'Project_3', 'project_type': 'OUTSTAFF',
                                                   'project_description': 'some_description_3',
                                                   'currency': 'dollars', 'basic_price': 4000,
                                                   'manager_info': user.id,
                                                   'client': client.id,
                                                   'all_time_money_spent': 1000, 'deadline': '2018-12-10',
                                                   'project_started_date': '2018-08-01', 'owner': self.owner_1.id})

        update_g_calendar_event_mock.return_value = 'Updated event in google calendar'
        project = Project.objects.get(project_name='Project_3')
        project.deadline = '2018-11-29'
        project.save()

        gmail_sender_mock.assert_called_once_with("Deadline for project 'Project_3' has changed",
                                                  'manager_email@uvik.net',
                                                  "Changes for project 'Project_3' deadline", cc=[])
        self.assertEqual(response.status_code, 201)
