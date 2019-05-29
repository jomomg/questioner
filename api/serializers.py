from rest_framework import serializers

from api.models import Event, Question


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'location', 'happening_on')
        read_only_fields = ('id', 'created_at')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'body', 'event', 'created_at')
        read_only_fields = ('id', 'created_at')
