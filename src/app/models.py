import uuid

from django.db import models


class Member(models.Model):
    username = models.CharField(max_length=128, blank=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
