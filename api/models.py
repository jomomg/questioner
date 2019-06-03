import uuid
import datetime

from django.db import models
from django.contrib.auth.models import User


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
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.utcnow)

    @property
    def votes(self):
        up = Question.objects.filter(vote__type=Vote.UP).count()
        down = Question.objects.filter(vote__type=Vote.DOWN).count()
        return {
            'up': up,
            'down': down,
            'total': up - down
        }


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    url = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VOTE_TYPE_CHOICES = (
        (UP, 'Up'),
        (DOWN, 'Down')
    )

    type = models.IntegerField(choices=VOTE_TYPE_CHOICES)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
