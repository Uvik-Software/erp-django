from django.contrib.auth.hashers import make_password
from django.test import TestCase

from core.models import Developer, User, Manager


class TestCreateUser(TestCase):

    def test_create_user_developer(self):
        try:
            response = self.client.post('/create_user/', {'user_name': '', 'user_password': '',
                                                          'user_role': 'DEVELOPER', 'developer_name': 'DEV_1',
                                                          'developer_surname': 'Familia_1',
                                                          'developer_email': 'so@so.com', 'developer_hourly_rate': 15,
                                                          'developer_birthday_date': '1999-10-20',
                                                          'developer_monthly_salary': 1500})
        except (Developer.DoesNotExist, User.DoesNotExist):
            pass
        else:
            self.assertEqual(len(Developer.objects.all()), 0)
            self.assertEqual(len(User.objects.all()), 0)
            self.assertEqual(response.status_code, 200)

        response_2 = self.client.post('/create_user/', {'user_name': 'User_dev', 'user_password': 'user_password',
                                                        'user_role': 'DEVELOPER', 'developer_name': 'DEV_2',
                                                        'developer_surname': 'Familia_2',
                                                        'developer_email': 'some@some.com', 'developer_hourly_rate': 15,
                                                        'developer_birthday_date': '1998-10-20',
                                                        'developer_monthly_salary': 1500})

        user_dev = Developer.objects.get(user__username='User_dev')
        dev_user = User.objects.get(username='User_dev')

        self.assertEqual(user_dev.user.username, 'User_dev')
        self.assertEqual(user_dev.user.user_type, 'DEVELOPER')
        self.assertEqual(dev_user.developer_set.get(surname='Familia_2').surname, 'Familia_2')
        self.assertEqual(dev_user.developer_set.get(name='DEV_2').name, 'DEV_2')
        self.assertEqual(response_2.status_code, 201)

    def test_create_user_manager(self):
        try:
            response = self.client.post('/create_user/', {'user_name': '', 'user_password': '',
                                                          'user_role': 'MANAGER', 'manager_name': 'MAN_1',
                                                          'manager_surname': 'Familia_1', 'manager_email': 'so@so.com',
                                                          'manager_position': 'marketing manager',
                                                          'manager_address': 'some_address',
                                                          'manager_company_name': 'UVIK'})
        except (Manager.DoesNotExist, User.DoesNotExist):
            pass
        else:
            self.assertEqual(len(Manager.objects.all()), 0)
            self.assertEqual(response.status_code, 200)

        response_2 = self.client.post('/create_user/', {'user_name': 'User_man', 'user_password': 'user_password',
                                                        'user_role': 'MANAGER', 'manager_name': 'MAN_2',
                                                        'manager_surname': 'Familia_2',
                                                        'manager_email': 'some@some.com',
                                                        'manager_position': 'marketing manager',
                                                        'manager_address': 'some_address',
                                                        'manager_company_name': 'UVIK'})

        user_man = Manager.objects.get(owner__username='User_man')
        man_user = User.objects.get(username='User_man')

        self.assertEqual(user_man.owner.username, 'User_man')
        self.assertEqual(user_man.owner.user_type, 'MANAGER')
        self.assertEqual(man_user.manager_set.get(surname='Familia_2').surname, 'Familia_2')
        self.assertEqual(man_user.manager_set.get(name='MAN_2').name, 'MAN_2')
        self.assertEqual(response_2.status_code, 201)
