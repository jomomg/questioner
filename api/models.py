import uuid
import datetime
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    location = models.CharField(max_length=60)
    title = models.CharField(max_length=300)
    happening_on = models.DateField()
    created_at = models.DateTimeField(default=datetime.datetime.utcnow)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=120)
    body = models.CharField(max_length=300)
    votes = models.IntegerField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.utcnow)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    url = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
