from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task
def notify_members(hour, minute):
    from proj.models import Subscription, Confirmation
    when = '{0}:{1}'.format(str(hour), str(minute))
    subscriptions = list(Subscription.objects.filter(when=when).all())
    for subscription in subscriptions:
        confirmation = Confirmation.objects.create(member=subscription.member, when=when)
        subscription.member.gcmdevice_set.last().send_message(
            'Через полчаса у вас состоится поездка! '
            'Подтвердите что вы готовы и выходите к выходу!'
            'Ваш id: {}'.format(confirmation.id)
        )


@app.task
def group_members(hour, minute):
    from proj.models import Confirmation, Group
    when = '{0}:{1}'.format(str(hour), str(minute))
    confirmations = list(Confirmation.objects.filter(when=when).filter(confirmed=True).all())
    while len(confirmations) >= 7:
        group = Group.objects.create()
        for _ in range(4):
            confirmation = confirmations.pop()
            group.members.add(confirmation.member)
            group.save()
    if len(confirmations) == 6:
        group = Group.objects.create()
        for _ in range(3):
            confirmation = confirmations.pop()
            group.members.add(confirmation.member)
            group.save()
    if len(confirmations) == 5:
        group = Group.objects.create()
        for _ in range(3):
            confirmation = confirmations.pop()
            group.members.add(confirmation.member)
            group.save()
        group = Group.objects.create()
        for _ in range(2):
            confirmation = confirmations.pop()
            group.members.add(confirmation.member)
            group.save()
    if 4 >= len(confirmations) >= 1:
        group = Group.objects.create()
        while len(confirmations) > 0:
            confirmation = confirmations.pop()
            group.members.add(confirmation.member)
            group.save()

    Confirmation.objects.all().delete()


tasks = {}

for hour in range(0, 24):
    for minute in (0, 30):
        tasks['notify users_{0}_{1}'.format(hour, minute)] = {
            'task': 'core.celery.notify_members',
            'schedule': crontab(hour=str(hour), minute=str(minute)),
            'args': ((hour + (minute + 30) // 60) % 24, (minute + 30) % 60)
        }
    for minute in (20, 50):
        tasks['notify users_{0}_{1}'.format(hour, minute)] = {
            'task': 'core.celery.group_members',
            'schedule': crontab(hour=str(hour), minute=str(minute)),
            'args': ((hour + (minute + 10) // 60) % 24, (minute + 10) % 60)
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
