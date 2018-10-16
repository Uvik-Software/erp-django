from django.contrib.auth.hashers import make_password
from django.test import TestCase

from core.models import Developer, User, Manager


class TestCreateUser(TestCase):

    def test_create_user_developer(self):
        try:
            response = self.client.post('/create_user/', {'user_name': '', 'user_password': '',
                                                          'user_role': 'DEVELOPER', 'developer_name': 'POCIK',
                                                          'developer_surname': 'POCIKOVIC',
                                                          'developer_email': 'so@so.com', 'developer_hourly_rate': 15,
                                                          'developer_birthday_date': '1999-10-20',
                                                          'developer_monthly_salary': 1500})
        except Developer.DoesNotExist:
            pass
        else:
            self.assertEqual(len(Developer.objects.all()), 0)
            self.assertEqual(len(User.objects.all()), 0)
            self.assertEqual(response.status_code, 200)

        response_2 = self.client.post('/create_user/', {'user_name': 'User_dev', 'user_password': 'user_password',
                                                        'user_role': 'DEVELOPER', 'developer_name': 'POCIK_2',
                                                        'developer_surname': 'POCIKOVIC_2',
                                                        'developer_email': 'some@some.com', 'developer_hourly_rate': 15,
                                                        'developer_birthday_date': '1998-10-20',
                                                        'developer_monthly_salary': 1500})
        user_dev = Developer.objects.get(user__username='User_dev')
        dev_user = User.objects.get(username='User_dev')

        self.assertEqual(user_dev.user.username, 'User_dev')
        self.assertEqual(user_dev.user.user_type, 'DEVELOPER')
        self.assertEqual(dev_user.developer_set.get(surname='POCIKOVIC_2').surname, 'POCIKOVIC_2')
        self.assertEqual(dev_user.developer_set.get(name='POCIK_2').name, 'POCIK_2')
        self.assertEqual(response_2.status_code, 201)

    def test_create_user_manager(self):
        try:
            response = self.client.post('/create_user/', {'user_name': '', 'user_password': '',
                                                          'user_role': 'MANAGER', 'manager_name': 'KICOP',
                                                          'manager_surname': 'CIVOKICOP', 'manager_email': 'so@so.com',
                                                          'manager_position': 'marketing manager',
                                                          'manager_address': 'some_address',
                                                          'manager_company_name': 'UVIK'})
        except Manager.DoesNotExist:
            pass
        else:
            self.assertEqual(len(Manager.objects.all()), 0)
            self.assertEqual(response.status_code, 200)

        response_2 = self.client.post('/create_user/', {'user_name': 'User_man', 'user_password': 'user_password',
                                                        'user_role': 'MANAGER', 'manager_name': 'KICOP_2',
                                                        'manager_surname': 'CIVOKICOP_2',
                                                        'manager_email': 'some@some.com',
                                                        'manager_position': 'marketing manager',
                                                        'manager_address': 'some_address',
                                                        'manager_company_name': 'UVIK'})
        user_man = Manager.objects.get(owner__username='User_man')
        man_user = User.objects.get(username='User_man')

        self.assertEqual(user_man.owner.username, 'User_man')
        self.assertEqual(user_man.owner.user_type, 'MANAGER')
        self.assertEqual(man_user.manager_set.get(surname='CIVOKICOP_2').surname, 'CIVOKICOP_2')
        self.assertEqual(man_user.manager_set.get(name='KICOP_2').name, 'KICOP_2')
        self.assertEqual(response_2.status_code, 201)