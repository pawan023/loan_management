from celery import Celery
from django.conf import settings
import os
from celery.schedules import crontab
from celery.signals import worker_process_init

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_management.settings')
BROKER_URL = 'redis://localhost:6379'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERYD_TASK_TIME_LIMIT = 40 * 60
CELERYD_TASK_SOFT_TIME_LIMIT = 37 * 60
DJANGO_CELERY_BEAT_TZ_AWARE = True

CELERY_QUEUES_DICT = {
    "sp-search-dataflow-periodic-queue-v1": "sp-search-dataflow-periodic-queue-v1"
}

app = Celery('loan_management.my_celery', broker=BROKER_URL)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_transport_options = {'visibility_timeout': 60 * 60 * 1000}  # 1 hour in ms
