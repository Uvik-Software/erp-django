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

# every hour crontab(minute=0, hour='*/1') erp_django.celery.longtime_add
app.conf.beat_schedule = {
    'send-report-every-min': {
        'task': 'erp_django.celery.longtime_add',
        'schedule': crontab(hour="*/1"),
    },
}


""""@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

@app.task
def test(arg):
    print("IAMHERE!!!!!")
    logger.debug("something2")
    print(arg)"""

@app.task
def longtime_add():
    logger.debug("something")
    print('long time task finished11111')
