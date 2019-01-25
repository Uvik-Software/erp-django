from django.db import models

from apps.core.models import User


class Notification(models.Model):
    TYPE_NOTIFICATION = (
        ('START_PROJECT', 'Start project'),
        ('DEADLINE', 'Deadline'),
        ('BIRTHDAY', 'Birthday'),
        ('VACATION', 'Vacation'),
        ('HOLIDAY', 'Holiday'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, default='')
    description = models.CharField(max_length=256, default='')
    checked = models.BooleanField(default=False)
    type_notice = models.CharField(max_length=16, choices=TYPE_NOTIFICATION, default='START_PROJECT')
