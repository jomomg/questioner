from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status

from api.models import Question, Vote
from api.serializers import QuestionSerializer, VoteSerializer
from .base import ListViewBase, DetailViewBase
from utils.response import success_, error_


class QuestionList(ListViewBase):
    serializer_class = QuestionSerializer
    model = Question


class QuestionDetail(DetailViewBase):
    serializer_class = QuestionSerializer
    model = Question


class VoteView(APIView):
    @staticmethod
    def get_object(model, pk):
        try:
            obj = model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise exceptions.NotFound('Question not found')
        else:
            return obj

    def put(self, request, pk):
        if 'type' not in request.data:
            raise exceptions.ParseError('you must include the vote type')
        if request.data['type'] not in (1, -1):
            raise exceptions.ParseError('vote must be either 1 or -1')
        vote_info = {
            'type': request.data['type'],
            'question': self.get_object(Question, pk),
            'user': request.user
        }
        new_vote = Vote(**vote_info)
        new_vote.save()
        serializer = VoteSerializer(new_vote)
        return Response(success_('Vote recorded', serializer.data), status.HTTP_200_OK)
