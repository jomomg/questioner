from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import EventSerializer
from api.models import Event
from utils.response import wrap_response


class EventList(APIView):
    @staticmethod
    def post(request):
        event_data = request.data
        serializer = EventSerializer(data=event_data)
        if serializer.is_valid():
            serializer.save()
            return Response(wrap_response('Event created', data=serializer.data),
                            status=status.HTTP_201_CREATED)
        return Response(wrap_response('An error occurred',
                                      serializer.errors, error=True),
                        status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        response = wrap_response('Retrieved all events', data=serializer.data)
        return Response(response, status.HTTP_200_OK)


class EventDetail(APIView):
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            response = wrap_response('Not found', error=True)
            return Response(response, status.HTTP_404_NOT_FOUND)
        else:
            serializer = EventSerializer(event)
            response = wrap_response('Event retrieved', data=serializer.data)
            return Response(response, status.HTTP_200_OK)
