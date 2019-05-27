from api.models import Event
from api.serializers import EventSerializer
from .base import ListViewBase, DetailViewBase


class EventList(ListViewBase):
    serializer_class = EventSerializer
    model = Event


class EventDetail(DetailViewBase):
    serializer_class = EventSerializer
    model = Event
