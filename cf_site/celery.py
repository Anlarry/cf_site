from __future__ import absolute_import, unicode_literals
import  os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cf_site.settings')

app = Celery('cf_site')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

