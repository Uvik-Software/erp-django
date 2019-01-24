import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_django.settings')
app = Celery('erp_django')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'check-events-every-hour': {
        'task': 'erp_django.celery.notification_worker',
        'schedule': crontab(hour="*/24"),  # every hour crontab(minute=0, hour='*/1')
    },
}


@app.task
def notification_worker():
    from apps.notifications.utils import NotificationsProcessor

    NotificationsProcessor().process()
