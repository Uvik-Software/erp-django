from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.test import TestCase, TransactionTestCase

from core.models import Vacation, Developer, User, Manager
import datetime


DATE = datetime.datetime.now()
TO_DATE = datetime.datetime.now() + datetime.timedelta(days=20)


class TestVacation(TransactionTestCase):

    def setUp(self):

        self.dev = Developer.objects.create(
            username="uvik_dev",
            password=make_password("some_password"),
            type="DEVELOPER",
            first_name="John",
            last_name="Doe",
            email="some@some.com",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=50),
            monthly_salary=1000,
        )

        man = Manager.objects.create(
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

        self.vac_dev = Vacation.objects.create(
            user=self.dev,
            from_date=DATE - datetime.timedelta(days=10),
            to_date=TO_DATE.strftime("%Y-%m-%d"),
        )

        self.vac_man = Vacation.objects.create(
            user=man,
            from_date=DATE - datetime.timedelta(days=5),
            to_date=TO_DATE.strftime("%Y-%m-%d"),
            comments="some_comments",
        )

    def test_get_vac_unauthorized(self):
        response = self.client.get("/set_vacation/")
        self.assertEqual(response.status_code, 401)

    def test_get_vac_for_developer(self):
        user = User.objects.get(username='uvik_dev')
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.get('/set_vacation/')
        resp_body = response.json()
        dev_user = Developer.objects.get(user_ptr_id=resp_body["data"][0]["user_id"])
        self.assertEqual(dev_user.username, 'uvik_dev')
        self.assertEqual(response.status_code, 200)

    def test_get_vac_for_manager(self):
        user = User.objects.get(username='uvik_man')
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.get('/set_vacation/')
        resp_body = response.json()
        man_user = Vacation.objects.get(user__id=resp_body["data"][1]["user_id"])
        self.assertEqual(man_user.user.username, 'uvik_man')
        self.assertEqual(response.status_code, 200)

    def test_post_vac_for_developer(self):
        user = User.objects.get(username='uvik_dev')
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.post('/set_vacation/', {'from_date': '2018-11-10', 'to_date': '2018-10-20',
                                                       'is_approved': True, 'developer_id': 1})
        post_check = self.client.get('/set_vacation/')
        body_post_check = post_check.json()
        vacation_post = Vacation.objects.get(user__id=body_post_check['data'][0]['user_id'],
                                             from_date='2018-11-10')

        self.assertEqual(vacation_post.from_date.strftime('%Y-%m-%d'), '2018-11-10')
        self.assertEqual(len(Vacation.objects.all()), 3)
        self.assertEqual(response.status_code, 201)

    def test_post_vac_for_manager(self):
        user = User.objects.get(username='uvik_man')
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.post('/set_vacation/', {'from_date': '2018-12-01', 'to_date': '2018-12-20',
                                                       'is_approved': True, 'developer_id': 1})
        post_check = self.client.get('/set_vacation/')
        body_post_check = post_check.json()
        vacation_post = Vacation.objects.get(user__id=body_post_check['data'][0]['user_id'],
                                             from_date='2018-12-01')

        self.assertEqual(vacation_post.from_date.strftime('%Y-%m-%d'), '2018-12-01')
        self.assertEqual(len(Vacation.objects.all()), 3)
        self.assertEqual(response.status_code, 201)

    @patch('core.signals.gmail_sender')
    def test_put_vac_for_manager(self, gmail_sender_mock):
        user = User.objects.get(username='uvik_man')
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.post('/set_vacation/', {'from_date': '2018-12-01', 'to_date': '2018-12-20',
                                                       'is_approved': True, 'developer_id': 1})

        vac_post_data = Vacation.objects.get(from_date='2018-12-01')
        resp_put = self.client.put('/set_vacation/', {'from_date': '2018-11-01',
                                                      'to_date': '2018-11-20',
                                                      'approved': False,
                                                      'comments': '111111111',
                                                      'id': vac_post_data.id},
                                   content_type='application/json')

        vac_put_data = Vacation.objects.get(from_date='2018-11-01')
        gmail_sender_mock.assert_called_once_with('Approvement about your vacation is updated', 'some@some.com',
                                                  'Approvement about your vacation is left')
        self.assertEqual(vac_post_data.from_date.strftime('%Y-%m-%d'), '2018-12-01')
        self.assertEqual(vac_put_data.from_date.strftime('%Y-%m-%d'), '2018-11-01')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_put.status_code, 200)

    def test_put_vac_for_developer(self):
        user = User.objects.get(username='uvik_dev')
        login = self.client.login(username=user.username, password="some_password")
        fake_dev = Developer.objects.create(
            username="uvik_dev_666", password=make_password("some_password"),
            type="DEVELOPER",
            first_name="John",
            last_name="Smith",
            email="js@js.com",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=50),
            monthly_salary=1000,
        )
        user = User.objects.get(id=fake_dev.user_ptr_id)
        fake_vac = Vacation.objects.create(
            user=user,
            from_date=DATE - datetime.timedelta(days=20),
            to_date=TO_DATE.strftime("%Y-%m-%d"),
        )
        response = self.client.get('/set_vacation/')
        resp_body = response.json()

        resp_put_1 = self.client.put('/set_vacation/', {'from_date': '2017-10-01',
                                                        'to_date': '2017-12-20',
                                                        'approved': True,
                                                        'comments': '111111111',
                                                        'id': resp_body["data"][0]['id']},
                                     content_type='application/json')

        resp_put_2 = self.client.put('/set_vacation/', {'from_date': '2017-09-01',
                                                        'to_date': '2017-12-20',
                                                        'approved': True,
                                                        'comments': '111111111',
                                                        'id': resp_body["data"][2]['id']},
                                     content_type='application/json')

        vac_data_1 = Vacation.objects.get(from_date='2017-10-01')

        try:
            vac_data_2 = Vacation.objects.get(from_date='2017-09-01')
        except Vacation.DoesNotExist:
            vac_data_2 = "You can't update vacation that is not yours"

        self.assertEqual(vac_data_1.to_date.strftime('%Y-%m-%d'), '2017-12-20')
        self.assertEqual(vac_data_2, "You can't update vacation that is not yours")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_put_1.status_code, 200)
        self.assertEqual(resp_put_2.status_code, 200)

    def test_delete_vac_for_developer(self):
        user = User.objects.get(username='uvik_dev')
        login = self.client.login(username=user.username, password="some_password")
        fake_dev = Developer.objects.create(
            username="uvik_dev_666",
            password=make_password("some_password"),
            type="DEVELOPER",
            first_name="John",
            last_name="Smith",
            email="js@js.com",
            hourly_rate=5,
            birthday_date=DATE - datetime.timedelta(days=50),
            monthly_salary=1000,
            )
        user = User.objects.get(id=fake_dev.user_ptr_id)
        fake_vac = Vacation.objects.create(
            user=user,
            from_date=DATE - datetime.timedelta(days=10),
            to_date=TO_DATE.strftime("%Y-%m-%d")
        )
        response = self.client.get('/set_vacation/')
        resp_body = response.json()

        resp_delete_1 = self.client.delete('/set_vacation/',
                                           {'vacation_id': resp_body["data"][0]['id']},
                                           content_type='application/json')

        resp_delete_2 = self.client.delete('/set_vacation/',
                                           {'vacation_id': resp_body["data"][2]['id']},
                                           content_type='application/json')

        self.assertEqual(len(Vacation.objects.all()), 2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_delete_1.status_code, 204)
        self.assertEqual(resp_delete_2.status_code, 200)

    def test_delete_vac_for_manager(self):
        user = User.objects.get(username='uvik_man')
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.get('/set_vacation/')
        resp_body = response.json()
        resp_delete_1 = self.client.delete('/set_vacation/',
                                           {'vacation_id': resp_body["data"][0]['id']},
                                           content_type='application/json')

        resp_delete_2 = self.client.delete('/set_vacation/',
                                           {'vacation_id': resp_body["data"][1]['id']},
                                           content_type='application/json')

        self.assertEqual(len(Vacation.objects.all()), 0)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp_delete_1.status_code, 204)
        self.assertEqual(resp_delete_2.status_code, 204)

    @patch('core.signals.gmail_sender')
    def test_send_mail_approve_vac(self, gmail_sender_mock):
        user = User.objects.get(username='uvik_man')
        login = self.client.login(username=user.username, password="some_password")
        response = self.client.post('/set_vacation/', {'from_date': '2018-12-01', 'to_date': '2018-12-20',
                                                       'is_approved': True, 'developer_id': self.dev.user_ptr_id})

        vacation = Vacation.objects.get(from_date='2018-12-01')
        resp_put = self.client.put('/set_vacation/', {'from_date': '2018-11-01',
                                                      'to_date': '2018-11-20',
                                                      'approved': False,
                                                      'comments': '111111111',
                                                      'id': vacation.id},
                                   content_type='application/json')

        gmail_sender_mock.assert_called_once_with('Approvement about your vacation is updated', 'some@some.com',
                                                  'Approvement about your vacation is left')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(resp_put.status_code, 200)
