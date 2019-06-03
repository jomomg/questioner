from rest_framework import serializers

from api.models import Event, Question, Vote


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'location', 'happening_on')
        read_only_fields = ('id', 'created_at')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'body', 'event', 'created_at', 'votes')
        read_only_fields = ('id', 'created_at')


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ('type', 'question')
        read_only_fields = ('question', )
