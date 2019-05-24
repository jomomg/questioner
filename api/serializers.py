from rest_framework import serializers

from api.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'title', 'location', 'happening_on')
        read_only_fields = ('id', 'created_at')
