from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import EventSerializer, QuestionSerializer
from api.models import Event, Question
from utils.response import wrap_response


class ListViewBase(APIView):
    serializer_class = None
    model = None

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                wrap_response(f'{self.model.__name__} created',
                              data=serializer.data),
                status=status.HTTP_201_CREATED)
        return Response(wrap_response('An error occurred',
                                      serializer.errors, error=True),
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        events = self.model.objects.all()
        serializer = self.serializer_class(events, many=True)
        response = wrap_response(
            f'Retrieved all {self.model.__name__.lower()}s',
            data=serializer.data)
        return Response(response, status.HTTP_200_OK)


class DetailViewBase(APIView):
    serializer_class = None
    model = None
    
    def get(self, request, pk):
        try:
            event = self.model.objects.get(pk=pk)
        except self.model.DoesNotExist:
            response = wrap_response('Not found', error=True)
            return Response(response, status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            response = wrap_response('An error occurred', data=err, error=True)
            return Response(response, status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(event)
            response = wrap_response(f'{self.model.__name__} retrieved',
                                     data=serializer.data)
            return Response(response, status.HTTP_200_OK)


class EventList(ListViewBase):
    serializer_class = EventSerializer
    model = Event


class EventDetail(DetailViewBase):
    serializer_class = EventSerializer
    model = Event


class QuestionList(ListViewBase):
    serializer_class = QuestionSerializer
    model = Question


class QuestionDetail(DetailViewBase):
    serializer_class = QuestionSerializer
    model = Question

