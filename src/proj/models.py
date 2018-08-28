import uuid

from django.db import models


class Member(models.Model):
    username = models.CharField(max_length=128, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.id)


class Subscription(models.Model):
    member = models.ForeignKey(to='proj.Member', null=False, on_delete=models.CASCADE, related_name='subscriptions')
    departure = models.CharField(max_length=128, blank=False)
    destination = models.CharField(max_length=128, blank=False)
    when = models.CharField(max_length=16, blank=False)
