from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def notify_users(hour, minute):
    print('{0}:{1}'.format(str(hour), str(minute)))
    # when = '{0}:{1}'.format(str(hour), str(minute))
    # subscriptions = Subscription.objects.filter(when=when).all()
    # for subscription in subscriptions:
    #     print(subscription.member.username)
    # print('subscriptions: {}'.format(subscriptions.count()))


tasks = {}

for hour in range(0, 24):
    for minute in (0, 30):
        tasks['notify users_{0}_{1}'.format(hour, minute)] = {
            'task': 'core.celery.notify_users',
            'schedule': crontab(hour=str(hour), minute=str(minute)),
            'args': ((hour + (minute + 30) // 60) % 24, (minute + 30) % 60)
        }

app.conf.beat_schedule = tasks

# @app.on_after_configure.connect
# def setup_periodic_tasks(**kwargs):
#     app.add_periodic_task(
#         notify_users.s(hour=1, minute=(1 + 30)),
#         run_every=crontab(hour='*', minute='*'),
#         name='notify users'
#     )
# for hour in range(0, 23):
#     for minute in (0, 30):
#         sender.add_periodic_task(
#             crontab(hour=str(hour), minute=str(minute)),
#             notify_users.s(hour, minute=(minute + 30)),
#             name='notify users'
#         )
