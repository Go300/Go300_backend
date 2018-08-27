from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

from app.models import Subscription

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('core.settings', namespace='CELERY')

app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for hour in range(0, 11):
        for minute in (0, 30):
            sender.add_periodic_task(
                crontab(hour=hour, minute=minute),
                notify_users.s(hour, minute=(minute + 30))
            )


@app.task
def notify_users(hour, minute):
    when = '{0}:{1}'.format(str(hour), str(minute))
    subscriptions = Subscription.objects.filter(when=when).all()
    for subscription in subscriptions:
        print(subscription.member.username)
