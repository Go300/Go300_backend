from celery.schedules import crontab

from core.celery import app
from proj.models import Subscription


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    for hour in range(0, 23):
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
    print('subscriptions: {}'.format(subscriptions.count()))
