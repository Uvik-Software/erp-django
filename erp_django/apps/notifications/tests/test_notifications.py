from django.contrib.auth.hashers import make_password
from django.test import TestCase, TransactionTestCase

from apps.core.models import User
from apps.notifications.models import Notification


class TestNotifications(TransactionTestCase):

    def setUp(self):
        self.user = User.objects.create(username='uvik_user', password=make_password('password'))
        self.notification = Notification.objects.create(user=self.user, title='Test notice', description='Test')

    def test_get_notification_unauthorized(self):
        response = self.client.get("/notifications/")
        self.assertEqual(response.status_code, 401)

    def test_get_notifications(self):
        self.client.login(username='uvik_user', password='password')
        response = self.client.get('/notifications/')
        body_res = response.json()

        self.assertEqual(body_res['results'][0]['title'], 'Test notice')
        self.assertEqual(response.status_code, 200)

    def test_delete_notification(self):
        self.client.login(username='uvik_user', password='password')
        Notification.objects.create(user=self.user, title='Second notice', description='Test')
        response = self.client.delete('/notifications/1/')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Notification.objects.all().count(), 1)

    def test_delete_all_notifications(self):
        self.client.login(username='uvik_user', password='password')
        Notification.objects.create(user=self.user, title='Second notice', description='Test')
        response = self.client.delete('/notifications/1/?data=all')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Notification.objects.all().count(), 0)

    def test_update_all_notifications(self):
        self.client.login(username='uvik_user', password='password')
        Notification.objects.create(user=self.user, title='Second notice', description='Test')
        response = self.client.put('/notifications/1/', {})

        self.assertEqual(Notification.objects.get(id=2).checked, True)
        self.assertEqual(Notification.objects.get(id=1).checked, True)
        self.assertEqual(response.status_code, 200)
