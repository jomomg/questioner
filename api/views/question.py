from api.models import Question
from api.serializers import QuestionSerializer
from .base import ListViewBase, DetailViewBase


class QuestionList(ListViewBase):
    serializer_class = QuestionSerializer
    model = Question


class QuestionDetail(DetailViewBase):
    serializer_class = QuestionSerializer
    model = Question
