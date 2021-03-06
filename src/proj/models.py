import uuid

from django.db import models


class Group(models.Model):
    pass


class Member(models.Model):
    username = models.CharField(max_length=128, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    group = models.ForeignKey(to='proj.Group', null=True, on_delete=models.CASCADE, related_name='members')

    def __str__(self):
        return str(self.id)


class Subscription(models.Model):
    member = models.ForeignKey(to='proj.Member', null=False, on_delete=models.CASCADE, related_name='subscriptions')
    departure = models.CharField(max_length=128, blank=False)
    destination = models.CharField(max_length=128, blank=False)
    when = models.CharField(max_length=16, blank=False)


class Confirmation(models.Model):
    subscription = models.ForeignKey(
        to='proj.Subscription',
        on_delete=models.CASCADE,
        related_name='confirmations',
        null=False
    )
    confirmed = models.BooleanField(default=False)
